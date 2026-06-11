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
  Accurately identifying disaster-affected areas is crucial for data-driven disaster resilience. In response, we introduce Georelating, a task that infers affected areas from textual reports containing complex locative expressions, moving beyond traditional geoparsing approaches that rely on explicit point locations. Georelating instead combines resolving unnamed regions and reasoning about spatial relations to represent event-affected areas within standardized Discrete Global Grid Systems (DGGSs).

  We propose addressing Georelating with a pipeline capitalizing on the contextual understanding of large language model (LLM) agents to perform geospatial reasoning. Preliminary evaluation highlights the potential of this approach for the foundational geocoding stage and the novel Georelating task. We point out future paths for enhancing Georelating systems toward intuitive and efficient disaster information systems.

conference: "ACM SIGSPATIAL 2025"
doi: "https://doi.org/10.1145/3748636.3762733"
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