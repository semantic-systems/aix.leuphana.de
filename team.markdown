---
layout: page
title: Team
permalink: /team/
---

{% assign team_by_category = site.team | group_by: "job_category" %}
{% for category in team_by_category %}
{% case category.name %}
{% when "head" %}
<h2>Head</h2>
{% when "academic_advisor" %}
<h2>Academic Advisor</h2>
{% when "research_assistant" %}
<h2>Research Assistants</h2>
{% when "research_associate" %}
<h2>Research Associate</h2>
{% when "scholarship_holder" %}
<h2>Scholarship Holder</h2>
{% when "external_phd" %}
<h2>External PhD Students</h2>
{% when "student_assistant" %}
<h2>Student Assistants and Research Assistants</h2>
{% when "alumni" %}
<h2>Alumni</h2>
{% else %}
<h2>{{ category.name | replace: "_", " " | capitalize }}</h2>
{% endcase %}
<div class="team-grid">
{% for member in category.items %}
<div class="person-card">
<a href="{{ member.url }}">
<img src="/assets/images/{{ member.image }}" alt="{{ member.name }}" class="profile-pic">
<div>
<h3>{{ member.name }}</h3>
<p class="role">{{ member.title }}</p>
</div>
</a>
</div>
{% endfor %}
</div>
{% endfor %}
