# Automated Publication Crawler Implementation

This plan outlines the design and integration of a script to automatically fetch publications for the AIX research group using the DBLP and Semantic Scholar APIs, generate Jekyll `.md` files, and run periodically in Docker.

## User Review Required

> [!IMPORTANT]
> **Docker Service Addition**: Instead of modifying the `jekyll-serve` image to install Python and configure cron (which can be messy and break the web server environment), I propose adding a new `crawler` service to `docker-compose.yml`. This service will use a lightweight Python image, run the script periodically, and share the `_publications/` folder with the Jekyll service. Does this approach work for you?

## Open Questions

> [!WARNING]
> **DBLP Author ID**: Currently, the script uses the DBLP author ID `165/1589` or the string query `"Ricardo_Usbeck"`. Should we hardcode this, or would you like to maintain a list of author names in a config file to fetch publications for the entire team?

## Proposed Changes

---

### Scripts Component

#### [NEW] `scripts/fetch_publications.py`
A Python script that will:
1. **Query DBLP API**: Use `https://dblp.org/search/publ/api?q=author:Ricardo_Usbeck:&format=json` (DBLP natively supports JSON output!).
2. **Extract DOIs**: Parse the JSON response to get DOIs, titles, venue, authors, and year.
3. **Fetch Abstracts**: Query the Semantic Scholar API using the DOI (`https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=abstract`) to get the missing abstract.
4. **Generate Markdown**: Output a `.md` file for each publication in the `_publications/` directory following the `TEMPLATE-PUBLICATION.md` format. It will skip generating files if they already exist, allowing authors to manually update files safely.

#### [NEW] `requirements.txt`
Dependencies for the Python script:
- `requests` (for API calls)
- `pytest` (for running the validation tests)

---

### Testing Component

#### [NEW] `tests/test_fetch_publications.py`
A test suite (using `unittest` or `pytest`) that will:
1. Validate that the script correctly parses the DBLP JSON response structure.
2. Validate that Semantic Scholar DOI lookup correctly extracts abstracts.
3. Evaluate the Markdown generation function to ensure front matter is properly formatted, DOIs are included, and special characters in titles don't break the YAML.

---

### Docker Configuration

#### [MODIFY] `docker-compose.yml`
Add a new service `publications-crawler`:
```yaml
services:
  jekyll:
    image: bretfisher/jekyll-serve
    volumes:
      - .:/site
    ports:
      - "4000:4000"
  crawler:
    image: python:3.11-slim
    volumes:
      - .:/site
    working_dir: /site
    command: /bin/bash -c "pip install -r requirements.txt && while true; do python3 scripts/fetch_publications.py; sleep 86400; done"
```
*This will run the crawler once every 24 hours (86400 seconds) in the background while the Docker container is up.*

---

## Verification Plan

### Automated Tests
- Run `pytest tests/test_fetch_publications.py` to ensure the logic and JSON parsing work securely.

### Manual Verification
- Run `docker-compose up` and verify that the `crawler` service starts, fetches data, and creates `.md` files in `_publications/`.
- Verify the generated publication `.md` files appear correctly on `http://localhost:4000/publications/` and have working DOIs.
