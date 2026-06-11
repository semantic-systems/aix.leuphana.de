---
layout: page
title: Publications
permalink: /publications/
---

{% assign publications_by_year = site.publications | group_by: "year" | sort: "name" | reverse %}

{% for year_group in publications_by_year %}
  ## {{ year_group.name }}

  {% for publication in year_group.items %}
    <div class="publication-entry">
      <h3>
        <a href="{{ publication.url }}">{{ publication.title }}</a>
        {% if publication.github_page %}
          <span class="github-link">[GitHub Page]</span>
        {% endif %}
      </h3>
      <p><strong>Authors:</strong> {{ publication.authors | join: ", " }}</p>
      <p><strong>Conference:</strong> {{ publication.conference }}</p>
      {% if publication.abstract %}
        <div class="publication-abstract">
          <strong>Abstract:</strong> {{ publication.abstract | truncatewords: 30 }}
          <a href="{{ publication.url }}">Read more</a>
        </div>
      {% endif %}
    </div>
  {% endfor %}
{% endfor %}
