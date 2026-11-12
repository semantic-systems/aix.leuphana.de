# How to edit the AIX website

You can change the website in your browser on GitHub. You don't need to install anything. Every change is checked by a website admin before it goes live.

You need a GitHub account with access to the repository [semantic-systems/aix.leuphana.de](https://github.com/semantic-systems/aix.leuphana.de). Ask a website admin if you don't have access.

## How a change goes live

1. You edit a file on GitHub and save it as a **pull request** (a change proposal).
2. An admin looks at it and merges it.
3. The website updates by itself, usually within 5 minutes.

## Update your profile

1. Open the repository on GitHub and click the folder **`_team`**.
2. Click your file, for example `jane-doe.md`.
3. Click the **pencil icon** (top right, "Edit this file").
4. Change what you need (see below).
5. Click **Commit changes…**, choose **Create a new branch for this commit and start a pull request**, then click **Propose changes** and **Create pull request**.

A profile file has two parts.

**The top part**, between the two `---` lines, holds the basic details. Keep the format `field: "value"`, including the quotation marks:

| Field | What to write |
|---|---|
| `name` | Your name as it should appear, e.g. `"Dr. Jane Doe"` |
| `title` | Your position, e.g. `"Research Associate"` |
| `image` | The file name of your photo, e.g. `"jane-doe.jpg"` (see below) |
| `job_category` | Your group on the team page: `head`, `office_management`, `technical_staff`, `researcher`, `student_assistant` or `alumni` |
| `alumni_note` | Only for alumni, optional: a short line such as `"now at TU Berlin"` |

**The bottom part**, below the second `---`, is the text of your page. Replace "Profile details coming soon." with a few sentences about yourself and your research. If you want people to contact you, write your email address in the *Contact* section. Contact details only appear if you write them there.

Simple formatting:

- `## Heading` makes a heading
- `**bold**` makes **bold** text
- `[link text](https://example.org)` makes a link
- a line starting with `- ` makes a list item

### Add or change your photo

1. Go to the folder **`assets/images/profile_photo`**.
2. Click **Add file → Upload files** and upload your photo. Use a square JPG or PNG, about 600 × 600 pixels, named like `jane-doe.jpg`.
3. Commit it in the same way as above, as a pull request.
4. In your profile, set `image: "jane-doe.jpg"`. Write only the file name, not the folder.

### When you leave the group

Set `job_category: "alumni"`. If you like, add `alumni_note: "now at …"`. Your profile then moves to the *Alumni* section of the team page.

## Publish other content

For each type of content there is a template. Open it, copy all of its text, create a new file in the same folder (**Add file → Create new file**), paste the text and replace the example values.

| Content | Folder | Template | File name |
|---|---|---|---|
| News | `_posts` | `2099-01-01-TEMPLATE-NEWS.md` | `2026-12-01-short-title.md` (date first) |
| Project | `_projects` | `TEMPLATE-PROJECT.md` | `short-project-name.md` |
| Demo | `_demos` | `TEMPLATE-DEMO.md` | `short-demo-name.md` |
| Publication | `_publications` | `TEMPLATE-PUBLICATION.md` | `short-paper-title.md` |

Things to know:

- File names use lowercase letters and hyphens only, no spaces or umlauts.
- `published: false` keeps a page hidden. Set it to `published: true` when the page is ready.
- For news, the date in the file name and the `date:` field must match, and must not be in the future.
- Publications listed on DBLP are added automatically once a day. Only add a publication by hand if it is not on DBLP. Before you do, search the publications page to make sure it isn't there already.
- Images for news, projects and demos go into `assets/images`. Link them as `/assets/images/file-name.jpg`.

## If something doesn't show up

Wait 5 minutes after the merge and reload the page. If it's still missing, check that `published: true` is set, that the file name follows the rules above, and that the quotation marks in the top part are complete. If that doesn't help, ask a website admin.

The other guides in this folder cover the same topics for technical maintainers, in more detail.
