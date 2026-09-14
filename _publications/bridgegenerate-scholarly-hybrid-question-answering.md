---
layout: publication
title: "Bridge-Generate: Scholarly Hybrid Question Answering"
year: 2025
authors:
  - "Tilahun Abedissa Taffa"
  - "Ricardo Usbeck"
doi: "https://doi.org/10.1145/3701716.3715459"
is_conference: true
is_journal: false
is_archive: false
conference: "WWW 2025"
---

> **Abstract:**
> Answering scholarly hybrid questions requires access to bibliographic facts stored in structured data, such as a Knowledge Graph (KG) and textual information. Existing Scholarly Hybrid Question Answering (SHQA) approaches rely on retrieving KG triples and documents from the Wikipedia text corpus and prompt an LLM (Large Language Model) for answers. However, the retrieval is heavily keyword-based, introducing noise into the context. Furthermore, despite detecting the entities in the question, the models do not attempt any question analysis. Therefore, we propose a new SHQA system that employs a bridge-generate approach. During the bridge phase, our system recursively identifies entity-encapsulating phrases within the question and resolves the entities leveraging the underlying KGs. It then formulates assertion statements based on the resolved entities and their corresponding phrases. In the generation phase, the system auto-generates context guided by the question and the assertions. Finally, it returns an answer prompting an LLM with the generated context, the assertions, and the question. Our approach outperforms previous approaches, addressing the identified gaps.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/www/TaffaU25,
  author       = {Tilahun Abedissa Taffa and
                  Ricardo Usbeck},
  editor       = {Guodong Long and
                  Michale Blumestein and
                  Yi Chang and
                  Liane Lewin{-}Eytan and
                  Zi Helen Huang and
                  Elad Yom{-}Tov},
  title        = {Bridge-Generate: Scholarly Hybrid Question Answering},
  booktitle    = {Companion Proceedings of the {ACM} on Web Conference 2025, {WWW} 2025,
                  Sydney, NSW, Australia, 28 April 2025 - 2 May 2025},
  pages        = {1321--1325},
  publisher    = {{ACM}},
  year         = {2025},
  url          = {https://doi.org/10.1145/3701716.3715459},
  doi          = {10.1145/3701716.3715459},
  timestamp    = {Sun, 02 Nov 2025 21:27:17 +0100},
  biburl       = {https://dblp.org/rec/conf/www/TaffaU25.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
