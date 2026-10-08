# Publications

The site contains one Markdown file per paper in `_publications/`. Many records come from `scripts/fetch_publications.py`, which reads DBLP and tracks its work in `_publications/.state.json`. Start with the [setup guide](getting-started.md) if you are new to editing the site.

## Check before adding

Search `/publications/` and `_publications/` for the paper title and DOI. If it already exists, correct that file rather than create a duplicate. If the paper is new and the publication fetcher is responsible for it, coordinate with whoever maintains the fetch process; generated metadata may be updated later. Review file changes after a fetch before committing them.

## Add a manual record

1. Copy the [publication template](../_publications/TEMPLATE-PUBLICATION.md) to `_publications/short-paper-title.md`.
2. Replace the example title, numeric year, authors, venue, abstract, and links. Keep `published: false` while preparing the entry.
3. Use the paper's actual metadata. Do not invent a DOI or use the template's sample DOI.
4. Temporarily set `published: true` to preview `/publications/` and the detail page locally. Return it to `false` if review is still pending; leave it `true` once approved.

## Front matter fields

| Field | Meaning | Display |
| --- | --- | --- |
| `layout` | `publication` | Selects the detail layout. |
| `title` | Exact publication title. | List, search, detail heading. |
| `year` | Four-digit number such as `2026`. | Sorting, list grouping, detail page. |
| `authors` | YAML list in the paper's author order. | List, search, detail page, linked team profiles. |
| `abstract` | Optional text summary. | Shown as a preview on the publication list when set. |
| `is_conference`, `is_journal`, `is_archive` | Boolean publication type flags. | Determines the venue label. |
| `conference`, `journal` | Venue name for the selected type. | List and detail page. |
| `doi`, `pdf` | Full verified URLs. | Paper and PDF buttons. |
| `github_repo`, `github_page`, `demo` | Optional code, project page, and demo URLs. | Buttons on the detail page. |
| `published` | `false` for a draft, `true` when ready. | Publication control. |
| `link_check_owner` | Maintainer's team profile filename stem for a manual record. | Broken-link alerts; generated papers should use the separate roster. |

Example author and type fields:

```yaml
year: 2026
authors:
  - "Jane Doe"
  - "Alex Example"
is_conference: true
is_journal: false
is_archive: false
conference: "Example Conference 2026"
```

For a journal article, set `is_journal: true`, set the other type flags to `false`, and use `journal` instead of `conference`. For a preprint, use `is_archive: true`. Keep author spelling consistent with team `name` fields. Publication search uses those names; matching names also add the paper automatically to team profiles.

## Abstract, body, and images

The list preview reads `abstract` from front matter. The detail page renders the Markdown body. Put a concise plain-language explanation, an abstract, or a link to the paper in the body. If you want an image, follow [the image guide](images.md) and include it in the body; the publication layout does not use a thumbnail. Link to an authorized PDF rather than uploading a copy without permission.

## Maintain and publish

Correct typos, broken DOI/PDF links, and metadata in the existing file. Because the fetch script also uses `_publications/.state.json`, inspect its state entry when modifying a generated record and check later generated changes for overwrites or duplicates. Avoid editing the state file casually. Preview the year grouping, search by title and author, and check the paper's detail page. Finish with [the publishing steps](getting-started.md#publish-a-change).
For a generated paper, assign its website maintainer in [`scripts/link_owners.yml`](../scripts/link_owners.yml) so the assignment survives a fetch. See [broken-link notifications](link-checker.md).
