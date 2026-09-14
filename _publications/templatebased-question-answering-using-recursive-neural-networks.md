---
layout: publication
title: "Template-based Question Answering using Recursive Neural Networks"
year: 2021
authors:
  - "Ram G. Athreya"
  - "Srividya Kona Bansal"
  - "Axel-Cyrille Ngonga Ngomo"
  - "Ricardo Usbeck"
doi: "https://doi.org/10.1109/ICSC50631.2021.00041"
is_conference: true
is_journal: false
is_archive: false
conference: "ICSC 2021"
---

> **Abstract:**
> Most question answering (QA) systems over Linked Data, i.e. Knowledge Graphs, approach the question answering task as a conversion from a natural language question to its corresponding SPARQL query. A common approach is to use query templates to generate SPARQL queries with slots that need to be filled. Using templates instead of running an extensive NLP pipeline or end-to-end model shifts the QA problem into a classification task, where the system needs to match the input question to the appropriate template. This paper presents an approach to automatically learn and classify natural language questions into corresponding templates using recursive neural networks. Our model was trained on 5000 questions and their respective SPARQL queries from the preexisting LC-QuAD dataset grounded in DBpedia, spanning 5042 entities and 615 predicates. The resulting model was evaluated using the FAIR GERBIL QA framework resulting in 0.419 macro f-measure on LC-QuAD and 0.417 macro f-measure on QALD-7.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/semco/AthreyaBNU21,
  author       = {Ram G. Athreya and
                  Srividya Kona Bansal and
                  Axel{-}Cyrille Ngonga Ngomo and
                  Ricardo Usbeck},
  title        = {Template-based Question Answering using Recursive Neural Networks},
  booktitle    = {15th {IEEE} International Conference on Semantic Computing, {ICSC}
                  2021, Laguna Hills, CA, USA, January 27-29, 2021},
  pages        = {195--198},
  publisher    = {{IEEE}},
  year         = {2021},
  url          = {https://doi.org/10.1109/ICSC50631.2021.00041},
  doi          = {10.1109/ICSC50631.2021.00041},
  timestamp    = {Mon, 26 Jun 2023 20:45:27 +0200},
  biburl       = {https://dblp.org/rec/conf/semco/AthreyaBNU21.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
