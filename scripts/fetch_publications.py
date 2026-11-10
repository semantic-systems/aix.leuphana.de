import os
import sys
import json
import time
import re
from datetime import datetime, timezone
import subprocess
import html
import glob
import requests
from urllib.parse import urlsplit

# dblp's search API and record pages sit behind a bot challenge; its official SPARQL
# endpoint is open to scripts and has the same data. Ricardo Usbeck's dblp person ID:
DBLP_SPARQL_URL = "https://sparql.dblp.org/sparql"
DBLP_PERSON = "https://dblp.org/pid/65/9656"
OUTPUT_DIR = "_publications"
STATE_FILE = "_publications/.state.json"

# Honest identification for the public APIs used below (DBLP, OpenAlex, Crossref,
# Semantic Scholar, Zenodo, ACL Anthology). No browser automation, no scraping of
# sites whose terms forbid it (e.g. Google Scholar).
USER_AGENT = "AIX-Website-PublicationFetcher/2.0 (+https://aix.leuphana.de; mailto:aix@leuphana.de)"

class ApiFetcher:
    """Plain HTTP client: waits between requests to the same host and backs off
    when a server answers 429/5xx (respecting Retry-After)."""
    _instance = None
    MIN_INTERVAL = 1.0  # seconds between two requests to the same host
    MAX_ATTEMPTS = 4

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.s2_api_key = os.environ.get("S2_API_KEY", "")  # optional, free from Semantic Scholar
        self._last_request = {}
        self.last_status = None  # HTTP status of the most recent request (None if it failed)

    def _get(self, url, params=None, accept="application/json"):
        host = urlsplit(url).netloc
        for attempt in range(self.MAX_ATTEMPTS):
            wait = self._last_request.get(host, 0) + self.MIN_INTERVAL - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last_request[host] = time.monotonic()
            try:
                headers = {"Accept": accept}
                if self.s2_api_key and host == "api.semanticscholar.org":
                    headers["x-api-key"] = self.s2_api_key
                resp = self.session.get(url, params=params, headers=headers, timeout=30)
                self.last_status = resp.status_code
            except requests.RequestException as e:
                self.last_status = None
                log(f"Request to {host} failed ({type(e).__name__}), retrying", "WARN")
                time.sleep(2 ** attempt)
                continue
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < self.MAX_ATTEMPTS - 1:
                retry_after = resp.headers.get("Retry-After", "")
                delay = int(retry_after) if retry_after.isdigit() else 2 ** (attempt + 1)
                time.sleep(min(delay, 60))
                continue
            return resp
        return None

    def get_json(self, url, params=None):
        resp = self._get(url, params)
        if resp is None or resp.status_code >= 400:
            return None
        try:
            return resp.json()
        except ValueError:
            return None

    def get_text(self, url, params=None):
        resp = self._get(url, params, accept="text/plain, */*;q=0.8")
        if resp is None or resp.status_code >= 400:
            return ""
        return resp.text

    def close(self):
        self.session.close()

# ─── Logging helpers ───────────────────────────────────────

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}]  {msg}")

def log_header(title):
    print()
    print("━" * 60)
    print(f"  {title}")
    print("━" * 60)

def log_summary(label, value):
    print(f"  {label:<35} {value}")

# ─── State management ─────────────────────────────────────

def load_state():
    """Load the state file tracking which publications have abstracts."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"summary": {}, "publications": {}}

def save_state(state):
    """Recalculate summary stats and save the state file."""
    pubs = state.get("publications", {})
    total = len(pubs)
    with_abstract = sum(1 for v in pubs.values() if v.get("has_abstract"))
    without_abstract = total - with_abstract

    total_conference = sum(1 for v in pubs.values() if v.get("is_conference"))
    total_journal = sum(1 for v in pubs.values() if v.get("is_journal"))
    total_archive = sum(1 for v in pubs.values() if v.get("is_archive"))

    state["summary"] = {
        "total_publications": total,
        "with_abstract": with_abstract,
        "without_abstract": without_abstract,
        "total_conference": total_conference,
        "total_journal": total_journal,
        "total_archive": total_archive,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

# ─── Core functions ────────────────────────────────────────

def sanitize_filename(title):
    filename = re.sub(r'[^a-zA-Z0-9\s]', '', title).strip()
    filename = re.sub(r'\s+', '-', filename).lower()
    return filename[:100].rstrip('-')

# dblp RDF class -> the publication type names of the dblp search API used by this script
DBLP_TYPES = {
    "Inproceedings": "Conference and Workshop Papers",
    "Article": "Journal Articles",
    "Informal": "Informal and Other Publications",
    "Editorship": "Editorship",
    "Incollection": "Parts in Books or Collections",
    "Book": "Books and Theses",
    "Data": "Data and Artifacts",
    "Reference": "Reference Works",
}

def sparql_select(query):
    """Run a SELECT query against dblp's SPARQL endpoint and return plain dict rows."""
    fetcher = ApiFetcher.get_instance()
    resp = fetcher._get(DBLP_SPARQL_URL, params={"query": query}, accept="application/sparql-results+json")
    if resp is None or resp.status_code >= 400:
        raise RuntimeError(f"dblp SPARQL request failed (HTTP {getattr(resp, 'status_code', 'no response')})")
    rows = resp.json().get("results", {}).get("bindings", [])
    return [{k: v.get("value") for k, v in row.items()} for row in rows]

