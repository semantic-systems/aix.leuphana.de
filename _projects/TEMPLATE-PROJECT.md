---
layout: project
title: "REPLACE WITH TITLE: Name of the Project"
date: 2024-01-01 # Start date of the project (Format: YYYY-MM-DD). This also controls the sorting order.
end_date: "2026-12-31" # Optional. End date of the project. If empty or removed, it will display as "Present".
status: "Ongoing" # e.g. "Ongoing", "Completed", "In Review"
thumbnail: "/assets/images/your-thumbnail-image.jpg" # Square preview image for the main Projects list
image: "/assets/images/your-banner-image.jpg" # Large banner image inside the actual project page (optional)
excerpt: "A short 1-2 sentence summary explaining what this project aims to achieve."
published: false # Change this to 'true' when you want it to appear on the live website!
# List project members. If a member matches exactly with a name in the Team database, they will be highlighted and linked!
project_members:
  - name: "Ricardo Usbeck"
    role: "Scientific Project Manager"
  - name: "Anna Ehrenberg"
# Add related links (e.g., video, social network, publications). Remove or leave empty if none.
links:
  - title: "Project Video"
    url: "https://youtube.com/"
  - title: "Publications"
    url: "https://google.com/"
---

Explain the background and goals of the project here.

## Objectives
- Objective 1
- Objective 2

## Methodology
Describe how you are solving the problem.

**Images inside the text:**
If you want a beautifully formatted image with dynamic width, height, and a caption, use this HTML block:

{% highlight html %}
<figure style="text-align: center; margin: 2rem 0;">
  <img src="{{ '/assets/images/your-image.jpg' | relative_url }}" alt="Description" style="width: 100%; max-width: 600px; height: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  <figcaption style="font-size: 0.9rem; color: gray; margin-top: 0.5rem;">Your caption goes here</figcaption>
</figure>
{% endhighlight %}
