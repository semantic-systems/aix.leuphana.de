<!-- ---
layout: project
title: "Neuro-Symbolic LLM Integration"
status: "Active"
team: ["Ricardo Usbeck", "Junbo Huang"]
github_repo: "https://github.com/semantic-systems/neuro-symbolic-llm"
image: ""
excerpt: "Investigating the seamless integration of Large Language Models with Knowledge Graphs to improve factual accuracy and reasoning capabilities."
---

<figure style="margin: 2rem 0; text-align: center;">
  <div style="background: var(--c-granit-20); height: 350px; display: flex; align-items: center; justify-content: center; border-radius: 8px; border: 2px dashed var(--c-granit-40);">
    <span style="color: var(--text-secondary); font-style: italic;">[ Placeholder: Architectural diagram showing LLM and KG interaction ]</span>
  </div>
  <figcaption style="font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.5rem;">System architecture for the Neuro-Symbolic Reasoner.</figcaption>
</figure>

### Project Overview

Large Language Models (LLMs) have demonstrated remarkable capabilities in natural language understanding and generation. However, they are prone to hallucinations and often struggle with complex, multi-hop logical reasoning.

This project investigates the integration of LLMs with structured Knowledge Graphs (KGs). By anchoring the generative capabilities of LLMs in the factual, verifiable triples of a Knowledge Graph, we aim to build neuro-symbolic systems that are both highly articulate and strictly factual.

### Key Objectives

1.  **Retrieval-Augmented Reasoning:** Developing novel methods for retrieving sub-graphs from massive KGs that are highly relevant to a user's query, and encoding them into the LLM's context.
2.  **Explainability:** Ensuring that every claim made by the LLM can be traced back to a specific node or edge in the Knowledge Graph, providing a verifiable "chain of thought."
3.  **Knowledge Base Population:** Using LLMs to extract structured information from unstructured text to continuously grow and refine the underlying Knowledge Graph.

### Current Progress

We have successfully developed a prototype that queries Wikidata in real-time to verify the factual consistency of LLM outputs. Preliminary results show a 40% reduction in hallucinations on complex factual queries compared to standard, ungrounded LLMs. -->