def fetch_dblp_publications():
    """Fetch all publications (incl. edited volumes) of DBLP_PERSON from dblp."""
    log("Querying dblp SPARQL endpoint...")
    meta_query = f"""PREFIX dblp: <https://dblp.org/rdf/schema#>
SELECT ?pub (SAMPLE(?t) AS ?title) (SAMPLE(?y) AS ?year) (SAMPLE(?ty) AS ?type) (SAMPLE(?v) AS ?venue)
       (SAMPLE(?d) AS ?doi) (SAMPLE(?page) AS ?ee) (SAMPLE(?pg) AS ?pages) (SAMPLE(?vol) AS ?volume) (SAMPLE(?iss) AS ?number)
WHERE {{
  ?pub dblp:createdBy <{DBLP_PERSON}> ; dblp:title ?t ; a ?ty .
  FILTER(?ty != dblp:Publication)
  OPTIONAL {{ ?pub dblp:yearOfPublication ?y }}
  OPTIONAL {{ ?pub dblp:publishedIn ?v }}
  OPTIONAL {{ ?pub dblp:doi ?d }}
  OPTIONAL {{ ?pub dblp:primaryDocumentPage ?page }}
  OPTIONAL {{ ?pub dblp:pagination ?pg }}
  OPTIONAL {{ ?pub dblp:publishedInJournalVolume ?vol }}
  OPTIONAL {{ ?pub dblp:publishedInJournalVolumeIssue ?iss }}
}} GROUP BY ?pub"""
    people_query = f"""PREFIX dblp: <https://dblp.org/rdf/schema#>
SELECT ?pub ?ord ?name ?role WHERE {{
  ?pub dblp:createdBy <{DBLP_PERSON}> ; dblp:hasSignature ?sig .
  ?sig dblp:signatureOrdinal ?ord ; dblp:signatureDblpName ?name ; a ?role .
  FILTER(?role IN (dblp:AuthorSignature, dblp:EditorSignature))
}}"""
    try:
        meta = sparql_select(meta_query)
        people = sparql_select(people_query)
    except Exception as e:
        log(f"dblp request failed: {e}", "ERROR")
        return []

    authors, editors = {}, {}
    for row in people:
        target = editors if row["role"].endswith("EditorSignature") else authors
        target.setdefault(row["pub"], []).append((int(row["ord"]), row["name"]))

    publications = []
    for row in meta:
        uri = row["pub"]
        pub_type = DBLP_TYPES.get(row.get("type", "").rsplit("#", 1)[-1], "")
        venue = row.get("venue") or ""
        doi = row.get("doi") or ""
        names = authors.get(uri) or editors.get(uri) or []
        pub = {
            "key": uri.split("/rec/", 1)[-1],
            "title": (row.get("title") or "").strip().rstrip('.'),
            "year": (row.get("year") or "")[:4],
            "venue": venue,
            "doi": doi.replace("https://doi.org/", "") if doi else None,
            "ee": row.get("ee"),
            "type": pub_type,
            "pages": row.get("pages"),
            "volume": row.get("volume"),
            "number": row.get("number"),
            "is_editorship": pub_type == "Editorship",
            "is_conference": False,
            "is_journal": False,
            "is_archive": False,
            "authors": [name for _, name in sorted(names)],
        }
        if pub_type == "Conference and Workshop Papers":
            pub["is_conference"] = True
            if venue: pub["conference"] = re.sub(r"\s*\([^)]*\)", "", venue).strip()
        elif pub_type == "Journal Articles":
            pub["is_journal"] = True
            if venue: pub["journal"] = venue
        elif "Informal" in pub_type:
            pub["is_archive"] = True
        publications.append(pub)

    log(f"dblp fetch complete: {len(publications)} publications retrieved.")
    return publications

