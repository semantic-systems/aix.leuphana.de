---
name: "Prof. Dr. Ricardo Usbeck"
title: "Head of Research Group"
image: "ricardo_usbeck.jpg"
job_category: "head"

bio: |
  Prof. Dr. Ricardo Usbeck is the head of the Artificial Intelligence and Explainability (AIX) research group at Leuphana University. His research focuses on neuro-symbolic AI, combining neural network-based machine learning with symbolic AI to create explainable and responsible real-world solutions.

  With a strong background in Natural Language Processing and Knowledge Graphs, Prof. Usbeck leads innovative research in areas such as Knowledge Graph Question Answering, Conversational AI, and Bio-medical Knowledge Graphs.

research_interests:
  - Neuro-symbolic AI
  - Knowledge Graph Question Answering
  - Conversational AI
  - Natural Language Processing
  - Bio-medical Knowledge Graphs
  - Ethics of AI
  - Sustainability in AI

email: "ricardo.usbeck@leuphana.de"
website: "https://www.leuphana.de/en/institutes/iis/artificial-intelligence-and-explainability.html"
github: "ricardousbeck"
linkedin: "https://www.linkedin.com/in/ricardo-usbeck/"
office: "C14.103"

layout: team_member
permalink: /team/ricardo-usbeck/
---

## About Me

{{ page.bio }}

## Research Interests

{% for interest in page.research_interests %}
- {{ interest }}
{% endfor %}

## Contact

- Email: {{ page.email }}
{% if page.website %}- Website: [{{ page.name }}]({{ page.website }}){% endif %}
{% if page.github %}- GitHub: [{{ page.github }}](https://github.com/{{ page.github }}){% endif %}
{% if page.linkedin %}- LinkedIn: [{{ page.name }}]({{ page.linkedin }}){% endif %}
{% if page.office %}- Office: {{ page.office }}{% endif %}