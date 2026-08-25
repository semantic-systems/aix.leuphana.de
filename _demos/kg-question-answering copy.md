---
layout: demo
title: "Interactive Knowledge Graph Visualizer"
demo_url: "https://semantic-systems.github.io/kg-visualizer-demo"
image: ""
excerpt: "A web-based tool for exploring and visualizing massive RDF Knowledge Graphs in real-time."
---

<figure style="margin: 2rem 0; text-align: center;">
  {% if page.image and page.image != "" %}
    <img src="{{ page.image | relative_url }}" alt="Demo Screenshot" style="width: 100%; max-height: 500px; object-fit: contain; border-radius: 8px; border: 1px solid var(--c-granit-40); box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
  {% else %}
    <div style="background: var(--c-granit-20); height: 400px; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 2px dashed var(--c-granit-40);">
      <span style="color: var(--text-secondary); font-style: italic;">[ Placeholder: Screenshot of a complex node-edge graph visualization ]</span>
    </div>
  {% endif %}
  <figcaption style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.5rem;">The visualizer rendering a local sub-graph around a specific entity.</figcaption>
</figure>

### About This Demo

Understanding the structure of massive Knowledge Graphs (like DBpedia or Wikidata) can be incredibly challenging without the right tools. Often, researchers are forced to write complex SPARQL queries just to understand the local neighborhood of a single entity.

We built the **Interactive Knowledge Graph Visualizer** to make graph exploration intuitive and accessible. 

### Features

- **Real-time SPARQL Translation:** Type a simple query, and the visualizer translates it into SPARQL behind the scenes, rendering the results instantly.
- **Force-Directed Graph Layout:** The visualizer uses advanced physics engines to lay out nodes (entities) and edges (relations) so that the structure of the data is naturally apparent.
- **Expandable Nodes:** Click on any node to dynamically load and render its neighbors, allowing you to "walk" the graph step-by-step.

### Try It Out

Click the "Launch Demo" button above to open the application in a new tab. The demo connects to a live, read-only endpoint of DBpedia. Try searching for "Leuphana University" to see it in action!
