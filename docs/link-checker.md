# Broken-link notifications

Every 24 hours, the crawler fetches publications, builds a fresh Jekyll site in its own temporary directory, and checks the links in that build. It sends **confirmed 404/410 links and DNS lookup failures found in a page's own source** to the people explicitly responsible for that page. A DNS lookup failure includes `net::ERR_NAME_NOT_RESOLVED`; the owner should check the URL and domain because the failure may be temporary. Admins receive a daily email listing only these broken links, including links supplied by shared layouts and pages with no owner. Other uncertain responses are logged but left out of the email. The script does not infer responsibility from the first project member or from a paper's authors.

Links whose host is `doi.org` or `linkedin.com` (including subdomains such as `www.linkedin.com` and `dx.doi.org`) are skipped entirely. These sites often reject automated checks; skipped links do not appear in owner or admin emails.

The checker compares each generated page with its Markdown source. If the source is newer than the HTML, or the HTML changes while a scan is running, that page is skipped. The admin email shows only the number of skipped pages and asks for a rebuild. It does not claim the full site is clean until every page is checked. Notification history for skipped pages is kept until a later scan of a fresh build. The daily crawler's fresh build should avoid stale pages; manual checks against `_site/` still require a recent build. If the crawler's Jekyll build fails, the checker does not run or send a clean result; inspect the crawler logs.

## Assign an owner

An owner is the filename stem of a profile in `_team/`. For example, `_team/jane-doe.md` has owner ID `jane-doe`. That profile must have a real `email` field in its YAML front matter. The email field is already used as contact information elsewhere on the site; do not insert an unapproved or placeholder address.

For a manually maintained post, project, demo, or publication, add:

```yaml
link_check_owner: "jane-doe"
```

For two people who both maintain the page, use a list instead:

```yaml
link_check_owners:
  - "jane-doe"
  - "alex-example"
```

Team profiles default to their own owner ID. Pages without a reachable owner remain in the admin summary. The owner's name is **not** taken from `author`, `authors`, or `project_members` because those fields describe contributors, not necessarily who updates the website.

## Assign owners to generated publications

The publication fetcher may rewrite `_publications/*.md`. Put persistent assignments in [`scripts/link_owners.yml`](../scripts/link_owners.yml) using the exact source path:

```yaml
pages:
  _publications/short-paper-title.md:
    - jane-doe
  _projects/example-project.md:
    - jane-doe
    - alex-example
```

The roster entry takes precedence over a front matter owner field. It is safe for it to contain only a few pages; the rest go to admins until owners are assigned. Update the roster when a filename changes or responsibility moves to someone else.
If one person truly maintains an entire collection, a wildcard key such as `_publications/*.md` can provide a default; specific file entries take precedence. Do not use a wildcard just because someone appears as an author on many papers.

## Configure admins and email

In the crawler's `.env`, set `SMTP_PASSWORD` and a comma-separated `LINK_CHECK_ADMIN_EMAILS`. The latter defaults to the current admin/test recipient if omitted; set it explicitly for the production admin list. The existing SMTP host, port, sender, and login are command-line defaults in the script and can be overridden with its CLI options. Keep secrets out of tracked files.

Admins receive one email per scan. It lists broken links, their routing, and any failed owner deliveries. If none are found and all pages were checked, it says “No broken links found right now.” If pages were skipped, it says the scan is incomplete and gives the count without listing every page. Owners receive one action email for new 404/410 or DNS lookup failures and, if the issue remains, a reminder after seven days. The reminder history lives in ignored `link_notification_state.json`; keep that file on the crawler's persistent volume to avoid repeated first-time alerts after restarts.

## Preview routing before sending

First review coverage without network requests:

```sh
python3 scripts/check_broken_links.py --ownership-report
```

For a manual check, build the site so `_site/` matches the current content and run from the repository root with the crawler's Python environment:

```sh
python3 scripts/check_broken_links.py --dry-run
```

This still performs network checks, but prints the proposed emails and does not send them or update reminder history. To limit a live run to one already assigned recipient, use `--test-only name@example.org`. The checker sends only to that address in this mode and does not update reminder history. Check the admin summary and owner assignments before enabling normal sends.

The daily crawler builds into `/tmp/aix-link-check-site` and passes that directory through `--site-dir`. The repository's GitHub Actions workflow deploys pushes to `main` and runs `docker compose up -d --build` on the VPS, so it rebuilds the crawler image automatically. The separate CI Jekyll build validates the site in GitHub Actions; the crawler still creates its own fresh build on the VPS before every link scan.

The daily crawler in `Dockerfile.crawler` already invokes this script. It needs a current `_site/` build to scan. If an owner is missing or has no usable email, the admin summary says why; add the correct team profile email or change the assignment, then review the next scan.
