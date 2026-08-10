---
layout: post
title: "REPLACE WITH TITLE: Short and catchy title for the news"
date: 2026-01-01 # Format exactly like this: YYYY-MM-DD. This controls sorting!
author: "Name of the Author"
categories: [news] # You can add more categories like [news, event, research]
thumbnail: "/assets/images/main_building_leuphana.png" # Square preview image for the main News list page
image: "/assets/images/Luftaufnahme_Leuphana_Universitaet_Lueneburg I.jpg" # Large banner image inside the actual post (optional)
excerpt: "A 1-2 sentence summary of this news that will show up as a preview on the main page."
published: false # Change this to 'true' when you want it to appear on the live website!
---

Write your news content here! 
You can use standard markdown syntax for **bold**, *italics*, and [links](https://example.com).

## Headings
Use two hashtags for a large section heading.

### Smaller Headings
Use three hashtags for smaller subsections.

**Images inside the text:**
If you just want a simple image, use markdown:

![Description of image](/assets/images/Redepult.jpg)

If you want a beautifully formatted image with dynamic width, height, and a caption, use this HTML block:

<figure style="text-align: center; margin: 2rem 0;">
  <img src="{{ '/assets/images/Redepult.jpg' | relative_url }}" alt="Description" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  <figcaption style="font-size: 0.9rem; color: gray; margin-top: 0.5rem;">Your caption goes here</figcaption>
</figure>

**Lists:**
- Bullet point 1
- Bullet point 2
