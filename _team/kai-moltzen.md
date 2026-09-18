---
name: "Kai Moltzen"
title: "Research Associate in GeoAI"
image: "kai-moltzen.png"
job_category: "researcher"

bio: |
  Following my Bachelor's in Engineering and Management (B. Eng.) at Esslingen University of Applied Sciences, I completed an M.Sc. in Data Science at Leuphana University Lüneburg. Alongside my studies, I gained industry experience through internships and working student positions at Mercedes-Benz, Ulixes Robotersysteme, and Markt-Pilot.

  During both my undergraduate and graduate education, I enjoyed sharing knowledge by conducting tutorials in Mathematics and Machine Learning. I was also actively involved as a student representative and member of various study commissions during my Bachelor's and Master's studies. To broaden my cultural and technical horizons, I spent three semesters abroad at Tampere University (Finland) and Ca' Foscari University of Venice (Italy).

  Currently, as a research associate in Leuphana's AIX group, I am pursuing my PhD under the supervision of Ricardo Usbeck. In this role, I continue my passion for teaching across several subjects, contribute to the development of the research group, and conduct research in topics related to GeoAI.

  In my research, I am driven by the goal of strengthening societal resilience. Through combining the wealth of geospatial information contained in natural language with our knowledge of the physical world as learned from massive amounts of remote sensing images, I am convinced we can improve our understanding of our environment. This helps a plethora of applications, with my focus lying on the rapid and reliable generation of global disaster information and mitigation strategies.

research_interests:
  - Geospatial Foundation Models (GeoFMs) & Earth Embeddings
  - (Qualitative) Spatial Reasoning
  - Geospatial Knowledge Graphs (GeoKGs)
  - AI to enhance (natural) disaster resilience
  - Spatial Representation Learning
  - Explainable Artificial Intelligence
  - Natural Language Understanding

teaching:
  - "Connecting AI and our Environment: Current Methods in GeoAI (M.Sc.)"
  - Explainable Artificial Intelligence (XAI) and Data Visualization (B.Sc.)
  - Advanced Machine Learning - LLMs, RAG, KGs (M.Sc.)
  - AI project (B.Sc.)
  - Foundations of AI (B.Sc.)
  - DataX (B.Sc.)

education:
  - degree: "Management and Data Science, Master"
    thesis: "A Self-Reflective, LLM-Driven Multi-Agent Architecture for Georelating Natural Disasters from News"
    institution: "Leuphana Universität Lüneburg"
    period: "01.10.2022 → 21.03.2025"
    supervisor: "Usbeck, Ricardo"
  - degree: "Engineering and Management, Bachelor"
    thesis: "Object Controlled Technologies for Digital Assistance Systems in Manual Assemlies"
    institution: "Esslingen University of Applied Sciences"
    period: "01.03.2018 → 28.02.2022"
    supervisor: "Reichert, Frederik"

prizes:
  - name: "2025 Research Award of the School of Management & Technology"
    date: "10.12.2025"
  - name: "Award for Completing the Course of Study 'Management and Data Science' with Outstanding Success"
    date: "14.06.2025"

email: "kai.moltzen@leuphana.de"
phone: "+49.4131.677-2417"
office: "C4.308b"
address: "Universitätsallee 1, 21335 Lüneburg"
orcid: "0009-0001-8150-3181"
website: "https://www.leuphana.de/en/institutes/iis/persons/kai-moltzen.html"
research_portal: "https://fis.leuphana.de/en/persons/kai-moltzen/"

layout: team_member
permalink: /team/kai-moltzen/
---
## Me in Short
Hi, I'm Kai. I research and teach about automatically interpreting language that describes geospatial regions or event like the destruction caused by a disaster. For that, I combine natural language texts with earth embeddings learned from remote sensing images. Let's get in contact!

## Vita

{{ page.bio }}

## Research Interests

{% for interest in page.research_interests %}
- {{ interest }}
{% endfor %}

## Teaching

{% for course in page.teaching %}
- {{ course }}
{% endfor %}

## Education/Academic qualification

{% for edu in page.education %}
- **{{ edu.degree }}**, {{ edu.thesis }}, {{ edu.institution }}<br>{{ edu.period }}, supervised by {{ edu.supervisor }}
{% endfor %}

## Prizes

{% for prize in page.prizes %}
- {{ prize.name }} ({{ prize.date }})
{% endfor %}

## Contact

- Email: [{{ page.email }}](mailto:{{ page.email }})
- Phone: {{ page.phone }}
- Office: {{ page.office }}, {{ page.address }}
- ORCID: [{{ page.orcid }}](https://orcid.org/{{ page.orcid }})
- Leuphana profile: [{{ page.name }}]({{ page.website }})
- Research portal: [{{ page.name }}]({{ page.research_portal }})
