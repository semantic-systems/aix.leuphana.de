---
layout: publication
title: "Text-to-SPARQL Generation with Reinforcement Learning: A GRPO-based Approach on DBLP"
year: 2026
authors:
  - "Jann Pfeifer"
  - "Debayan Banerjee"
  - "Ricardo Usbeck"
doi: "https://doi.org/10.48550/ARXIV.2605.20066"
is_conference: false
is_journal: false
is_archive: true
demo: 
---

> **Abstract:**
> Knowledge graph question answering seeks to translate natural language questions into executable queries over knowledge graphs, but existing approaches often rely on large models or full supervision in the form of gold query annotations. This study examines whether reinforcement learning with outcome-based rewards can train a small instruction-tuned language model to perform zero-shot Text-to-SPARQL generation in the scholarly domain. Group-Relative Policy Optimization (GRPO) is applied to the Qwen3-1.7B model on DBLP-QuAD, using prompts that combine natural language questions with symbolic hints about entities and relations. Training relies on execution feedback, structural constraints, and answer-level rewards, with an additional variant that incorporates gold-query-based shaping. The resulting models are compared to the unmodified zero-shot baseline and to a supervised DoRA-finetuned baseline across answer-level accuracy, execution accuracy, category-wise scores, and generalization to held-out templates. GRPO substantially improves over the zero-shot baseline and exhibits competitive generalization, while supervised DoRA finetuning achieves higher overall accuracy on the same model scale. Ablation analyses indicate that execution-based rewards account for most gains, with additional shaping yielding limited additional benefit, suggesting that outcome-based reinforcement learning is a viable training strategy when gold queries are unavailable for token-level supervision.

<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@article{DBLP:journals/corr/abs-2605-20066,
  author       = {Jann Pfeifer and
                  Debayan Banerjee and
                  Ricardo Usbeck},
  title        = {Text-to-SPARQL Generation with Reinforcement Learning: {A} GRPO-based
                  Approach on {DBLP}},
  journal      = {CoRR},
  volume       = {abs/2605.20066},
  year         = {2026},
  url          = {https://doi.org/10.48550/arXiv.2605.20066},
  doi          = {10.48550/ARXIV.2605.20066},
  eprinttype   = {arXiv},
  eprint       = {2605.20066},
  timestamp    = {Fri, 12 Jun 2026 15:09:06 +0200},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2605-20066.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
