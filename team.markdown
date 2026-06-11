---
layout: page
title: Team
permalink: /team/
---

{% assign team_by_category = site.team | group_by: "job_category" %}

{% for category in team_by_category %}
  {% case category.name %}
    {% when "head" %}
      ## Head
    {% when "academic_advisor" %}
      ## Academic Advisor
    {% when "research_assistant" %}
      ## Research Assistants
    {% when "research_associate" %}
      ## Research Associate
    {% when "scholarship_holder" %}
      ## Scholarship Holder
    {% when "external_phd" %}
      ## External PhD Students
    {% when "student_assistant" %}
      ## Student Assistants and Research Assistants
    {% when "alumni" %}
      ## Alumni
    {% else %}
      ## {{ category.name | replace: "_", " " | capitalize }}
  {% endcase %}

  <div class="team-grid">
    {% for member in category.items %}
      <div class="person-card">
        <a href="{{ member.url }}">
          <img src="/assets/images/{{ member.image }}" alt="{{ member.name }}" class="profile-pic">
          <div>
            <h4>{{ member.name }}</h4>
          </div>
        </a>
      </div>
    {% endfor %}
  </div>
{% endfor %}
