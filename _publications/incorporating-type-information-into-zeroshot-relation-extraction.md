---
layout: publication
title: "Incorporating Type Information into Zero-Shot Relation Extraction"
year: 2024
authors:
  - "Ricardo Usbeck"
  - "Cedric Möller"
is_conference: true
is_journal: false
is_archive: false
conference: "TEXT2KG/DQMLKG@ESWC 2024"
---

> **Abstract:**
> The task of zero-shot relation extraction focuses on the extraction of relations not seen during training time.
Commonly, additional information about the relation such as the relation name or a description of the relation is
utilised. In this work, we analyze whether a relation extractor can benefit from the inclusion of fine-grained type
information about the involved entities. This is based on the intuition that relation descriptions might contain
ontological information on the domain and range of the entity types that are usually put into relation. For that,
we follow a cross-encoding setup where we encode both, the entity information and relation information, as one
sequence and learn to score the representation. We examine this method on several datasets and show that the
inclusion of the fine-grained type information leads to an improvement in performance.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/text2kg/UsbeckM24,
  author       = {Ricardo Usbeck and
                  Cedric M{\"{o}}ller},
  editor       = {Sanju Tiwari and
                  Nandana Mihindukulasooriya and
                  Francesco Osborne and
                  Dimitris Kontokostas and
                  Jennifer D'Souza and
                  Mayank Kejriwal and
                  Maria Angela Pellegrino and
                  Anisa Rula and
                  Jos{\'{e}} Emilio Labra Gayo and
                  Michael Cochez and
                  Mehwish Alam},
  title        = {Incorporating Type Information into Zero-Shot Relation Extraction},
  booktitle    = {Joint proceedings of the 3rd International workshop on knowledge graph
                  generation from text {(TEXT2KG)} and Data Quality meets Machine Learning
                  and Knowledge Graphs {(DQMLKG)} co-located with the Extended Semantic
                  Web Conference {(} {ESWC} 2024), Hersonissos, Greece, May 26-30, 2024},
  series       = {{CEUR} Workshop Proceedings},
  volume       = {3747},
  pages        = {10},
  publisher    = {CEUR-WS.org},
  year         = {2024},
  url          = {https://ceur-ws.org/Vol-3747/text2kg\_paper3.pdf},
  timestamp    = {Thu, 31 Oct 2024 17:18:55 +0100},
  biburl       = {https://dblp.org/rec/conf/text2kg/UsbeckM24.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
