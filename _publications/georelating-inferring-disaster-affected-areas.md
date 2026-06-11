---
title: "Georelating: Inferring Disaster-Affected Areas from Textual Reports"
authors:
  - "Ricardo Usbeck"
  - "Kai Moltzen"
  - "Jubo Huang"
year: 2025
github_repo: "https://github.com/semantic-systems/SIGSPATIAL2025-Georelating"
github_page: "https://semantic-systems.github.io/SIGSPATIAL2025-Georelating/"

abstract: |
  This paper presents Georelating, a novel approach for inferring disaster-affected areas from textual reports. Our method combines natural language processing with geospatial analysis to automatically identify locations mentioned in disaster reports and map them to affected areas.

conference: "ACM SIGSPATIAL 2025"
doi: "https://doi.org/10.1145/3486193.3486201"
pdf: "https://arxiv.org/pdf/2506.00001.pdf"

layout: publication
permalink: /publications/georelating-inferring-disaster-affected-areas/
---

## {{ page.title }}

**Authors:** {{ page.authors | join: ", " }}

**Year:** {{ page.year }}

**GitHub:** [Repository]({{ page.github_repo }})

**GitHub Page:** [Project Website]({{ page.github_page }})

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