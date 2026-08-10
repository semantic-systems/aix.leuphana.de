import os
import sys
import json
import time
import random
import re
from datetime import datetime, timezone
import requests
from scholarly import scholarly

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

    state["summary"] = {
        "total_publications": total,
        "with_abstract": with_abstract,
        "without_abstract": without_abstract,
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
                    "type": info.get("type")
                }

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

# ─── Main ──────────────────────────────────────────────────

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    state = load_state()
    pubs_state = state.get("publications", {})

    # ── SYNC: Reconcile state with actual files ───────────
    log_header("SYNC — Reconciling state with existing files")
    synced = 0
    for filename, info in pubs_state.items():
        if info.get("has_abstract"):
            continue
        filepath = info.get("file", "")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if "*Abstract not available.*" not in content and "> **Abstract:**" in content:
                pubs_state[filename]["has_abstract"] = True
                synced += 1
    if synced:
        state["publications"] = pubs_state
        save_state(state)
        log(f"Synced {synced} files that already had abstracts.")
    else:
        log("State is up to date.")

    # ── PHASE 1: DBLP ─────────────────────────────────────
    log_header("PHASE 1 — Fetch publications from DBLP")

    publications = fetch_dblp_publications()

    new_count = 0
    skipped = 0
    for pub in publications:
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
                "file": filepath
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

    # ── PHASE 2: Google Scholar ───────────────────────────
    needs_abstract = {k: v for k, v in pubs_state.items() if not v.get("has_abstract")}

    if not needs_abstract:
        log_header("PHASE 2 — Google Scholar (skipped)")
        log("All publications already have abstracts. Nothing to do.")
        return

    log_header(f"PHASE 2 — Fetch abstracts from Google Scholar ({len(needs_abstract)} remaining)")

    enriched = 0

    for i, (filename, info) in enumerate(needs_abstract.items()):
        title = info["title"]
        filepath = info["file"]

        progress = f"[{i+1}/{len(needs_abstract)}]"
        log(f"{progress} {title[:65]}...")

        if not os.path.exists(filepath):
            log(f"{progress} File missing, skipping.", "WARN")
            continue

        abstract = fetch_abstract_scholarly(title)

        if abstract == "RATE_LIMITED":
            log(f"{progress} Rate limited by Google Scholar. Aborting Phase 2 early.", "WARN")
            break
        elif abstract:
            updated = update_abstract_in_file(filepath, abstract)
            if updated:
                pubs_state[filename]["has_abstract"] = True
                enriched += 1
                log(f"{progress} ✓ Abstract added")
                state["publications"] = pubs_state
                save_state(state)
        else:
            log(f"{progress} ✗ No abstract found")

        sleep_time = random.uniform(1, 5)
        log(f"{progress} Sleeping {sleep_time:.0f}s...")
        time.sleep(sleep_time)

    state["publications"] = pubs_state
    save_state(state)

    log_header("PHASE 2 — Summary")
    log_summary("Abstracts added this run:", enriched)
    log_summary("Still missing:", len(needs_abstract) - enriched)
    log_summary("Total publications tracked:", state["summary"]["total_publications"])
    log_summary("With abstract:", state["summary"]["with_abstract"])
    log_summary("Without abstract:", state["summary"]["without_abstract"])
    log_summary("Last updated:", state["summary"]["last_updated"])
    print()

if __name__ == "__main__":
    main()
