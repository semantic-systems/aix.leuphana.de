---
layout: publication
title: "DBLPLink: An Entity Linker for the DBLP Scholarly Knowledge Graph"
year: 2023
authors:
  - "Debayan Banerjee"
  - "Arefa"
  - "Ricardo Usbeck"
  - "Chris Biemann"
is_conference: true
is_journal: false
is_archive: false
conference: "ISWC 2023"
---

> **Abstract:**
> In this work, we present a web application named DBLPLink, which performs entity linking over the DBLP scholarly knowledge graph. DBLPLink uses text-to-text pre-trained language models, such as T5, to produce entity label spans from an input text question. Entity candidates are fetched from a database based on the labels, and an entity re-ranker sorts them based on entity embeddings, such as TransE, DistMult and ComplEx. The results are displayed so that users may compare and contrast the results between T5-small, T5-base and the different KG embeddings used. The demo can be accessed at https://ltdemos.informatik.uni-hamburg.de/dblplink/.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/semweb/BanerjeeAUB23,
  author       = {Debayan Banerjee and
                  Arefa and
                  Ricardo Usbeck and
                  Chris Biemann},
  editor       = {Irini Fundulaki and
                  Kouji Kozaki and
                  Daniel Garijo and
                  Jos{\'{e}} Manu{\'{e}}l G{\'{o}}mez{-}P{\'{e}}rez},
  title        = {DBLPLink: An Entity Linker for the {DBLP} Scholarly Knowledge Graph},
  booktitle    = {Proceedings of the {ISWC} 2023 Posters, Demos and Industry Tracks:
                  From Novel Ideas to Industrial Practice co-located with 22nd International
                  Semantic Web Conference {(ISWC} 2023), Athens, Greece, November 6-10,
                  2023},
  series       = {{CEUR} Workshop Proceedings},
  volume       = {3632},
  publisher    = {CEUR-WS.org},
  year         = {2023},
  url          = {https://ceur-ws.org/Vol-3632/ISWC2023\_paper\_428.pdf},
  timestamp    = {Wed, 07 Feb 2024 16:02:39 +0100},
  biburl       = {https://dblp.org/rec/conf/semweb/BanerjeeAUB23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