def enrich_from_crossref(pub):
    """Add full venue title, publisher and editors from Crossref (best effort, DOI only)."""
    if not pub.get("doi"):
        return
    data = ApiFetcher.get_instance().get_json(f"https://api.crossref.org/works/{pub['doi']}", params={"mailto": "aix@leuphana.de"})
    message = (data or {}).get("message", {})
    # Book chapters list the series first ("Lecture Notes in Computer Science"), then the book title
    container = (message.get("container-title") or [""])[-1]
    if container:
        pub["venue_full"] = container
    if message.get("publisher"):
        pub["publisher"] = message["publisher"]
    editors = [" ".join(x for x in (e.get("given"), e.get("family")) if x) for e in message.get("editor", [])]
    if editors and not pub.get("is_editorship"):
        pub["editors"] = [e for e in editors if e]

def bibtex_escape(value):
    return str(value).replace("{", "\\{").replace("}", "\\}")

def build_dblp_bibtex(pub):
    """BibTeX in dblp's layout, built from the dblp metadata (dblp's .bib export is not
    reachable for scripts). Existing publication files are never rewritten."""
    if not pub.get("key"):
        return ""
    entry = {
        "Conference and Workshop Papers": "inproceedings", "Journal Articles": "article",
        "Editorship": "proceedings", "Parts in Books or Collections": "incollection",
        "Books and Theses": "book", "Data and Artifacts": "misc",
    }.get(pub.get("type"), "misc")
    fields = []
    names = " and\n                  ".join(pub.get("authors", []))
    if names:
        fields.append(("editor" if pub.get("is_editorship") else "author", names))
    if pub.get("editors"):
        fields.append(("editor", " and\n                  ".join(pub["editors"])))
    fields.append(("title", pub.get("title", "")))
    venue = pub.get("venue_full") or pub.get("venue")
    if venue:
        fields.append(("journal" if entry == "article" else "booktitle" if entry in ("inproceedings", "incollection") else "howpublished", venue))
    for name in ("volume", "number", "pages"):
        if pub.get(name):
            fields.append((name, str(pub[name]).replace("-", "--")))
    if pub.get("publisher"):
        fields.append(("publisher", pub["publisher"]))
    if pub.get("year"):
        fields.append(("year", pub["year"]))
    if pub.get("ee"):
        fields.append(("url", pub["ee"]))
    if pub.get("doi"):
        fields.append(("doi", pub["doi"]))
    body = ",\n".join(f"  {name:<12} = {{{bibtex_escape(value) if name not in ('author', 'editor', 'url', 'doi') else value}}}" for name, value in fields)
    body += ",\n  bibsource    = {dblp computer science bibliography, https://dblp.org}"
    return f"@{entry}{{DBLP:{pub['key']},\n{body}\n}}"

def generate_markdown(pub, bibtex, filepath, abstract=""):
    title = pub.get("title", "Untitled").replace('"', '\\"')
    year = pub.get("year", "")
    doi = pub.get("doi", "")
    authors = pub.get("authors", [])

    md = "---\n"
    md += "layout: publication\n"
    md += f'title: "{title}"\n'
    if year:
        md += f"year: {year}\n"

    if authors:
        md += "authors:\n"
        for a in authors:
            md += f"  - \"{a}\"\n"

    if doi:
        doi_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
        md += f'doi: "{doi_url}"\n'

    is_conference = pub.get("is_conference", False)
    is_journal = pub.get("is_journal", False)
    is_archive = pub.get("is_archive", False)
    conference_name = pub.get("conference", "")
    journal_name = pub.get("journal", "")

    md += f"is_conference: {str(is_conference).lower()}\n"
    md += f"is_journal: {str(is_journal).lower()}\n"
    md += f"is_archive: {str(is_archive).lower()}\n"
    
    if is_conference and conference_name:
        c_name = conference_name.replace('"', '\\"')
        year_str = str(year)
        if year_str and year_str not in c_name:
            c_name = f"{c_name} {year_str}"
        md += f'conference: "{c_name}"\n'
    elif is_journal and journal_name:
        j_name = journal_name.replace('"', '\\"')
        md += f'journal: "{j_name}"\n'

    md += "---\n\n"

    if abstract:
        md += "> **Abstract:**\n"
        md += f"> {abstract}\n\n"
    else:
        md += "*Abstract not available.*\n\n"

    if bibtex:
        md += "<details markdown=\"1\" style=\"margin-top: 1.5rem;\">\n"
        md += "  <summary style=\"cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;\">Show BibTeX</summary>\n\n"
        md += "{% raw %}\n"
        md += "```bibtex\n"
        md += f"{bibtex.strip()}\n"
        md += "```\n"
        md += "{% endraw %}\n"
        md += "</details>\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

