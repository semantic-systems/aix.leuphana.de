---
layout: project
title: "Disaster Response Knowledge Graphs"
status: "Completed"
team: ["Kai Moltzen", "Ricardo Usbeck"]
github_repo: "https://github.com/semantic-systems/SIGSPATIAL2025-Georelating"
image: /assets/images/Georelating_overview.png
excerpt: "Building dynamic knowledge graphs that map complex locative expressions to physical geographic grids for rapid disaster response."
---

### Project Overview

When natural disasters strike, rapid and accurate identification of the affected areas is paramount for coordinating response and relief efforts. However, early reports of these events (such as news articles or social media posts) often describe locations using complex, relational language rather than precise coordinates. 

For example, a report might say a fire broke out "between the communities of Moorpark and Somis."

This project focuses on the novel task of **Georelating**—inferring these unnamed, relationally-described regions and mapping them onto standardized Discrete Global Grid Systems (DGGSs).

<figure style="margin: 2rem 0; text-align: center;">
  <img src="{{ '/assets/images/Georelating_overview.png' | relative_url }}" alt="Illustration of Georelating" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
  <figcaption style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.5rem;">Georelating parses a natural disaster's impact area described in text to a Discrete Global Grid System (DGGS) cell.</figcaption>
</figure>

### Methodology

Our approach utilizes a multi-agent Large Language Model (LLM) architecture.
1.  **Candidate Generation:** We first extract toponyms (place names) from the text and query geographical databases (like GeoNames) to resolve them to specific coordinates.
2.  **Reasoning:** We employ an "actor-critic" LLM setup to reason about the spatial relations (e.g., "North of", "between") connecting these resolved landmarks.
3.  **Grid Mapping:** We calculate the likely extent of the event and identify the smallest H3 DGGS cell that completely encompasses the predicted area.

### Impact

By moving beyond simple point-based geoparsing and instead resolving the actual *area* of impact into a standard grid, our system allows for immediate cross-referencing with other geospatial data (like population density or infrastructure maps) in a unified Geospatial Knowledge Graph, empowering first responders with actionable intelligence.
