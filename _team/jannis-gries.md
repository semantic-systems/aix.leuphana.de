---
name: "Jannis Gries"
title: "Doctoral Researcher | Legal AI"
image: "jannis-gries.jpg"
job_category: "researcher"

layout: team_member
permalink: /team/jannis-gries/
email: "jannis.gries[at]leuphana.de"
orcid: "0009-0000-9655-8890"


website: "https://www.leuphana.de/en/jannis-gries"
research_portal: "https://fis.leuphana.de/en/persons/jannis-gries/"
github: "jannisgries"
linkedin: "www.linkedin.com/in/jannis-gries-8116b862"
office: "C4.308b"

bio: |
  Jannis Gries is a PhD candidate and scholarship holder in the Artificial Intelligence and Explainability (AIX) research group, led by Ricardo Usbeck.

    He studied law at the University of Hamburg and KU Leuven, supported by the Deutschlandstipendium and the German Academic Scholarship Foundation. Internships during his studies took him to the Court of Justice of the European Union (CJEU) and the Federal Ministry of Finance; at the same time, he worked as a student assistant to Jürgen Basedow at the Max Planck Institute for Comparative and International Private Law. He passed his first state examination in January 2023. 

    He then worked as a research assistant to Konrad Duden at Leipzig University and, at the Max Planck Institute for Comparative and International Private Law, edited various manuscripts by Jürgen Basedow for their posthumous publication. Jannis Gries completed his legal traineeship at the Hanseatic Higher Regional Court, with placements at the Freshfields Lab, the German Federal Chancellery, and the Federal Constitutional Court.



research_interests:
    - Legal Artificial Intelligence
    - Explainable Artificial Intelligence
    - Law-based Alignment
    - Legal Argumentation
    - AI in Legal Education

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