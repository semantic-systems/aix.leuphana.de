---
layout: page
title: About
permalink: /about/
---
{% comment %} The text comes from _data/about.yml (shared with the Team page). {% endcomment %}
{{ site.data.about.intro | markdownify }}

## Research

{{ site.data.about.research | markdownify }}

## Teaching

{{ site.data.about.teaching | markdownify }}

## Transfer

{{ site.data.about.transfer | markdownify }}
