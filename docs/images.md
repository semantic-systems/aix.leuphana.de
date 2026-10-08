# Add pictures and other images

## Choose the correct folder

| Use | Folder | Front matter value |
| --- | --- | --- |
| Team portrait | `assets/images/profile_photo/` | Filename only, such as `image: "jane-doe.jpg"` |
| News, project, or demo image | `assets/images/` or `assets/icons/` | Site path, such as `thumbnail: "/assets/images/workshop.jpg"` |
| Image inside a page body | `assets/images/` | Markdown or HTML/Liquid path shown below |

Copy the image file into the repository before referencing it. In a file browser, open this project folder, navigate to the destination above, and drag or paste the picture there. Use a descriptive lowercase filename with hyphens, keep the original extension (`.jpg`, `.jpeg`, `.png`, `.webp`, or `.svg` as appropriate), and check that you are allowed to publish it. A portrait around 600–1000 pixels square and a banner around 1200–1800 pixels wide are usually enough; preserve the aspect ratio when resizing. Avoid spaces and multi-megabyte files where possible. Do not use local computer paths such as `/Users/...` or `C:\...` in content. Remove location or other private metadata from photos if needed before publishing.

## Team portrait

Put `jane-doe.jpg` in `assets/images/profile_photo/`, then set:

```yaml
image: "jane-doe.jpg"
```

Use only the filename here. The team layout adds the directory automatically and displays a circular crop on the profile page. The team list also uses this image. Check that the face stays visible after cropping. If no portrait is available, set `image: "blank.png"`.

## News images

Use `thumbnail` for the news list and home card. Use `image` for the large image near the top of the news detail page:

```yaml
thumbnail: "/assets/images/workshop-card.jpg"
image: "/assets/images/workshop-wide.jpg"
```

If only one image exists, both fields can use the same path. If neither is set, list cards use the site logo. The detail page displays a large image only when `image` is set.

## Project and demo images

Set `thumbnail` for the listing card and home card:

```yaml
thumbnail: "/assets/images/project-diagram.png"
```

The cards fall back to `image` and then the AIX logo. The current project and demo detail layouts do **not** automatically display `image` as a banner. If the detail page needs a picture, insert it in the Markdown body. Logos may fit better with optional `thumbnail_size: "65%"`; ordinary photos usually do not need that setting.

## Image inside the page body

Use descriptive alternative text. A simple Markdown image is enough in most cases:

```md
![A researcher presenting a project diagram]({{ '/assets/images/project-diagram.png' | relative_url }})
```

For a visible caption, use a figure:

```html
<figure>
  <img src="{{ '/assets/images/project-diagram.png' | relative_url }}" alt="Diagram showing the three stages of the project" style="max-width: 100%; height: auto;">
  <figcaption>Three stages of the project workflow.</figcaption>
</figure>
```

Describe the image's meaning in `alt`, not just its filename. For a purely decorative image, use `alt=""`. Check the image in the local preview and commit the asset with the content file. Publication records generally link to the paper PDF rather than upload and display a cover image.
