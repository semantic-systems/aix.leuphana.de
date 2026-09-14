---
layout: publication
title: "Transformer with Tree-order Encoding for Neural Program Generation"
year: 2022
authors:
  - "Klaudia-Doris Thellmann"
  - "Bernhard Stadler 0001"
  - "Ricardo Usbeck"
  - "Jens Lehmann 0001"
doi: "https://doi.org/10.48550/ARXIV.2206.13354"
is_conference: false
is_journal: false
is_archive: true
---

> **Abstract:**
> While a considerable amount of semantic parsing approaches have employed RNN architectures for code generation tasks, there have been only few attempts to investigate the applicability of Transformers for this task. Including hierarchical information of the underlying programming language syntax has proven to be effective for code generation. Since the positional encoding of the Transformer can only represent positions in a flat sequence, we have extended the encoding scheme to allow the attention mechanism to also attend over hierarchical positions in the input. Furthermore, we have realized a decoder based on a restrictive grammar graph model to improve the generation accuracy and ensure the well-formedness of the generated code. While we did not surpass the state of the art, our findings suggest that employing a tree-based positional encoding in combination with a shared natural-language subword vocabulary improves generation performance over sequential positional encodings.


<details markdown="1" style="margin-top: 1.5rem;">
  <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: var(--c-granit-20); border-radius: 6px;">Show BibTeX</summary>

{% raw %}
```bibtex
@article{DBLP:journals/corr/abs-2206-13354,
  author       = {Klaudia{-}Doris Thellmann and
                  Bernhard Stadler and
                  Ricardo Usbeck and
                  Jens Lehmann},
  title        = {Transformer with Tree-order Encoding for Neural Program Generation},
  journal      = {CoRR},
  volume       = {abs/2206.13354},
  year         = {2022},
  url          = {https://doi.org/10.48550/arXiv.2206.13354},
  doi          = {10.48550/ARXIV.2206.13354},
  eprinttype   = {arXiv},
  eprint       = {2206.13354},
  timestamp    = {Thu, 07 May 2026 20:22:14 +0200},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2206-13354.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
{% endraw %}
</details>
