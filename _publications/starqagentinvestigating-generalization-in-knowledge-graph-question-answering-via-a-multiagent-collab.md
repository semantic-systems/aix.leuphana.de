---
layout: publication
title: "STaRQ-Agent-Investigating Generalization in Knowledge Graph Question Answering via a Multi-Agent Collaborative Framework"
year: 2026
authors:
  - "Longquan Jiang 0001"
  - "Debayan Banerjee"
  - "Ricardo Usbeck"
doi: "https://doi.org/10.1109/ACCESS.2026.3681404"
is_conference: false
is_journal: true
is_archive: false
journal: "IEEE Access"
---

> **Abstract:**
> Generalization to different Knowledge Graphs (KGs) is a core challenge of Knowledge Graph Question Answering (KGQA). Current models struggle to adapt to unseen KGs due to their underlying heterogeneity. Most approaches depend on data-hungry methods, such as supervised fine-tuning and KG-specific few-shot demonstrations. These systems are limited in cross-KG generalization, and may exhibit hallucination problems, especially in low-resource or domain-specific scenarios. This paper presents STaRQ-Agent, an LLM-based multi-agent collaborative framework for the KGQA generalization problem. It comprises a core agent for SPARQL query generation, accompanied by three supportive agents for schema selection, template generation, and query refinement. This collaborative framework helps mitigate hallucination problems inherent in LLMs. STaRQ-Agent was evaluated on LC-QuAD 1.0, QALD-9, MetaQA, and MatKGQA datasets in few-shot and zero-shot settings. Experimental results demonstrate strong overall generalization across diverse KGs, without requiring high-quality annotated data, re-training, or fine-tuning. Specially, on LC-QuAD 1.0, QALD-9, and MetaQA, few-shot STaRQ-Agent outperforms the strongest baseline by 5.1%, 4.3%, and 0.7%, while zero-shot STaRQ-Agent shows only modest F1 drops of 8.7%, 12.3%, and 10.8%. Moreover, the state-of-the-art results on MatKGQA show its robust out-of-distribution generalization to novel KGs in low-resource specific domains.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@article{DBLP:journals/access/JiangBU26,
  author       = {Longquan Jiang and
                  Debayan Banerjee and
                  Ricardo Usbeck},
  title        = {STaRQ-Agent-Investigating Generalization in Knowledge Graph Question
                  Answering via a Multi-Agent Collaborative Framework},
  journal      = {{IEEE} Access},
  volume       = {14},
  pages        = {59158--59170},
  year         = {2026},
  url          = {https://doi.org/10.1109/ACCESS.2026.3681404},
  doi          = {10.1109/ACCESS.2026.3681404},
  timestamp    = {Mon, 04 May 2026 17:57:42 +0200},
  biburl       = {https://dblp.org/rec/journals/access/JiangBU26.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
