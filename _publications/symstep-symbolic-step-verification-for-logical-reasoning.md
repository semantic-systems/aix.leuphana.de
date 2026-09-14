---
layout: publication
title: "SymStep: Symbolic Step Verification for Logical Reasoning"
year: 2026
authors:
  - "Aida Usmanova"
  - "Rui Gao"
  - "Dilshod Azizov"
  - "Ricardo Usbeck"
  - "Zangir Iklassov"
doi: "https://doi.org/10.48550/ARXIV.2607.23055"
is_conference: false
is_journal: false
is_archive: true
---

> **Abstract:**
> Chain-of-thought (CoT) prompting can fail severely on constraint-dense logical reasoning tasks, where unverified errors accumulate silently across steps. We introduce SymStep: an LLM makes one atomic claim at a time (DEDUCE: Alice, pet, Cat), then a lightweight constraint propagator checks the claim for consistency with prior accepted deductions, rejects contradictions, and cascades implied facts automatically. SymStep+G additionally provides MRV guidance after each accepted step, directing the LLM toward the most constrained unresolved variable. On a 35-puzzle retained subset of ZebraLogicBench, a benchmark of 1,000 Einstein-style logic puzzles, Direct and CoT both achieve 0%, while SymStep+G reaches 97%. On AR-LSAT analytical reasoning problems, SymStep achieves 100% vs. CoT's 87%. On LGP-14, SymStep+G achieves 100% vs. 0% for CoT and Logic-LM, the strongest prior symbolic+LLM baseline we compare against. Ablation studies reveal that MRV guidance is a key mechanism for reducing directionless cycling, while consistency checking provides a safety net against explicit contradictions. Across six benchmarks spanning five task domains, SymStep variants match or exceed every baseline on constraint-dense and arithmetic tasks. Experiments on AQUA-RAT algebra confirm the advantage is constraint-density-specific.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@article{DBLP:journals/corr/abs-2607-23055,
  author       = {Aida Usmanova and
                  Rui Gao and
                  Dilshod Azizov and
                  Ricardo Usbeck and
                  Zangir Iklassov},
  title        = {SymStep: Symbolic Step Verification for Logical Reasoning},
  journal      = {CoRR},
  volume       = {abs/2607.23055},
  year         = {2026},
  url          = {https://doi.org/10.48550/arXiv.2607.23055},
  doi          = {10.48550/ARXIV.2607.23055},
  eprinttype   = {arXiv},
  eprint       = {2607.23055},
  timestamp    = {Tue, 11 Aug 2026 13:51:24 +0200},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2607-23055.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
