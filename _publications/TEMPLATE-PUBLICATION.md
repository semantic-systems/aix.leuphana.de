---
layout: publication
title: "REPLACE WITH TITLE: Exact Title of the Research Paper"
date: 2099-01-01 # Format exactly like this: YYYY-MM-DD. Controls sorting (newest first) AND represents the publication date
authors: "Author One, Author Two, Ricardo Usbeck"
conference: "Name of the Conference or Journal (e.g. ACL 2026)"
pdf_url: "https://arxiv.org/pdf/XXXX.XXXXX" # Direct link to the PDF
code_url: "https://github.com/semantic-systems/your-repo" # Link to your GitHub code (optional)
data_url: "https://zenodo.org/record/XXXX" # Link to your dataset (optional)
thumbnail: "/assets/images/your-thumbnail-image.jpg" # Optional preview image
published: false # Change this to 'true' when you want it to appear on the live website!
---

### Abstract
Paste the full abstract of the paper here. 

### Citation
```bibtex
@inproceedings{your_citation_key,
  title={Your Paper Title},
  author={One, Author and Two, Author and Usbeck, Ricardo},
  booktitle={Proceedings of the Conference},
  year={2026}
}
```
(Replace the bibtex block above with your actual citation)

**Images inside the text:**
If you want a beautifully formatted image with dynamic width, height, and a caption, use this HTML block:

{% highlight html %}
<figure style="text-align: center; margin: 2rem 0;">
  <img src="{{ '/assets/images/your-image.jpg' | relative_url }}" alt="Description" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  <figcaption style="font-size: 0.9rem; color: gray; margin-top: 0.5rem;">Your caption goes here</figcaption>
</figure>
{% endhighlight %}
