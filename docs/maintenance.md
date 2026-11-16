# Maintenance

For admins. Content editing: [editing.md](editing.md).

## Local preview

| Method | Command | URL |
|---|---|---|
| Docker (recommended) | `docker compose up jekyll` | <http://localhost:4000> |
| Ruby 3.2 + Bundler | `bundle install` then `bundle exec jekyll serve` | <http://localhost:4000> |

- Restart after changing `_config.yml`.
- Show drafts: `bundle exec jekyll serve --unpublished`.
- Do not start the `crawler` service for previews.

## Deployment

Push to `main` → [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml):

| Job | Does |
|---|---|
| `test-python` | `pytest` |
| `build-jekyll` | `jekyll build` |
| `deploy` | SSH to the VM: `git reset --hard origin/main`, keep `.env`, build crawler image (`docker build --network host`), `docker compose down` + `up -d --no-build`, wait for `localhost:4000`, check all services run |

- Success in the log: `Site is up` and `All services running: crawler jekyll`. Any failure turns the run red.
- Server: `hpc-v-gondel.leuphana.de`, SSH port 575, `/opt/jekyll/aix.leuphana.de`; nginx in front of Jekyll (`:4000`). Docker access needs the `docker` group.
- Manual restart on the VM: `docker build --network host -f Dockerfile.crawler -t aixleuphanade-crawler . && docker compose up -d --no-build`.

| Secret (GitHub → Settings → Secrets → Actions) | Use |
|---|---|
| `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY` | Deploy login |
| `SMTP_PASSWORD` | Optional; replaces the `SMTP_PASSWORD` line in the server's `.env` on deploy |

## Never commit

| File | Why |
|---|---|
| `.env` | `SMTP_PASSWORD`, `LINK_CHECK_ADMIN_EMAILS`, optional `S2_API_KEY` |
| `link_cache.json`, `link_notification_state.json` | Link-checker runtime state |
| `_site/`, `.jekyll-cache/`, `*.pyc`, `.DS_Store`, `.idea/` | Build output / local files |

All are in `.gitignore`. Repository internals (`README.md`, `docs/`, `tests/`, Docker files) are excluded from the website in `_config.yml`.

## Crawler

`crawler` service, `scripts/run_daily_crawler.sh`, every 24 h:

1. `scripts/fetch_publications.py`: new DBLP papers → `_publications/`
2. Fresh Jekyll build → `/tmp/aix-link-check-site`
3. `scripts/check_broken_links.py --site-dir /tmp/aix-link-check-site`

Logs: `docker compose logs --tail 100 crawler`.

### Publication fetcher

| Step | Source |
|---|---|
| Publication list (incl. edited volumes) | DBLP SPARQL endpoint `sparql.dblp.org`, person `pid/65/9656` |
| BibTeX | Built from DBLP data + Crossref (venue, publisher, editors) |
| Abstracts | Zenodo, ACL Anthology `.bib`, OpenAlex, Crossref, Semantic Scholar (`S2_API_KEY` optional) |

- Honest user agent, ≥ 1 s between requests per host, backoff on 429/5xx. No browser automation, no scraping.
- Never overwrites an existing file; skips titles already on the site.
- Title-search results only with an exact (normalised) title match; citation lines rejected.
- Skips code releases (`SKIP_DBLP_KEYS`, titles `owner/repo - …`).
- New edited volumes → `is_proceedings`; DBLP data records → `is_dataset`.
- State: `_publications/.state.json` (do not edit by hand).

### Link checker

| Rule | |
|---|---|
| Emailed to page owners | HTTP 404/410 and DNS failures, only for links in the page's own source |
| Admin summary | Daily; all confirmed broken links, routing, delivery failures |
| Never emailed | Blocked/uncertain responses (401, 403, 429, timeouts, …) |
| Skipped entirely | `doi.org`, `linkedin.com` |
| Pages skipped | Source newer than built HTML (scan marked incomplete) |
| Reminder | After 7 days if still broken |

- Requests: honest user agent, ≥ 1 s per host (also for each redirect hop), HEAD then GET.
- SMTP: `sysmail.leuphana.de:587`, defaults in the script; password from `.env`.
- Admins: `LINK_CHECK_ADMIN_EMAILS` in `.env` (comma-separated).

Page owners (team file name without `.md`; the profile needs a real `email`):

| Where | Syntax |
|---|---|
| Front matter of a page | `link_check_owner: "jane-doe"` or `link_check_owners: ["jane-doe", "alex-example"]` |
| [`scripts/link_owners.yml`](../scripts/link_owners.yml) (wins; use for generated papers) | `pages:` → `_publications/file.md: [jane-doe]`; wildcards like `_publications/*.md` allowed |
| Team profiles | Own profile by default |

Not taken from `author`, `authors` or `project_members`.

| Command | Does |
|---|---|
| `python3 scripts/check_broken_links.py --ownership-report` | Owner coverage, no network |
| `python3 scripts/check_broken_links.py --dry-run` | Checks links, prints emails, sends nothing |
| `… --test-only name@leuphana.de` | Sends only to that address |
| `… --site-dir DIR` | Check another build (default `_site/`) |

## Scripts

| Script | Status |
|---|---|
| `run_daily_crawler.sh`, `fetch_publications.py`, `check_broken_links.py`, `link_owners.yml` | In use (crawler) |
| `test_smtp.py` | Manual SMTP test |

## Repository map

| Path | Content |
|---|---|
| `_config.yml` | Collections, permalinks, excludes, defaults |
| `_team`, `_posts`, `_projects`, `_demos`, `_publications` | Content |
| `_data/about.yml` | Group texts (About and Team pages) |
| `pages/` | Top-level pages (team, projects, legal, …) |
| `_layouts/`, `_includes/` | Templates |
| `assets/` | `main.scss`, `fonts/` (self-hosted Roboto), `images/`, `icons/` |
| `api/` | Search indexes (generated by Jekyll) |
| `tools/meeting-planner/` | Meeting Point Planner (self-hosted Leaflet in `lib/`) |
| `scripts/`, `tests/` | Crawler scripts and their tests |
