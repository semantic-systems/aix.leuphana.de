---
layout: publication
title: "KGXL-Query: Extending SPARQL with Semantic Search and LLM Functionality for Question Answering over Heterogeneous Data"
year: 2026
authors:
  - "Tilahun Abedissa Taffa"
  - "Patrick Westphal"
  - "Debayan Banerjee"
  - "Ricardo Usbeck"
doi: "https://doi.org/10.3233/SSW260012"
is_conference: true
is_journal: false
is_archive: false
conference: "SEMANTiCS 2026"
---

> **Abstract:**
> The quest to answer complex questions, those requiring both structured facts and contextual evidence from unstructured data, has shown a gap in knowledge systems: the incompatibility between symbolic and semantic inference. Knowledge Graphs (KGs) support formal, logically grounded querying via structured languages such as SPARQL. Conversely, LLMs (Large Language Models) and semantic text search offer broad knowledge coverage through vector-based similarity metrics. However, beyond using KGs for refining text or LLM results, and complementing missing information in KGs via LLMs or text search, there is less emphasis on accessing LLMs & semantic text search functionality through SPARQL. Moreover, existing Question Answering (QA) methods on heterogeneous data sources use RAG, data unification, and decompose-and-aggregate methods. The unifying approaches suffer from irreversible information loss; decomposition-driven methods are prone to cascading errors; and RAG methods lack explainability and are limited to shallow textual integration. Therefore, we introduce KGXL-Query, a new SPARQL functionality extension that embeds LLMs and semantic search directly into SPARQL, enabling hybrid inference where symbolic and non-symbolic methods coexist within a single, executable, and explainable framework. Additionally, KGXL-Query paves the way by transforming the question to leverage the model rather than altering the data to fit it. Our experiments on four heterogeneous QA datasets show that KGXL consistently outperforms existing methods across all four benchmarks.


