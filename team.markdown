---
layout: page
title: Team
permalink: /team/
---

{% assign category_order = "head,tech_and_admin,academic_advisor,research_assistant,research_associate,scholarship_holder,external_phd,student_assistant,alumni" | split: "," %}
{% for category_name in category_order %}
{% assign members = site.team | where: "job_category", category_name %}
{% if members.size > 0 %}
{% case category_name %}
{% when "head" %}
<h2>Head</h2>
{% when "academic_advisor" %}
<h2>Academic Advisor</h2>
{% when "tech_and_admin" %}
<h2>Technical and Administrative Staff</h2>
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
{% endcase %}
<div class="team-grid">
{% for member in members %}
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
{% endif %}
{% endfor %}
