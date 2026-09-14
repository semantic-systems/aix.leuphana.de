---
layout: publication
title: "Entity Linking with Out-of-Knowledge-Graph Entity Detection and Clustering Using Only Knowledge Graphs"
year: 2024
authors:
  - "Cedric Möller"
  - "Ricardo Usbeck"
doi: "https://doi.org/10.3233/SSW240009"
is_conference: true
is_journal: false
is_archive: false
conference: "SEMANTICS 2024"
---

> **Abstract:**
> . Entity Linking is crucial for numerous downstream tasks, such as question answering, knowledge graph population, and general knowledge extraction. A frequently overlooked aspect of entity linking is the potential encounter with entities not yet present in a target knowledge graph. Although some recent studies have addressed this issue, they primarily utilize full-text knowledge bases or depend on external information. However, these resources are not available in most use cases. In this work, we solely rely on the information within a knowledge graph and assume no external information is accessible. To investigate the challenge of identifying and disambiguating entities absent from the knowledge graph, we introduce a comprehensive silver-standard benchmark dataset that covers texts from 1999 to 2022. Based on our novel dataset, we develop an approach using pre-trained language models and knowledge graph embeddings without the need for a parallel full-text corpus. Moreover, by assessing the influence of knowledge graph embeddings on the given task, we show that implementing a sequential entity linking approach, which considers the whole sentence, can outperform clustering techniques that handle each mention separately in specific instances.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/i-semantics/MollerU24,
  author       = {Cedric M{\"{o}}ller and
                  Ricardo Usbeck},
  editor       = {Angelo A. Salatino and
                  Mehwish Alam and
                  Femke Ongenae and
                  Sahar Vahdati and
                  Anna Lisa Gentile and
                  Tassilo Pellegrini and
                  Shufan Jiang},
  title        = {Entity Linking with Out-of-Knowledge-Graph Entity Detection and Clustering
                  Using Only Knowledge Graphs},
  booktitle    = {Knowledge Graphs in the Age of Language Models and Neuro-Symbolic
                  {AI} - Proceedings of the 20th International Conference on Semantic
                  Systems, 17-19 September 2024, Amsterdam, The Netherlands},
  series       = {Studies on the Semantic Web},
  volume       = {60},
  pages        = {88--105},
  publisher    = {{IOS} Press},
  year         = {2024},
  url          = {https://doi.org/10.3233/SSW240009},
  doi          = {10.3233/SSW240009},
  timestamp    = {Wed, 05 Nov 2025 16:09:05 +0100},
  biburl       = {https://dblp.org/rec/conf/i-semantics/MollerU24.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
