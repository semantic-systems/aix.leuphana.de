---
layout: publication
title: "GETT-QA: Graph Embedding Based T2T Transformer for Knowledge Graph Question Answering"
year: 2023
authors:
  - "Debayan Banerjee"
  - "Pranav Ajit Nair"
  - "Ricardo Usbeck"
  - "Chris Biemann"
doi: "https://doi.org/10.1007/978-3-031-33455-9_17"
is_conference: true
is_journal: false
is_archive: false
conference: "ESWC 2023"
---

> **Abstract:**
> In this work, we present an end-to-end Knowledge Graph Question Answering (KGQA) system named GETT-QA. GETT-QA uses T5, a popular text-to-text pre-trained language model. The model takes a question in natural language as input and produces a simpler form of the intended SPARQL query. In the simpler form, the model does not directly produce entity and relation IDs. Instead, it produces corresponding entity and relation labels. The labels are grounded to KG entity and relation IDs in a subsequent step. To further improve the results, we instruct the model to produce a truncated version of the KG embedding for each entity. The truncated KG embedding enables a finer search for disambiguation purposes. We find that T5 is able to learn the truncated KG embeddings without any change of loss function, improving KGQA performance. As a result, we report strong results for LC-QuAD 2.0 and SimpleQuestions-Wikidata datasets on end-to-end KGQA over Wikidata.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/esws/BanerjeeNUB23,
  author       = {Debayan Banerjee and
                  Pranav Ajit Nair and
                  Ricardo Usbeck and
                  Chris Biemann},
  editor       = {Catia Pesquita and
                  Ernesto Jim{\'{e}}nez{-}Ruiz and
                  Jamie P. McCusker and
                  Daniel Faria and
                  Mauro Dragoni and
                  Anastasia Dimou and
                  Rapha{\"{e}}l Troncy and
                  Sven Hertling},
  title        = {{GETT-QA:} Graph Embedding Based {T2T} Transformer for Knowledge Graph
                  Question Answering},
  booktitle    = {The Semantic Web - 20th International Conference, {ESWC} 2023, Hersonissos,
                  Crete, Greece, May 28 - June 1, 2023, Proceedings},
  series       = {Lecture Notes in Computer Science},
  volume       = {13870},
  pages        = {279--297},
  publisher    = {Springer},
  year         = {2023},
  url          = {https://doi.org/10.1007/978-3-031-33455-9\_17},
  doi          = {10.1007/978-3-031-33455-9\_17},
  timestamp    = {Mon, 05 Feb 2024 20:32:24 +0100},
  biburl       = {https://dblp.org/rec/conf/esws/BanerjeeNUB23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
