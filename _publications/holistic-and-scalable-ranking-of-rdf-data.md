---
layout: publication
title: "Holistic and scalable ranking of RDF data"
year: 2017
authors:
  - "Axel-Cyrille Ngonga Ngomo"
  - "Michael Hoffmann 0007"
  - "Ricardo Usbeck"
  - "Kunal Jha"
doi: "https://doi.org/10.1109/BIGDATA.2017.8257990"
is_conference: true
is_journal: false
is_archive: false
conference: "IEEE BigData 2017"
---

> **Abstract:**
> The volume and number of data sources published using Semantic Web standards such as RDF grows continuously. The largest of these data sources now contain billions of facts and are updated periodically. A large number of applications driven by such data sources requires the ranking of entities and facts contained in such knowledge graphs. Hence, there is a need for time-efficient approaches that can compute ranks for entities and facts simultaneously. In this paper, we present the first holistic ranking approach for RDF data. Our approach, dubbed HARE, allows the simultaneous computation of ranks for RDF triples, resources, properties and literals. To this end, HARE relies on the representation of RDF graphs as bi-partite graphs. It then employs a time-efficient extension of the random walk paradigm to bi-partite graphs. We show that by virtue of this extension, the worst-case complexity of HARE is O(n5) while that of PageRank is O(n6). In addition, we evaluate the practical efficiency of our approach by comparing it with PageRank on 6 real and 6 synthetic datasets with sizes up to 108triples. Our results show that HARE is up to 2 orders of magnitude faster than PageRank. We also present a brief evaluation of HARE's ranking accuracy by comparing it with that of PageRank applied directly to RDF graphs. Our evaluation on 19 classes of DBpedia demonstrates that there is no statistical difference between HARE and PageRank. We hence conclude that our approach goes beyond the state of the art by allowing the ranking of all RDF entities and of RDF triples without being worse w.r.t. the ranking quality it achieves on resources. HARE is open-source and is available at http://github.com/dice-group/hare.


