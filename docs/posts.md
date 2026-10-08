# News posts

Use news posts for announcements, events, releases, and other dated updates. Start with the [setup guide](getting-started.md) if you have not previewed the site before.

## Add a post

1. Copy the [news template](../_posts/2099-01-01-TEMPLATE-NEWS.md) to a new file such as `_posts/2026-10-02-new-dataset.md`. Do not modify the template itself.
2. Replace the example title, author, date, summary, and body. The filename date and front matter `date` should match. Jekyll does not show future dated posts until that date.
3. Keep `published: false` while writing. Temporarily set it to `true` to preview locally, then return it to `false` if the post is still a draft.
4. Add images using [the image instructions](images.md). Preview the card at `/news/` and the full article; leave `published: true` only when approved.

## Front matter fields

| Field | What to write | Where it appears |
| --- | --- | --- |
| `layout` | `post` | Selects the news detail layout. |
| `title` | A specific, short headline. | News list, home card, article heading. |
| `date` | `YYYY-MM-DD`, matching the filename. | List order and visible article date. |
| `author` | Contributor's display name. | Article byline. |
| `excerpt` | One or two sentences that make sense alone. | News list and home card. |
| `thumbnail` | `/assets/images/...` or `/assets/logo.svg`. | List and home card. |
| `image` | Optional wide image path. | Large image on the detail page. |
| `categories` | Optional YAML list, for example `[news, event]`. | Metadata; current news layout does not display it. |
| `published` | `false` during drafting, then `true`. | Controls whether Jekyll publishes it. |
| `link_check_owner` | Team profile filename stem of the page maintainer. | Broken-link alerts; separate from the displayed author. |

## Write the article

Begin with the key information: what happened, who was involved, when it happened, and why a visitor should care. Use `##` headings for details, a clear call to action if relevant, and links to the actual event, paper, or project. Add a descriptive `alt` text to every meaningful image. Avoid copying a press release without checking names, dates, and permissions.

## Maintain and publish

Update the existing file when facts or links change. Keep the original publication date unless it was wrong; changing the filename changes the post URL. If an event is over, update the article with results or a recap instead of silently changing its date. Preview `/news/`, the detail page, and mobile width; then follow [the publishing steps](getting-started.md#publish-a-change).
