---
layout: demo
title: "REPLACE WITH TITLE: Name of the Interactive Demo"
date: 2099-01-01 # Format exactly like this: YYYY-MM-DD. This controls the sorting order (newest first)
demo_url: "https://your-demo-website.com" # The actual link where users can try the demo
thumbnail: "/assets/images/your-thumbnail-image.jpg" # Square preview image for the main Demos list
image: "/assets/images/your-screenshot.jpg" # A screenshot of the demo in action (optional)
excerpt: "A short 1-2 sentence summary explaining what this demo does."
published: false # Change this to 'true' when you want it to appear on the live website!
---

Write a short introduction explaining how the user should interact with the demo and what it demonstrates.

## Features
- Feature 1
- Feature 2

**Images inside the text:**
If you want a beautifully formatted image with dynamic width, height, and a caption, use this HTML block:

{% highlight html %}
<figure style="text-align: center; margin: 2rem 0;">
  <img src="{{ '/assets/images/your-image.jpg' | relative_url }}" alt="Description" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  <figcaption style="font-size: 0.9rem; color: gray; margin-top: 0.5rem;">Your caption goes here</figcaption>
</figure>
{% endhighlight %}