def update_abstract_in_file(filepath, abstract):
    """Replace the '*Abstract not available.*' placeholder with the actual abstract."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "*Abstract not available.*" not in content:
        return False

    abstract_block = f"> **Abstract:**\n> {abstract}\n"
    content = content.replace("*Abstract not available.*", abstract_block)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

# ─── Last Layer Abstract Verification & Fallback (Phase 3) ───

CURATED_ABSTRACTS = {
    "8th Challenge on Question Answering over Linked Data": (
        "Recent years have seen a growing amount of research on question answering (QA) over Semantic Web data, "
        "shaping an interaction paradigm that allows end users to profit from the expressivity of Semantic Web knowledge bases. "
        "The Question Answering over Linked Data (QALD) challenge is an open challenge series on question answering over Linked Data. "
        "In this invited paper, we present the results and insights of the 8th Open Challenge on Question Answering over Linked Data (QALD-8), "
        "evaluating multilingual question answering systems over RDF knowledge graphs."
    ),
    "9th Challenge on Question Answering over Linked Data": (
        "Recent years have seen a growing amount of research on question answering (QA) over Semantic Web data, "
        "shaping an interaction paradigm that allows end users to profit from the expressive power of Semantic Web standards. "
        "At the same time, QA systems hide their complexity behind an intuitive and easy-to-use interface. "
        "However, the growing amount of data available on the Semantic Web has led to a heterogeneous data landscape "
        "where QA systems struggle to keep up with the volume, variety and veracity of the underlying knowledge. "
        "The Question Answering over Linked Data (QALD) challenges aim to provide up-to-date benchmarks for assessing and "
        "comparing state-of-the-art systems that mediate between a user, expressing his or her information need in natural language, "
        "and RDF data. In this paper, we present the setup, tasks, and results of the 9th Open Challenge on Question Answering over Linked Data (QALD-9)."
    ),
    "OKBQA: an Open Collaboration Framework": (
        "OKBQA is an open collaboration framework for the development of natural language question-answering systems over knowledge bases. "
        "Approaches to ease access to Linked Data include graphical query interfaces, agent-based systems, and natural language interfaces. "
        "OKBQA provides a standardized pipeline architecture and public repository for modular question answering over Linked Data."
    ),
    "DICE @ TREC-IS 2018: Combining Knowledge Graphs and Deep Learning to Identify Crisis-Relevant Tweets": (
        "In this paper, we describe our submissions to the TREC Incident Stream (TREC-IS) challenge 2018. "
        "We investigated different machine learning approaches to classify crisis-related tweets into different information types. "
        "We incorporated knowledge graphs as features into this social media analysis, in addition to bag of words, word embeddings, "
        "time data, and event-types. Further, we evaluate state-of-the-art classification models on 31 generated features sets. "
        "Our TREC-IS results indicate that a model based on combining knowledge graphs (i.e., Babelfy), word embeddings and textual "
        "features outperforms classical machine learning models."
    ),
    "Question Answering Over Linked Data: What is Difficult to Answer? What Affects the F scores?": (
        "We present a fine-grained analysis of the Question Answering over Linked Data (QALD-6) challenge. "
        "We divide the QALD-6 questions into 8 main categories and compare state-of-the-art questions answering (QA) "
        "systems over Linked Data against the individual categories. We show the difficulty (in terms of overall F scores "
        "of the QA systems) of each category. We show the effect of various natural language and SPARQL features such as "
        "the number of triple patterns, number of keywords, the answer size, the type of answers, the effect of aggregate "
        "functions, and the SPARQL query forms on the overall F scores of the QA systems."
    ),
    "Towards an Interoperable Ecosystem of AI and LT Platforms: A Roadmap for the Implementation of Different Levels of Interoperability": (
        "With regard to the wider area of AI/LT platform interoperability, we concentrate on two core aspects: "
        "(1) cross-platform search and discovery of resources and services; (2) composition of cross-platform service workflows. "
        "We devise five different levels (of increasing complexity) of platform interoperability that we suggest to implement "
        "in a wider federation of AI/LT platforms. We illustrate the approach using the five emerging AI/LT platforms "
        "AI4EU, ELG, Lynx, QURATOR and SPEAKER."
    ),
    "DBLP-QuAD DBLP Dump": (
        "This is the RDF dump of DBLP released on August 1, 2022. The DBLP RDF dump is published to allow "
        "fair and replicable evaluation of Knowledge Graph Question Answering (KGQA) systems with the DBLP-QuAD dataset."
    ),
    "dice-group/DBpedia-Chatlog-Analysis": (
        "Open-source software repository and code for the paper: An Approach for Ex-Post-Facto Analysis of "
        "Knowledge Graph-Driven Chatbots – The DBpedia Chatbot (http://chat.dbpedia.org/)."
    )
}

def clean_abstract_text(text):
    """Normalize whitespace and strip HTML/JATS tags from an abstract."""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = html.unescape(clean)
    clean = " ".join(clean.split())
    clean = re.sub(r'^(?:Abstract|Summary)[\.\:\—\-\s]*', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'([a-z])\.([A-Z][a-z])', r'\1. \2', clean)  # "intensive.Moreover" -> "intensive. Moreover"
    return clean.strip()

def extract_abstract_from_file(filepath):
    """Extract current abstract text from a publication markdown file."""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if "*Abstract not available.*" in content:
        return ""
    if "*Proceedings volume" in content:
        return "*Proceedings volume.*"
    if "*Preface" in content:
        return "*Preface.*"
    match = re.search(r'> \*\*Abstract:\*\*\s*\n((?:> .*\n?)+)', content)
    if match:
        lines = [line.lstrip('> ').strip() for line in match.group(1).strip().splitlines()]
        return " ".join(lines).strip()
    return ""

def extract_doi_from_file(filepath):
    """Extract DOI from publication frontmatter."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^doi:\s*"?(?:https?://doi\.org/)?([^"\n\r]+)"?', content, re.MULTILINE)
    if match:
        doi = match.group(1).strip()
        return doi if doi else None
    return None

def is_abstract_incomplete(abstract, title=""):
    """Check if an abstract is missing or cut off mid-sentence."""
    if not abstract or not abstract.strip():
        return True
    text = abstract.strip()
    if "*Abstract not available.*" in text:
        return True
    if text.startswith("*Proceedings volume") or text.startswith("*Preface"):
        return False
    if title and any(title.lower().startswith(p) for p in ["proceedings of", "joint proceedings of", "preface"]):
        if "*Proceedings volume" in text or "*Preface" in text:
            return False
    if text.endswith("...") or text.endswith("…"):
        return True
    # If the abstract is relatively short (< 600 chars) and doesn't end with standard closing punctuation
    if len(text) < 600 and text[-1] not in ('.', '!', '?', '"', "'", ')'):
        return True
    return False

def set_or_update_abstract_in_file(filepath, abstract):
    """Replace an existing abstract or placeholder with the full, complete abstract."""
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Format multi-paragraph abstract nicely for markdown blockquotes
    if abstract.startswith("*"):
        new_block = f"{abstract}\n"
    else:
        formatted = "\n> \n> ".join(p.strip() for p in abstract.split("\n") if p.strip())
        new_block = f"> **Abstract:**\n> {formatted}\n"

    if "*Abstract not available.*" in content:
        content = content.replace("*Abstract not available.*", new_block)
    elif "*Proceedings volume.*" in content:
        content = content.replace("*Proceedings volume.*", new_block.strip())
    elif "*Preface.*" in content:
        content = content.replace("*Preface.*", new_block.strip())
    elif "> **Abstract:**" in content:
        content = re.sub(r'> \*\*Abstract:\*\*\s*\n(?:> .*\n?)+', lambda _: new_block, content)
    else:
        if "<details" in content:
            content = content.replace("<details", f"{new_block}\n<details", 1)
        else:
            content += f"\n{new_block}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def fetch_zenodo_abstract(doi):
    """Fetch description for Zenodo records."""
    m = re.search(r'zenodo\.([0-9]+)', doi, re.I)
    if not m:
        return ""
    rec_id = m.group(1)
    url = f"https://zenodo.org/api/records/{rec_id}"
    try:
        fetcher = ApiFetcher.get_instance()
        data = fetcher.get_json(url)
        if data:
            desc = data.get("metadata", {}).get("description", "")
            return clean_abstract_text(desc)
    except Exception:
        pass
    return ""

def fetch_acl_abstract(doi=None, title=None):
    """Fetch abstract from ACL Anthology."""
    if doi and "10.18653" in doi.lower():
        clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        acl_id = clean_doi.split("/")[-1].lower()
        url = f"https://aclanthology.org/{acl_id}.bib"
        try:
            fetcher = ApiFetcher.get_instance()
            text = fetcher.get_text(url)
            if text:
                m = re.search(r'abstract\s*=\s*"((?:[^"\\]|\\.)*)"', text)
                if m:
                    raw = m.group(1).encode('utf-8').decode('unicode_escape')
                    return clean_abstract_text(raw)
        except Exception:
            pass

    if title and "Treating Dialogue Quality Evaluation" in title:
        url = "https://aclanthology.org/2020.lrec-1.64.bib"
        try:
            fetcher = ApiFetcher.get_instance()
            text = fetcher.get_text(url)
            if text:
                m = re.search(r'abstract\s*=\s*"((?:[^"\\]|\\.)*)"', text)
                if m:
                    raw = m.group(1).encode('utf-8').decode('unicode_escape')
                    return clean_abstract_text(raw)
        except Exception:
            pass
    return ""

def fetch_openalex_abstract(title, doi=None):
    """Fetch complete abstract from OpenAlex API (polite pool)."""
    headers = {"User-Agent": "AIX-Publication-Crawler/1.0 (mailto:aix@leuphana.de)"}
    if doi:
        clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        url = f"https://api.openalex.org/works/doi:{clean_doi}?mailto=aix@leuphana.de"
        try:
            fetcher = ApiFetcher.get_instance()
            data = fetcher.get_json(url)
            if data:
                inv = data.get("abstract_inverted_index")
                if inv:
                    w_idx = []
                    for w, positions in inv.items():
                        for p in positions:
                            w_idx.append((p, w))
                    w_idx.sort()
                    text = " ".join(w for _, w in w_idx).strip()
                    if text:
                        return clean_abstract_text(text)
        except Exception:
            pass

    if title:
        words = [w for w in re.findall(r'[a-zA-Z0-9]+', title) if len(w) > 3][:6]
        if words:
            query = " ".join(words)
            url = f"https://api.openalex.org/works?filter=title.search:{requests.utils.quote(query)}&per-page=3&mailto=aix@leuphana.de"
            try:
                fetcher = ApiFetcher.get_instance()
                data = fetcher.get_json(url)
                if data:
                    for item in data.get("results", []):
                        inv = item.get("abstract_inverted_index")
                        if inv:
                            w_idx = []
                            for w, positions in inv.items():
                                for p in positions:
                                    w_idx.append((p, w))
                            w_idx.sort()
                            text = " ".join(w for _, w in w_idx).strip()
                            if text:
                                return clean_abstract_text(text)
            except Exception:
                pass
    return ""

def fetch_crossref_abstract(doi):
    """Fetch complete abstract from Crossref API."""
    if not doi:
        return ""
    clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
    url = f"https://api.crossref.org/works/{clean_doi}?mailto=aix@leuphana.de"
    try:
        fetcher = ApiFetcher.get_instance()
        data = fetcher.get_json(url)
        if data:
            raw = data.get("message", {}).get("abstract")
            if raw:
                return clean_abstract_text(raw)
    except Exception:
        pass
    return ""

s2_circuit_broken = False

def fetch_abstract_semanticscholar(title, doi=None):
    """Fetch complete abstract from Semantic Scholar API with circuit breaker."""
    global s2_circuit_broken
    if s2_circuit_broken:
        return ""
    fetcher = ApiFetcher.get_instance()

    def rate_limited():
        # Only a real rate limit disables the API for this run; "paper not found" (404) does not.
        global s2_circuit_broken
        if fetcher.last_status == 429:
            s2_circuit_broken = True
            log("Semantic Scholar rate limited; disabling for remainder of run.", "WARN")
            return True
        return False

    try:
        if doi:
            clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
            data = fetcher.get_json(f"https://api.semanticscholar.org/graph/v1/paper/{clean_doi}?fields=title,abstract")
            if rate_limited():
                return ""
            if data and data.get("abstract"):
                return clean_abstract_text(data["abstract"])

        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={requests.utils.quote(title)}&limit=1&fields=title,abstract"
        data = fetcher.get_json(url)
        if rate_limited():
            return ""
        results = (data or {}).get("data", [])
        if results and results[0].get("abstract"):
            return clean_abstract_text(results[0]["abstract"])
    except Exception as e:
        log(f"Semantic Scholar error for '{title[:40]}': {e}", "WARN")
    return ""

def fetch_abstract_fallback(title, doi=None):
    """Multi-tiered robust fallback abstract fetcher."""
    # 0. Curated abstracts for special challenge/workshop reports
    for k, text in CURATED_ABSTRACTS.items():
        if k.lower() in title.lower() or title.lower() in k.lower():
            return text

    # 1. Zenodo
    if doi and "zenodo" in doi.lower():
        ab = fetch_zenodo_abstract(doi)
        if ab and len(ab) > 40:
            return ab

    # 2. ACL Anthology
    ab = fetch_acl_abstract(doi, title)
    if ab and len(ab) > 60:
        return ab

    # (Springer abstracts come from OpenAlex/Crossref; publisher pages are not scraped.)

    # 4. OpenAlex (polite pool)
    ab = fetch_openalex_abstract(title, doi)
    if ab and len(ab) > 80:
        return ab

    # 5. Crossref
    if doi:
        ab = fetch_crossref_abstract(doi)
        if ab and len(ab) > 80:
            return ab

    # 6. Semantic Scholar (with circuit breaker)
    ab = fetch_abstract_semanticscholar(title, doi)
    if ab and len(ab) > 80:
        return ab

    return ""

# ─── Main ──────────────────────────────────────────────────

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    state = load_state()
    pubs_state = state.get("publications", {})

    # ── SYNC: Reconcile state with actual files ───────────
    log_header("SYNC — Reconciling state with existing files")
    stale_md_keys = [k for k in pubs_state.keys() if k.endswith(".md")]
    for k in stale_md_keys:
        del pubs_state[k]

    synced = 0
    for filename, info in list(pubs_state.items()):
        filepath = info.get("file", os.path.join(OUTPUT_DIR, f"{filename}.md"))
        if os.path.exists(filepath):
            cur_ab = extract_abstract_from_file(filepath)
            title = info.get("title", "")
            has_valid = bool(cur_ab) and not is_abstract_incomplete(cur_ab, title)
            if pubs_state[filename].get("has_abstract") != has_valid:
                pubs_state[filename]["has_abstract"] = has_valid
                synced += 1
    if synced or stale_md_keys:
        state["publications"] = pubs_state
        save_state(state)
        log(f"Synced {synced} files (and cleaned {len(stale_md_keys)} duplicate keys).")
    else:
        log("State is up to date.")

    # ── PHASE 1: DBLP ─────────────────────────────────────
    log_header("PHASE 1 — Fetch publications from DBLP")

    publications = fetch_dblp_publications()

    # Deduplicate and group by sanitized title to enforce priority: Conference > Journal > Archive
    groups = {}
    for pub in publications:
        title = pub.get("title")
        if not title: continue
        fn = sanitize_filename(title)
        if fn:
            groups.setdefault(fn, []).append(pub)

    best_pubs = []
    for fn, group in groups.items():
        best = None
        for p in group:
            if p.get("is_conference"):
                best = p
                break
        if not best:
            for p in group:
                if p.get("is_journal"):
                    best = p
                    break
        if not best:
            for p in group:
                if p.get("is_archive"):
                    best = p
                    break
        if not best:
            best = group[0]
        best_pubs.append(best)

    # Titles of the files already on disk, normalized. Older files were named from titles that
    # still contained HTML entities (&quot; &apos; &amp;), so file names alone miss duplicates.
    def title_key(value):
        return re.sub(r'[^a-z0-9]', '', html.unescape(html.unescape(value or "")).lower())
    existing_titles = {}
    for path in glob.glob(os.path.join(OUTPUT_DIR, "*.md")):
        with open(path, encoding="utf-8") as fh:
            m = re.search(r'^title:\s*"(.*)"\s*$', fh.read(), re.MULTILINE)
        if m:
            existing_titles[title_key(m.group(1).replace('\\"', '"'))] = path

    new_count = 0
    skipped = 0
    for pub in best_pubs:
        title = pub.get("title")
        if not title:
            continue

        filename = sanitize_filename(title)
        if not filename:
            continue

        filepath = os.path.join(OUTPUT_DIR, f"{filename}.md")
        if not os.path.exists(filepath) and title_key(title) in existing_titles:
            # Same paper under an older file name: keep using that file
            filepath = existing_titles[title_key(title)]
            filename = os.path.splitext(os.path.basename(filepath))[0]

        # Register in state if not tracked yet
        if filename not in pubs_state:
            pubs_state[filename] = {
                "title": title,
                "has_abstract": False,
                "file": filepath,
                "is_conference": pub.get("is_conference", False),
                "is_journal": pub.get("is_journal", False),
                "is_archive": pub.get("is_archive", False)
            }

        # Don't overwrite existing files
        if os.path.exists(filepath):
            skipped += 1
            continue

        enrich_from_crossref(pub)
        bibtex = build_dblp_bibtex(pub)
        generate_markdown(pub, bibtex, filepath, abstract="")
        log(f"+ {filename}.md")
        new_count += 1

    state["publications"] = pubs_state
    save_state(state)

    log_header("PHASE 1 — Summary")
    log_summary("New files created:", new_count)
    log_summary("Existing files skipped:", skipped)
    log_summary("Total publications tracked:", state["summary"]["total_publications"])
    log_summary("With abstract:", state["summary"]["with_abstract"])
    log_summary("Without abstract:", state["summary"]["without_abstract"])

    # ── PHASE 2: Abstract Fetching ─────────────────────────
    needs_abstract = {k: v for k, v in pubs_state.items() if not v.get("has_abstract")}

    if not needs_abstract:
        log_header("PHASE 2 — Abstract Fetching (skipped)")
        log("All publications marked as having abstracts in state. Proceeding to verification.")
    else:
        log_header(f"PHASE 2 — Fetch abstracts ({len(needs_abstract)} remaining)")

    enriched = 0

    for i, (filename, info) in enumerate(needs_abstract.items()):
        title = info.get("title", "")
        filepath = info.get("file", os.path.join(OUTPUT_DIR, f"{filename}.md"))

        progress = f"[{i+1}/{len(needs_abstract)}]"
        log(f"{progress} {title[:65]}...")

        if not os.path.exists(filepath):
            log(f"{progress} File missing, skipping.", "WARN")
            continue

        doi = extract_doi_from_file(filepath) or info.get("doi")
        # 1. Try the open APIs (Zenodo, ACL Anthology, OpenAlex, Crossref, Semantic Scholar)
        abstract = fetch_abstract_fallback(title, doi)
        if abstract and not is_abstract_incomplete(abstract, title):
            updated = set_or_update_abstract_in_file(filepath, abstract)
            if updated:
                pubs_state[filename]["has_abstract"] = True
                enriched += 1
                log(f"{progress} ✓ Abstract added via API")
                state["publications"] = pubs_state
                save_state(state)
                continue

        # 2. Check if proceedings / preface
        if any(title.lower().startswith(p) for p in ["proceedings of", "joint proceedings of", "preface"]):
            proc_note = "*Proceedings volume.*" if "proceedings" in title.lower() else "*Preface.*"
            set_or_update_abstract_in_file(filepath, proc_note)
            pubs_state[filename]["has_abstract"] = True
            enriched += 1
            log(f"{progress} ℹ Marked as proceedings volume / preface")
            state["publications"] = pubs_state
            save_state(state)
            continue

        log(f"{progress} ✗ No abstract found")

    state["publications"] = pubs_state
    save_state(state)

    if needs_abstract:
        log_header("PHASE 2 — Summary")
        log_summary("Abstracts added this run:", enriched)
        log_summary("Still missing:", len(needs_abstract) - enriched)
        log_summary("Total publications tracked:", state["summary"]["total_publications"])
        log_summary("With abstract:", state["summary"]["with_abstract"])
        log_summary("Without abstract:", state["summary"]["without_abstract"])
        log_summary("Last updated:", state["summary"]["last_updated"])
        print()

    # ── PHASE 3: Last-Layer Abstract Verification & Completeness Checker ──
    log_header("PHASE 3 — Last-Layer Abstract Verification (Checking all papers on disk)")

    phase3_upgraded = 0
    phase3_checked = 0

    existing_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.md")))
    log(f"Inspecting {len(existing_files)} publication files on disk for missing or incomplete abstracts...")

    for i, filepath in enumerate(existing_files):
        progress = f"[{i+1}/{len(existing_files)}]"
        fn = os.path.splitext(os.path.basename(filepath))[0]

        if fn not in pubs_state:
            pubs_state[fn] = {"file": filepath, "has_abstract": False}

        with open(filepath, "r", encoding="utf-8") as fp:
            content = fp.read()

        tm = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
        title = tm.group(1) if tm else fn
        pubs_state[fn]["title"] = title
        doi = extract_doi_from_file(filepath)

        current_abstract = extract_abstract_from_file(filepath)

        # Check if proceedings volume or preface
        if any(title.lower().startswith(p) for p in ["proceedings of", "joint proceedings of", "preface"]):
            if current_abstract not in ("*Proceedings volume.*", "*Preface.*"):
                proc_note = "*Proceedings volume.*" if "proceedings" in title.lower() else "*Preface.*"
                set_or_update_abstract_in_file(filepath, proc_note)
                pubs_state[fn]["has_abstract"] = True
                phase3_upgraded += 1
                log(f"{progress}   ℹ Marked as proceedings volume / preface: {title[:55]}...")
                state["publications"] = pubs_state
                save_state(state)
            continue

        # Check if the abstract is missing or cut off
        if is_abstract_incomplete(current_abstract, title):
            phase3_checked += 1
            log(f"{progress} Incomplete/missing abstract ({len(current_abstract)} chars): {title[:55]}...")

            full_abstract = fetch_abstract_fallback(title, doi)
            if full_abstract and (not is_abstract_incomplete(full_abstract, title) or len(full_abstract) > len(current_abstract)):
                updated = set_or_update_abstract_in_file(filepath, full_abstract)
                if updated:
                    pubs_state[fn]["has_abstract"] = True
                    phase3_upgraded += 1
                    log(f"{progress}   ✓ Upgraded to full abstract ({len(full_abstract)} chars)")
                    state["publications"] = pubs_state
                    save_state(state)
            else:
                log(f"{progress}   ✗ Full abstract not found via fallback APIs")

            time.sleep(0.2)

    state["publications"] = pubs_state
    save_state(state)

    log_header("PHASE 3 — Summary")
    log_summary("Incomplete abstracts inspected:", phase3_checked)
    log_summary("Abstracts upgraded to full text:", phase3_upgraded)
    log_summary("Total publications tracked:", state["summary"]["total_publications"])
    log_summary("With abstract:", state["summary"]["with_abstract"])
    log_summary("Without abstract:", state["summary"]["without_abstract"])
    log_summary("Last updated:", state["summary"]["last_updated"])
    print()

if __name__ == "__main__":
    try:
        main()
    finally:
        if ApiFetcher._instance:
            ApiFetcher.get_instance().close()