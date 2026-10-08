# Demos

Use a demo page when visitors can try or view a research system. See the [setup guide](getting-started.md) and start from the [demo template](../_demos/TEMPLATE-DEMO.md).

## Add a demo

1. Check whether the demo already has a page in `_demos/`.
2. Copy the template to `_demos/short-demo-name.md` and replace the sample values.
3. Keep `published: false` while checking the live demo URL and instructions.
4. Temporarily set `published: true` to preview `/demos/` and the detail page locally. Return it to `false` if review is still pending; leave it `true` once approved.

## Front matter fields

| Field | Meaning | Display |
| --- | --- | --- |
| `layout` | `demo` | Selects the demo detail layout. |
| `title` | What the demo is called. | List, home card, detail heading. |
| `date` | Release or launch date in `YYYY-MM-DD`. | Controls list order. |
| `demo_url` | Full link where visitors can use it. | “Launch Demo” button. |
| `excerpt` | One or two sentences describing the experience. | List and home cards. |
| `thumbnail` | Site path to an image or logo. | List and home cards. |
| `published` | `false` for drafts, `true` when ready. | Publication control. |
| `link_check_owner` | Team profile filename stem of the demo page maintainer. | Broken-link alerts. |

Put the screenshot or logo in `assets/images/` or `assets/icons/`, then set `thumbnail: "/assets/images/demo-screenshot.png"`. The detail layout does not automatically display a banner image; insert one in the body if useful. See [the image guide](images.md).

## Write, maintain, and publish

Explain the purpose, first step, expected result, and any account or browser requirements. If the demo is unavailable, update the page or set it to unpublished rather than leaving a broken launch button. Recheck the external URL periodically. Preview the card and button, then follow [the publishing steps](getting-started.md#publish-a-change).
