# Editing the website

For everyone who updates content. Everything works in the browser on GitHub; no installation needed.
Technical setup, deployment and the crawler: [maintenance.md](maintenance.md).

## Workflow

1. Be a member of the `website-editors` team in the `semantic-systems` organization (ask a website admin).
2. Open the file → pencil icon (**Edit this file**). New file: **Add file → Create new file**. Image: **Add file → Upload files**.
3. **Commit changes…** → **Create a new branch … and start a pull request** → **Propose changes** → **Create pull request**.
4. Another website editor approves (content folders) or a website admin (everything else); tests and site build must pass. Then merge. The site updates within ~5 minutes.

## Rules for every file

| Rule | Example |
|---|---|
| File names: lowercase, hyphens, no spaces or umlauts | `jane-doe.md` |
| Top part between the two `---` lines: `field: "value"`, keep the quotes, spaces not tabs | `title: "Researcher"` |
| Bottom part below the second `---`: page text (Markdown) | |
| `published: false` hides a page; `true` publishes it | |
| No example values left in published pages | `example.org`, `First Last` |
| Dates `YYYY-MM-DD`, publication `year` four digits | `2026-12-01`, `2026` |

Markdown: `## Heading` · `**bold**` · `[text](https://…)` · `- list item` · `![description](/assets/images/file.jpg)`

## Content types

| Content | Folder | Template | File name |
|---|---|---|---|
| Team profile | `_team` | `template.md` | `first-last.md` |
| News | `_posts` | `2099-01-01-TEMPLATE-NEWS.md` | `2026-12-01-short-title.md` |
| Project | `_projects` | `TEMPLATE-PROJECT.md` | `short-name.md` |
| Demo | `_demos` | `TEMPLATE-DEMO.md` | `short-name.md` |
| Publication | `_publications` | `TEMPLATE-PUBLICATION.md` | `short-paper-title.md` |

New item: open the template → copy all text → create the new file → replace every value. Never edit a template itself.

### Team profile

| Field | Value |
|---|---|
| `name` | Display name; must match the spelling in projects and papers (`Dr.`/`Prof. Dr.` ignored) |
| `title` | Position, e.g. `"Research Associate"` |
| `image` | Photo file name only, e.g. `"jane-doe.jpg"`; `"blank.png"` if none |
| `job_category` | `head`, `office_management`, `technical_staff`, `researcher`, `student_assistant`, `alumni` |
| `alumni_note` | Alumni only, optional: `"now at TU Berlin"` |
| `email` | Optional; only with the person's consent. Used for broken-link alerts, not shown automatically |
| `permalink` | Keep as is (`/team/first-last/`) |

- Page text: replace "Profile details coming soon." Contact details appear only if written in the text.
- Projects and papers with a matching name are listed on the profile automatically.
- Leaving the group: `job_category: "alumni"` (optionally `alumni_note`), or `published: false`.

### News

| Field | Value |
|---|---|
| `title` | Short headline |
| `date` | Same date as in the file name; future dates stay hidden until that day |
| `author` | Display name |
| `excerpt` | 1–2 sentences for the news list and home page |
| `thumbnail` | Card image, e.g. `"/assets/images/event.jpg"`; default `"/assets/logo.svg"` |
| `image` | Optional large image on the article page |
| `link_check_owner` | Maintainer's team file name without `.md` |

Changing the file name changes the URL.

### Project

| Field | Value |
|---|---|
| `title`, `excerpt` | Name; 1–2 sentences on goal and outcome |
| `date`, `end_date` | Start; end (empty = "Present") |
| `status` | `"Ongoing"` or `"Completed"` |
| `thumbnail` | Card image or logo; optional `thumbnail_size: "65%"` for logos |
| `project_members` | List; `- name: "Jane Doe"` with optional `role: "Project lead"`; names as in team profiles |
| `participants`, `funding_organization` | Partner organisations; funder |
| `website`, `github_repo`, `links` | Verified links |
| `link_check_owner` | Maintainer's team file name |

When a project ends: set `status: "Completed"` and `end_date`.

### Demo

| Field | Value |
|---|---|
| `title`, `excerpt`, `date` | Name; 1–2 sentences; launch date |
| `demo_url` | Link for the "Launch Demo" button |
| `thumbnail` | Screenshot or logo |
| `link_check_owner` | Maintainer's team file name |

Demo offline → update the page or set `published: false`.

### Publication

- Papers on DBLP are added automatically once a day. Add by hand only if missing there; search `/publications/` first.
- Preprints stay separate from the published version.
- Code releases are not publications: add the repository to the paper as `github_repo`.

| Field | Value |
|---|---|
| `title`, `year` | Exact title; four-digit year |
| `authors` | List in paper order; editors for proceedings |
| Type (one `true`) | `is_conference` + `conference`, `is_journal` + `journal`, `is_archive` (preprint), `is_proceedings` + `proceedings`, `is_dataset` + `dataset`, `is_thesis` + `thesis` |
| `doi`, `pdf` | Full URLs → "Paper" / "PDF" buttons |
| `github_repo`, `github_page`, `demo` | Optional buttons |
| `link`, `link_label` | Any other URL and its button text (default "Website") |

Page text: abstract as `> **Abstract:**` followed by `> text`. Generated files are never overwritten by the fetcher; corrections are safe.

## Images

| Use | Folder | Field value |
|---|---|---|
| Team photo (square, ~600 × 600 px) | `assets/images/profile_photo/` | `image: "jane-doe.jpg"` (file name only) |
| News/project/demo card (~1200–1800 px wide) | `assets/images/` | `thumbnail: "/assets/images/file.jpg"` |
| Image in page text | `assets/images/` | `![what it shows](/assets/images/file.jpg)` |

- Only images you may publish; JPG/PNG/WebP/SVG; no multi-megabyte files.
- Always describe the image (`alt` text); decorative images: empty description.
- Project and demo pages show no banner automatically; put the image in the page text.

## Something doesn't show up

- Waited 5 minutes after the merge?
- `published: true`?
- File name and date follow the rules?
- Quotes in the top part complete?
- Still missing → ask a website admin.
