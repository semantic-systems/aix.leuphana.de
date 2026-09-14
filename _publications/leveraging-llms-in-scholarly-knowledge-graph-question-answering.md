---
layout: publication
title: "Leveraging LLMs in Scholarly Knowledge Graph Question Answering"
year: 2023
authors:
  - "Tilahun Abedissa Taffa"
  - "Ricardo Usbeck"
is_conference: true
is_journal: false
is_archive: false
conference: "QALD/SemREC@ISWC 2023"
---

> **Abstract:**
> This paper presents a scholarly Knowledge Graph Question Answering (KGQA) that answers bibliographic natural language questions by leveraging a large language model (LLM) in a few-shot manner. The model initially identifies the top-n similar training questions related to a given test question via a BERT-based sentence encoder and retrieves their corresponding SPARQL. Using the top-n similar question-SPARQL pairs as an example and the test question creates a prompt. Then pass the prompt to the LLM and generate a SPARQL. Finally, runs the SPARQL against the underlying KG - ORKG (Open Research KG) endpoint and returns an answer. Our system achieves an F1 score of 99.0%, on SciQA - one of the Scholarly-QALD-23 challenge benchmarks.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@inproceedings{DBLP:conf/semweb/TaffaU23,
  author       = {Tilahun Abedissa Taffa and
                  Ricardo Usbeck},
  editor       = {Debayan Banerjee and
                  Ricardo Usbeck and
                  Nandana Mihindukulasooriya and
                  Gunjan Singh and
                  Raghava Mutharaju and
                  Pavan Kapanipathi},
  title        = {Leveraging LLMs in Scholarly Knowledge Graph Question Answering},
  booktitle    = {Joint Proceedings of Scholarly {QALD} 2023 and SemREC 2023 co-located
                  with 22nd International Semantic Web Conference {ISWC} 2023, Athens,
                  Greece, November 6-10, 2023},
  series       = {{CEUR} Workshop Proceedings},
  volume       = {3592},
  publisher    = {CEUR-WS.org},
  year         = {2023},
  url          = {https://ceur-ws.org/Vol-3592/paper5.pdf},
  timestamp    = {Tue, 02 Jan 2024 17:44:44 +0100},
  biburl       = {https://dblp.org/rec/conf/semweb/TaffaU23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
