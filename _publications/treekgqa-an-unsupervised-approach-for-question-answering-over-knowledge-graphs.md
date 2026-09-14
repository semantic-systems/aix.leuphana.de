---
layout: publication
title: "Tree-KGQA: An Unsupervised Approach for Question Answering Over Knowledge Graphs"
year: 2022
authors:
  - "Md. Rashad Al Hasan Rony"
  - "Debanjan Chaudhuri"
  - "Ricardo Usbeck"
  - "Jens Lehmann 0001"
doi: "https://doi.org/10.1109/ACCESS.2022.3173355"
is_conference: false
is_journal: true
is_archive: false
journal: "IEEE Access"
---

> **Abstract:**
> Most Knowledge Graph-based Question Answering (KGQA) systems rely on training data to reach their optimal performance. However, acquiring training data for supervised systems is both time-consuming and resource-intensive. To address this, in this paper, we propose Tree-KGQA, an unsupervised KGQA system leveraging pre-trained language models and tree-based algorithms. Entity and relation linking are essential components of any KGQA system. We employ several pre-trained language models in the entity linking task to recognize the entities mentioned in the question and obtain the contextual representation for indexing. Furthermore, for relation linking we incorporate a pre-trained language model previously trained for language inference task. Finally, we introduce a novel algorithm for extracting the answer entities from a KG, where we construct a forest of interpretations and introduce tree-walking and tree disambiguation techniques. Our algorithm uses the linked relation and predicts the tree branches that eventually lead to the potential answer entities. The proposed method achieves 4.5% and 7.1% gains in F1 score in entity linking tasks on LC-QuAD 2.0 and LC-QuAD 2.0 (KBpearl) datasets, respectively, and a 5.4% increase in the relation linking task on LC-QuAD 2.0 (KBpearl). The comprehensive evaluations demonstrate that our unsupervised KGQA approach outperforms other supervised state-of-the-art methods on the WebQSP-WD test set (1.4% increase in F1 score) - without training on the target dataset.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@article{DBLP:journals/access/RonyCUL22,
  author       = {Md. Rashad Al Hasan Rony and
                  Debanjan Chaudhuri and
                  Ricardo Usbeck and
                  Jens Lehmann},
  title        = {Tree-KGQA: An Unsupervised Approach for Question Answering Over Knowledge
                  Graphs},
  journal      = {{IEEE} Access},
  volume       = {10},
  pages        = {50467--50478},
  year         = {2022},
  url          = {https://doi.org/10.1109/ACCESS.2022.3173355},
  doi          = {10.1109/ACCESS.2022.3173355},
  timestamp    = {Sun, 19 Jan 2025 13:58:22 +0100},
  biburl       = {https://dblp.org/rec/journals/access/RonyCUL22.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
