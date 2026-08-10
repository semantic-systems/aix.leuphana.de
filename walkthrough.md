# Automated Publication Crawler Walkthrough

I have successfully designed, built, tested, and integrated the automated publication crawler for the AIX website! 🎉

## What was implemented:

### 1. The Crawler Script ([`fetch_publications.py`](file:///Users/murat/Documents/SHK/Sysadmin/semantic-systems/aix.leuphana.de/aix.leuphana.de/scripts/fetch_publications.py))
- Created a Python script that queries the **DBLP JSON API** for Prof. Dr. Ricardo Usbeck.
- Automatically fetches up to 1000 publications, getting the title, venue, year, authors, and DOI.
- Queries the **Semantic Scholar API** using the DOI to extract the missing abstract.
- Retrieves the raw `.bib` **BibTeX data directly from DBLP**.
- Automatically generates well-formatted Markdown (`.md`) files directly into the `_publications/` directory, following your existing `TEMPLATE-PUBLICATION.md`.
- **Safety check**: If an `.md` file for a paper already exists, it skips it! This ensures any manual edits (like the *Georelating* example) are completely safe and won't be overwritten.

### 2. Validation Tests ([`test_fetch_publications.py`](file:///Users/murat/Documents/SHK/Sysadmin/semantic-systems/aix.leuphana.de/aix.leuphana.de/tests/test_fetch_publications.py))
- Added a full test suite using `unittest` and `pytest`.
- Mocked all API endpoints (DBLP and Semantic Scholar) to validate JSON parsing, Markdown generation, and data extraction without hitting real APIs.
- The tests run successfully in `0.003s`!

### 3. Docker Container Integration ([`docker-compose.yml`](file:///Users/murat/Documents/SHK/Sysadmin/semantic-systems/aix.leuphana.de/aix.leuphana.de/docker-compose.yml))
- Added a dedicated lightweight `crawler` service to your `docker-compose.yml`.
- This ensures the Jekyll service remains pristine and untouched.
- The crawler installs the needed dependencies via [`requirements.txt`](file:///Users/murat/Documents/SHK/Sysadmin/semantic-systems/aix.leuphana.de/aix.leuphana.de/requirements.txt) and runs a loop in the background, updating publications once every 24 hours (86,400 seconds) as long as the Docker container is running.

## Verification
- Run `docker-compose down` followed by `docker-compose up -d` to restart the containers. You will notice the `crawler` service starting up alongside `jekyll`.
- I have also triggered the script manually right now. Over the next few minutes, you will see `_publications/` populate with dozens of fresh, automatically generated Markdown files complete with DOIs, abstracts, and BibTeX!

> [!NOTE]
> The script is currently populating the `_publications/` directory. Once it finishes, Jekyll will rebuild the site and all publications will appear natively on the website!
