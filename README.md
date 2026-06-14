# AIX Research Group Website

This repository contains the source code for the AIX Research Group website, built using [Jekyll](https://jekyllrb.com/). 

## 🚀 Running the Website Locally

You can preview the website on your own computer before pushing changes to GitHub. The easiest way to run it is using Docker.

1. Open your terminal and navigate to this folder.
2. Run the following command:
   ```bash
   docker-compose up
   ```
3. Open your web browser and go to `http://localhost:4000`
4. The website will automatically update whenever you save a file!

---

## 📝 How to Add Content

The website is divided into four main sections: **News, Projects, Demos, and Publications**. 
To add new content, you just create a new Markdown (`.md`) file in the corresponding folder.

**To make it easy, there are TEMPLATE files in each folder!**
Instead of starting from scratch, simply copy the template, rename it, and fill in the blanks.

* `_posts/` -> News articles (Must be named `YYYY-MM-DD-title.md`)
* `_projects/` -> Research projects
* `_demos/` -> Interactive demos
* `_publications/` -> Published papers

---

## ⚠️ CRITICAL RULES & QUIRKS (Must Read)

Jekyll is powerful, but it has a few strict rules you need to follow. If your post isn't showing up, it is almost certainly because of one of these three reasons:

### 1. The "Future Dates" Rule
Jekyll has a built-in scheduling feature. **If a post has a date in the future, Jekyll will hide it.**
* If you set `date: 2099-01-01`, the post will physically not appear on the website until the year 2099.
* Always ensure your `date:` field is set to today's date or a past date if you want it to be visible immediately.

### 2. Sorting & Pagination
The main lists (News, Projects, Demos, Publications) are automatically sorted by **Date (Newest to Oldest)**.
* You **MUST** include a `date:` field in the front matter of every single `.md` file, formatted exactly like this: `YYYY-MM-DD` (e.g., `date: 2026-06-14`).
* If you do not include a date, the item will be thrown to the very bottom of the last page.
* To "pin" an item to the very top of the list, simply give it a date slightly in the future (but be careful, if it's a News post in `_posts`, Jekyll might hide it as explained above).

**How to change the number of items per page:**
By default, the website shows 10 items per page before generating a "Page 2". If you ever want to change this number, simply open the `_config.yml` file in the root directory, find the `pagination:` block, and change the `per_page: 10` value to whatever number you prefer!

### 3. Adding Images (Relative URLs)
When adding an image to an article, **never** use the absolute path from your computer (e.g. `C:/Users/...` or `/Users/user/...`). The web server cannot see your local hard drive!

Always put your images inside the `assets/images/` folder, and link to them using a **relative path**. 

**Standard Markdown Image:**
```markdown
![My Picture](/assets/images/my-picture.jpg)
```

**Beautifully Formatted HTML Image:**
(Use this if you want the image to be responsive, centered, and have a caption)
```html
<figure style="text-align: center; margin: 2rem 0;">
  <img src="{{ '/assets/images/my-picture.jpg' | relative_url }}" alt="Description" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  <figcaption style="font-size: 0.9rem; color: gray; margin-top: 0.5rem;">Your caption goes here</figcaption>
</figure>
```

---

## 🌐 Deployment & Publishing

The website is hosted on **GitHub Pages** using **GitHub Actions**. 

To publish your changes:
1. Make sure `published: true` is set in your post's front matter.
2. Commit your changes and push them to the `feature/site-redesign-and-pagination` branch (or `main` when you merge).
3. GitHub Actions will automatically detect the push, rebuild the website, and deploy it to `aix.leuphana.de`. You can watch the progress in the "Actions" tab on GitHub.
