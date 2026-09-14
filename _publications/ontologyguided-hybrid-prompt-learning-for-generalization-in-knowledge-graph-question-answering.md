---
layout: publication
title: "Ontology-Guided, Hybrid Prompt Learning for Generalization in Knowledge Graph Question Answering"
year: 2025
authors:
  - "Longquan Jiang 0001"
  - "Junbo Huang"
  - "Cedric Möller"
  - "Ricardo Usbeck"
doi: "https://doi.org/10.1109/ICSC64641.2025.00010"
is_conference: true
is_journal: false
is_archive: false
conference: "ICSC 2025"
---

> **Abstract:**
> Most existing Knowledge Graph Question Answering (KGQA) approaches are designed for a specific KG, such as Wikidata, DBpedia or Freebase. Due to the heterogeneity of the underlying graph schema, topology and assertions, most KGQA systems cannot be transferred to unseen Knowledge Graphs (KGs) without resource-intensive training data. We present OntoSCPrompt, a novel Large Language Model (LLM)-based KGQA approach with a two-stage architecture that separates semantic parsing from KG-dependent interactions. OntoSCPrompt first generates a SPARQL query structure (including SPARQL keywords such as SELECT, ASK, WHERE and placeholders for missing tokens) and then fills them with KG-specific information. To enhance the understanding of the underlying KG, we present an ontology-guided, hybrid prompt learning strategy that integrates KG ontology into the learning process of hybrid prompts (e.g., discrete and continuous vectors). We also present several task-specific decoding strategies to ensure the correctness and executability of generated SPARQL queries in both stages. Experimental results demonstrate that OntoSCPrompt performs as well as SOTA approaches without retraining on a number of KGQA datasets such as CWQ, WebQSP and LC-QuAD 1.0 in a resource-efficient manner and can generalize well to unseen domain-specific KGs like DBLP-QuAD and CoyPu KG 11Code: https://github.com/LongquanJiang/OntoSCPrompt.

<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/semco/JiangHMU25,
  author       = {Longquan Jiang and
                  Junbo Huang and
                  Cedric M{\"{o}}ller and
                  Ricardo Usbeck},
  title        = {Ontology-Guided, Hybrid Prompt Learning for Generalization in Knowledge
                  Graph Question Answering},
  booktitle    = {19th International Conference on Semantic Computing, {ICSC} 2025,
                  Laguna Hills, CA, USA, February 3-5, 2025},
  pages        = {28--35},
  publisher    = {{IEEE}},
  year         = {2025},
  url          = {https://doi.org/10.1109/ICSC64641.2025.00010},
  doi          = {10.1109/ICSC64641.2025.00010},
  timestamp    = {Wed, 02 Jul 2025 18:52:19 +0200},
  biburl       = {https://dblp.org/rec/conf/semco/JiangHMU25.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
