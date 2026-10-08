# Projects

Use a project page for a research activity with a clear goal, people, and timeline. See the [setup guide](getting-started.md) before editing and the [project template](../_projects/TEMPLATE-PROJECT.md) for a starting file.

## Add a project

1. Check `_projects/` and `/projects/` for an existing page. Update that page if the project already exists.
2. Copy the template to a short lowercase filename such as `_projects/example-knowledge-graph.md`.
3. Replace the example front matter and write a plain-language opening paragraph below the second `---`.
4. Keep `published: false` while drafting. Temporarily set it to `true` to preview the list card and detail page locally. Return it to `false` if review is still pending.

## Front matter fields

| Field | Meaning | Where it appears |
| --- | --- | --- |
| `layout` | `project` | Selects the detail layout. |
| `title` | Official project name or a clear public name. | Card, search, detail heading. |
| `date` | Start date in `YYYY-MM-DD` format. | List order and timeline. |
| `end_date` | Optional end date in the same format. | Timeline; omitted means “Present”. |
| `status` | For example `Ongoing` or `Completed`. | Card and detail page. |
| `excerpt` | One or two sentences about the goal and outcome. | Card and search results. |
| `thumbnail` | Site path to a card image or logo. | Project list and home cards. |
| `project_members` | People involved; see below. | Detail page, project search, member profiles. |
| `website`, `github_repo` | Verified public links. | Buttons or metadata on the detail page. |
| `funding_organization`, `participants` | Funder and partner organization names. | Detail page. |
| `links` | List of labeled URLs to videos, reports, or results. | Detail page buttons. |
| `published` | `false` for drafts, `true` when ready. | Publication control. |
| `link_check_owner` | Team profile filename stem for the person maintaining the page. | Broken-link alert routing. |

Use `project_members` as a YAML list. Each entry can be a name or an object with a role:

```yaml
project_members:
  - name: "Jane Doe"
    role: "Project lead"
  - name: "Alex Example"
```

Use the same full name as the person's team profile. This lets the detail page link to the profile and lets the profile automatically list the project. Project search checks both the title and member names. Partners such as universities belong in `participants`, not `project_members`.
The first project member is not automatically the page owner. Set `link_check_owner` separately, following the [notification guide](link-checker.md).

## Add images and write the page

Put the logo or photo in `assets/images/` or `assets/icons/`, then set `thumbnail: "/assets/images/example-project.jpg"`. The listing card uses that image. The current project detail layout does not create a banner from `image`; insert a meaningful picture in the body if it should appear there. See [the image guide](images.md).

Explain the problem, objectives, approach, partners, and concrete results. Use `##` headings and link to deliverables only when the URL works. Avoid internal project jargon without a short explanation.

## Maintain and publish

Update `status` and `end_date` when the project ends. Recheck members, funders, and external URLs as they change. Edit the existing file so the URL stays stable. Preview `/projects/`, search by the title and a member, and open the detail page. Finish with [the publishing steps](getting-started.md#publish-a-change).
