---
# Team Member Template
# This is a template for creating individual team member pages
# Copy this file and rename it to [first-name-last-name].md
# Then fill in the details below

# Required fields
name: "Debayan Banerjee"
title: "Academic/Professional Title"
image: "debayan_banerjee.png"  # Place image in assets/images/ directory
job_category: "academic_advisor"     # Use one of: head, tech_and_admin, academic_advisor, research_assistant, research_associate, scholarship_holder, external_phd, student_assistant, alumni

# Optional fields
bio: |
  Write a short biography here. This can include your academic background, research interests, and professional experience.

research_interests:
  - Interest 1
  - Interest 2
  - Interest 3

email: "email@example.com"
website: "https://personal-website.com"
github: "github-username"
linkedin: "linkedin-profile-url"
office: "Office Location"

# Layout settings (do not modify)
layout: team_member
permalink: /team/:title/
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