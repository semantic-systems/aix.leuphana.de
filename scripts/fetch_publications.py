import os
import sys
import json
import time
import random
import re
from datetime import datetime, timezone
import subprocess
import html
import requests
try:
    from scholarly import scholarly
except Exception as e:
    scholarly = None

DBLP_API_URL = "https://dblp.org/search/publ/api"
AUTHOR_QUERY = "author:Ricardo_Usbeck:"
OUTPUT_DIR = "_publications"
STATE_FILE = "_publications/.state.json"

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

def fetch_dblp_publications():
    """Fetch ALL publications from DBLP, paginating in batches of 100."""
    log("Querying DBLP API...")
    publications = []
    batch_size = 100
    offset = 0
    total = None

    while True:
        params = {
            "q": AUTHOR_QUERY,
            "format": "json",
            "h": batch_size,
            "f": offset
        }
        try:
            response = requests.get(DBLP_API_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            hits_obj = data.get("result", {}).get("hits", {})
            if total is None:
                total = int(hits_obj.get("@total", 0))
                log(f"DBLP reports {total} total publications.")

            hits = hits_obj.get("hit", [])
            if not hits:
                break

            for hit in hits:
                info = hit.get("info", {})
                pub = {
                    "key": info.get("key"),
                    "title": info.get("title", "").strip().rstrip('.'),
                    "year": info.get("year"),
                    "venue": info.get("venue"),
                    "doi": info.get("doi"),
                    "ee": info.get("ee"),
                    "type": info.get("type"),
                    "is_conference": False,
                    "is_journal": False,
                    "is_archive": False,
                }
                
                pub_type = info.get("type", "")
                venue = info.get("venue", "")
                if pub_type == "Conference and Workshop Papers":
                    pub["is_conference"] = True
                    if venue: pub["conference"] = venue
                elif pub_type == "Journal Articles":
                    pub["is_journal"] = True
                    if venue: pub["journal"] = venue
                elif "Informal" in pub_type:
                    pub["is_archive"] = True

                authors = info.get("authors", {}).get("author", [])
                if isinstance(authors, dict):
                    authors = [authors]
                pub["authors"] = [a.get("text") for a in authors if isinstance(a, dict) and "text" in a]

                publications.append(pub)

            offset += batch_size
            log(f"  Fetched batch: {len(publications)}/{total}")

            if offset >= total:
                break

        except Exception as e:
            log(f"DBLP request failed (offset={offset}): {e}", "ERROR")
            break

    log(f"DBLP fetch complete: {len(publications)} publications retrieved.")
    return publications

def fetch_dblp_bibtex(key):
    """Fetch BibTeX string directly from DBLP"""
    if not key:
        return ""
    try:
        bib_url = f"https://dblp.org/rec/{key}.bib"
        response = requests.get(bib_url, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        log(f"BibTeX fetch failed for {key}: {e}", "WARN")
    return ""

def fetch_abstract_scholarly(title):
    """Use scholarly to search Google Scholar and return the abstract."""
    if not scholarly:
        return ""
    try:
        search_query = scholarly.search_pubs(title)
        first_result = next(search_query, None)
        if first_result:
            return first_result.get('bib', {}).get('abstract', "")
        return ""
    except Exception as e:
        error_str = str(e)
        log(f"Google Scholar error: {error_str}", "WARN")
        if "Cannot Fetch from Google Scholar" in error_str or "MaxTriesExceededException" in error_str:
            return "RATE_LIMITED"
        return ""

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
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            desc = r.json().get("metadata", {}).get("description", "")
            return clean_abstract_text(desc)
    except Exception:
        pass
    return ""

def fetch_acl_abstract(doi=None, title=None):
    """Fetch abstract from ACL Anthology."""
    if doi and "10.18653" in doi.lower():
        clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
        acl_id = clean_doi.split("/")[-1].lower()
        url = f"https://aclanthology.org/{acl_id}/"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                m = re.search(r'abstract:\s*"((?:[^"\\]|\\.)*)"', r.text)
                if m:
                    raw = m.group(1).encode('utf-8').decode('unicode_escape')
                    return clean_abstract_text(raw)
        except Exception:
            pass

    if title and "Treating Dialogue Quality Evaluation" in title:
        url = "https://aclanthology.org/2020.lrec-1.64/"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                m = re.search(r'abstract:\s*"((?:[^"\\]|\\.)*)"', r.text)
                if m:
                    raw = m.group(1).encode('utf-8').decode('unicode_escape')
                    return clean_abstract_text(raw)
        except Exception:
            pass
    return ""

def fetch_springer_abstract(doi):
    """Fetch full abstract from SpringerLink metadata using curl."""
    if not doi:
        return ""
    clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
    if not (clean_doi.startswith("10.1007/") or clean_doi.startswith("10.1002/")):
        return ""
    
    # Try direct DOI resolution first (curl follows redirects automatically)
    urls = [f"https://doi.org/{clean_doi}"]
    for prefix in ["chapter", "article", "referenceworkentry"]:
        urls.append(f"https://link.springer.com/{prefix}/{clean_doi}")

    for url in urls:
        try:
            cmd = ["curl", "-sL", "--max-time", "10", url]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0 and ("application/ld+json" in res.stdout or "Abs1" in res.stdout):
                json_matches = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', res.stdout, re.DOTALL)
                for j in json_matches:
                    try:
                        data = json.loads(j)
                        desc = data.get("description") or data.get("mainEntity", {}).get("description")
                        if desc and len(desc) > 80:
                            return clean_abstract_text(desc)
                    except Exception:
                        pass
                m = re.search(r'<(?:section|div)[^>]*(?:id|aria-labelledby)=["\']Abs1[^"\']*["\'][^>]*>(.*?)</(?:section|div)>', res.stdout, re.DOTALL)
                if m:
                    clean = clean_abstract_text(m.group(1))
                    if len(clean) > 80:
                        return clean
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
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                inv = r.json().get("abstract_inverted_index")
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
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    for item in r.json().get("results", []):
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
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            raw = r.json().get("message", {}).get("abstract")
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
    headers = {"User-Agent": "AIX-Publication-Crawler/1.0 (mailto:aix@leuphana.de)"}
    try:
        if doi:
            clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
            url = f"https://api.semanticscholar.org/graph/v1/paper/{clean_doi}?fields=title,abstract"
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 429:
                s2_circuit_broken = True
                log("Semantic Scholar rate limited (429); disabling for remainder of run.", "WARN")
                return ""
            if resp.status_code == 200:
                abs_text = resp.json().get("abstract")
                if abs_text:
                    return clean_abstract_text(abs_text)

        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={requests.utils.quote(title)}&limit=1&fields=title,abstract"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 429:
            s2_circuit_broken = True
            log("Semantic Scholar rate limited (429); disabling for remainder of run.", "WARN")
            return ""
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            if data and data[0].get("abstract"):
                return clean_abstract_text(data[0].get("abstract"))
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

    # 3. SpringerLink (direct publisher metadata via curl)
    if doi and ("10.1007" in doi or "10.1002" in doi):
        ab = fetch_springer_abstract(doi)
        if ab and len(ab) > 80:
            return ab

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

        # Polite delay to avoid DBLP rate-limiting
        time.sleep(1)
        bibtex = fetch_dblp_bibtex(pub.get("key"))
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
    scholar_failures = 0

    for i, (filename, info) in enumerate(needs_abstract.items()):
        title = info.get("title", "")
        filepath = info.get("file", os.path.join(OUTPUT_DIR, f"{filename}.md"))

        progress = f"[{i+1}/{len(needs_abstract)}]"
        log(f"{progress} {title[:65]}...")

        if not os.path.exists(filepath):
            log(f"{progress} File missing, skipping.", "WARN")
            continue

        doi = extract_doi_from_file(filepath) or info.get("doi")
        # 1. First try fast, reliable fallback APIs (Springer, OpenAlex, ACL, Zenodo, Crossref)
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

        # 3. Fallback to Google Scholar if available and not failing
        if scholarly and scholar_failures < 3:
            abstract = fetch_abstract_scholarly(title)
            if abstract == "RATE_LIMITED":
                log(f"{progress} Rate limited by Google Scholar. Disabling Scholar for remainder.", "WARN")
                scholar_failures = 999
            elif abstract:
                updated = set_or_update_abstract_in_file(filepath, abstract)
                if updated:
                    pubs_state[filename]["has_abstract"] = True
                    enriched += 1
                    log(f"{progress} ✓ Abstract added via Scholar")
                    state["publications"] = pubs_state
                    save_state(state)
                time.sleep(random.uniform(1, 3))
            else:
                scholar_failures += 1
                log(f"{progress} ✗ No abstract found")
        else:
            log(f"{progress} ✗ Scholar skipped or unavailable")

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

    import glob
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
    main()