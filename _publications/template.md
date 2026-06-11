---
# Publication Template
# This is a template for creating publication entries
# Copy this file and rename it to [publication-title].md
# Then fill in the details below

# Required fields
title: "Publication Title"
authors:
  - "Author 1"
  - "Author 2"
year: 2023
github_repo: "https://github.com/semantic-systems/repo-name"  # Link to GitHub repository
github_page: "https://semantic-systems.github.io/SIGSPATIAL2025-Georelating/"
# Optional fields
abstract: |
  Write a short abstract of the publication here.

conference: "Conference Name"
doi: "https://doi.org/..."
pdf: "https://link-to-pdf.com"
website: "https://publication-website.com"

# Layout settings (do not modify)
layout: publication
permalink: /publications/:title/
---

## {{ page.title }}

**Authors:** {{ page.authors | join: ", " }}

**Year:** {{ page.year }}

**GitHub:** [Repository]({{ page.github_repo }})

{% if page.abstract %}
## Abstract

{{ page.abstract }}
{% endif %}

{% if page.conference %}
**Conference:** {{ page.conference }}
{% endif %}

{% if page.doi %}
**DOI:** [{{ page.doi }}]({{ page.doi }})
{% endif %}

{% if page.pdf %}
**PDF:** [Download PDF]({{ page.pdf }})
{% endif %}

{% if page.website %}
**Website:** [Publication Website]({{ page.website }})
{% endif %}