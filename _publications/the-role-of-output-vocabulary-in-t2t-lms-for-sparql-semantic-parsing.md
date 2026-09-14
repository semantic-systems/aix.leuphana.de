---
layout: publication
title: "The Role of Output Vocabulary in T2T LMs for SPARQL Semantic Parsing"
year: 2023
authors:
  - "Debayan Banerjee"
  - "Pranav Ajit Nair"
  - "Ricardo Usbeck"
  - "Chris Biemann"
doi: "https://doi.org/10.18653/V1/2023.FINDINGS-ACL.774"
is_conference: true
is_journal: false
is_archive: false
conference: "ACL 2023"
---

> **Abstract:**
> In this work, we analyse the role of output vocabulary for text-to-text (T2T) models on the task of SPARQL semantic parsing. We perform experiments within the the context of knowledge graph question answering (KGQA), where the task is to convert questions in natural language to the SPARQL query language. We observe that the query vocabulary is distinct from human vocabulary. Language Models (LMs) are pre-dominantly trained for human language tasks, and hence, if the query vocabulary is replaced with a vocabulary more attuned to the LM tokenizer, the performance of models may improve. We carry out carefully selected vocabulary substitutions on the queries and find absolute gains in the range of 17% on the GrailQA dataset.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/acl/BanerjeeNUB23,
  author       = {Debayan Banerjee and
                  Pranav Ajit Nair and
                  Ricardo Usbeck and
                  Chris Biemann},
  editor       = {Anna Rogers and
                  Jordan L. Boyd{-}Graber and
                  Naoaki Okazaki},
  title        = {The Role of Output Vocabulary in {T2T} LMs for {SPARQL} Semantic Parsing},
  booktitle    = {Findings of the Association for Computational Linguistics: {ACL} 2023,
                  Toronto, Canada, July 9-14, 2023},
  series       = {Findings of {ACL}},
  volume       = {{ACL} 2023},
  pages        = {12219--12228},
  publisher    = {Association for Computational Linguistics},
  year         = {2023},
  url          = {https://doi.org/10.18653/v1/2023.findings-acl.774},
  doi          = {10.18653/V1/2023.FINDINGS-ACL.774},
  timestamp    = {Tue, 27 Jan 2026 20:26:47 +0100},
  biburl       = {https://dblp.org/rec/conf/acl/BanerjeeNUB23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
