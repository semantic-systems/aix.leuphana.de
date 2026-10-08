# Team profiles

Each `_team/` file creates an individual page and a card on `/team/`. Use the [team template](../_team/template.md) for a new person. [Avatar Aang's example](../_team/avatar-aang.md) shows a complete page with a portrait, structured details, headings, lists, and links. It is a fictional example currently marked `published: true`, so it may appear on the team page until switched off; do not copy its character facts into a real profile.

## Add a person

1. Search `_team/` for an existing profile. Update it if the person is already listed.
2. Copy the template to `_team/first-name-last-name.md` using lowercase letters and hyphens.
3. Fill in the name, role, category, portrait, and a short biography. Keep `published: false` while drafting.
4. Add contact details only if the person has approved them for the public website.
5. Temporarily set `published: true` to preview `/team/` and the detail page locally. Return it to `false` if review is still pending; leave it `true` once approved.

## Front matter fields

| Field | Meaning | Display |
| --- | --- | --- |
| `layout` | `team_member` | Selects the profile layout. |
| `name` | Public display name. Keep spelling consistent in projects and papers. | Team card, page heading, automatic matching. |
| `title` | Position or academic title. | Subtitle on the profile page. |
| `job_category` | One of the categories below. | Group on `/team/`. |
| `image` | Portrait filename, such as `jane-doe.jpg`. | Team card and circular profile picture. |
| `published` | `false` while drafting; `true` to publish. | Publication control. |
| `permalink` | Optional fixed path such as `/team/jane-doe/`. | Keeps the profile URL stable. |
| `bio`, `research_interests` | Optional structured text and list. | Display them in the body with Liquid, as in the Aang example. |
| `email`, `website`, `github`, `linkedin`, `office` | Optional verified contact details. | Include them explicitly in the Markdown body if you want visitors to see them. |

The team page groups `head`, `office_management`, `technical_staff`, `researcher`, `student_assistant`, and `alumni`. Any other value appears under “Other Members”. Choose the category that reflects the person's current role. Do not put an academic title in `job_category`.

## Add a portrait

Copy the image to `assets/images/profile_photo/`. If the file is named `jane-doe.jpg`, write `image: "jane-doe.jpg"` in front matter. Do **not** put `/assets/images/...` in this field: the layout adds that folder. A square or nearly square photo works best because the profile picture is cropped to a circle. Use `blank.png` if there is no approved portrait. See [the full image guide](images.md).

## Write the page body

Below the second `---`, write a short “About” paragraph in clear language. Add headings such as `## Research interests`, `## Teaching`, and `## Contact` when there is useful information. Fields like `bio` and `email` do not appear automatically: write the text in the body or render the field with Liquid, for example `{{ page.bio }}` and `{{ page.email }}`. Remove empty headings and example contact addresses.

## Automatic project and paper links

The profile layout scans published projects' `project_members` and published papers' `authors` during each Jekyll build. Matching titles appear as links below the person's written profile. Match the full name consistently; the layout ignores a leading `Dr.` or `Prof. Dr.` in the team profile name. For example, `name: "Jane Doe"` matches `- name: "Jane Doe"` in a project and `- "Jane Doe"` in a publication. Initials, misspellings, or different surnames do not match automatically. Add the person to the project or publication record to create the link; do not hand-edit the generated list on the profile page.

The link checker assigns a team profile's own broken links to that profile's email address when present. To receive alerts for posts, projects, or papers the person maintains, assign the team profile filename stem as their owner ID. See [broken-link notifications](link-checker.md).

## Maintain and publish

Update the same file when a person changes role, portrait, office, or contact information. Check the person's preference before publishing personal data. If `name` changes, update matching project and publication records so automatic links still work. If the person leaves, move them to `alumni` if the group wants to retain the page, or set `published: false` if it should no longer be public. Preview both `/team/` and the detail page, then follow [the publishing steps](getting-started.md#publish-a-change).
