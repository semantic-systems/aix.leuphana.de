# AIX Research Group website

The source for [aix.leuphana.de](https://aix.leuphana.de), built with Jekyll. Markdown files provide the content; Jekyll turns them into a static website.

## Preview locally

1. Install Docker with Compose.
2. Run `docker compose up jekyll` from this directory.
3. Open <http://localhost:4000>. Stop the preview with Ctrl+C.

For installation, images, draft workflow, and publishing, follow the [complete setup and editing guide](docs/getting-started.md). The optional `crawler` service fetches publications and checks links; it is not needed for routine editing.

Page maintainers and admins can configure link alerts using the [broken-link notification guide](docs/link-checker.md).

## Content guides

| Content | Source | Guide | Template |
| --- | --- | --- | --- |
| News posts | `_posts/` | [Posts](docs/posts.md) | [News example](_posts/2099-01-01-TEMPLATE-NEWS.md) |
| Projects | `_projects/` | [Projects](docs/projects.md) | [Project example](_projects/TEMPLATE-PROJECT.md) |
| Publications | `_publications/` | [Publications](docs/publications.md) | [Publication example](_publications/TEMPLATE-PUBLICATION.md) |
| Team profiles | `_team/` | [Team](docs/team.md) | [Team example](_team/template.md) |
| Demos | `_demos/` | [Demos](docs/demos.md) | [Demo example](_demos/TEMPLATE-DEMO.md) |

Start from a template, replace every example value, and follow the matching guide. See [images and portraits](docs/images.md) before adding pictures. Use short lowercase filenames with hyphens and keep `published: false` on drafts.

Before publishing, preview the list and detail page, check links and image descriptions, and confirm search finds publications by title or author and projects by title or project member. Set `published: true` when the content is ready. Pushing to `main` triggers the configured GitHub Actions checks and VPS deployment; see the [publishing steps](docs/getting-started.md#publish-a-change).

## Repository map

`_config.yml` defines collections, permalinks, and pagination. `pages/` defines top-level routes. `_layouts/` and `_includes/` render pages. `assets/` contains styles and images. `api/` contains generated search indexes. `scripts/` contains publication ingestion and maintenance utilities.
