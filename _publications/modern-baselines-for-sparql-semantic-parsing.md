---
layout: publication
title: "Modern Baselines for SPARQL Semantic Parsing"
year: 2022
authors:
  - "Debayan Banerjee"
  - "Pranav Ajit Nair"
  - "Jivat Neet Kaur"
  - "Ricardo Usbeck"
  - "Chris Biemann"
doi: "https://doi.org/10.1145/3477495.3531841"
is_conference: true
is_journal: false
is_archive: false
conference: "SIGIR 2022"
---

> **Abstract:**
> In this work, we focus on the task of generating SPARQL queries from natural language questions, which can then be executed on Knowledge Graphs (KGs). We assume that gold entity and relations have been provided, and the remaining task is to arrange them in the right order along with SPARQL vocabulary, and input tokens to produce the correct SPARQL query. Pre-trained Language Models (PLMs) have not been explored in depth on this task so far, so we experiment with BART, T5 and PGNs (Pointer Generator Networks) with BERT embeddings, looking for new baselines in the PLM era for this task, on DBpedia and Wikidata KGs. We show that T5 requires special input tokenisation, but produces state of the art performance on LC-QuAD 1.0 and LC-QuAD 2.0 datasets, and outperforms task-specific models from previous works. Moreover, the methods enable semantic parsing for questions where a part of the input needs to be copied to the output query, thus enabling a new paradigm in KG semantic parsing.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/sigir/BanerjeeNKUB22,
  author       = {Debayan Banerjee and
                  Pranav Ajit Nair and
                  Jivat Neet Kaur and
                  Ricardo Usbeck and
                  Chris Biemann},
  editor       = {Enrique Amig{\'{o}} and
                  Pablo Castells and
                  Julio Gonzalo and
                  Ben Carterette and
                  J. Shane Culpepper and
                  Gabriella Kazai},
  title        = {Modern Baselines for {SPARQL} Semantic Parsing},
  booktitle    = {{SIGIR} '22: The 45th International {ACM} {SIGIR} Conference on Research
                  and Development in Information Retrieval, Madrid, Spain, July 11 -
                  15, 2022},
  pages        = {2260--2265},
  publisher    = {{ACM}},
  year         = {2022},
  url          = {https://doi.org/10.1145/3477495.3531841},
  doi          = {10.1145/3477495.3531841},
  timestamp    = {Thu, 12 Mar 2026 08:05:43 +0100},
  biburl       = {https://dblp.org/rec/conf/sigir/BanerjeeNKUB22.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
