---
title: "Georelating: Inferring Disaster-Affected Areas from Textual Reports"
authors:
  - "Kai Moltzen"
  - "Junbo Huang"
  - "Ricardo Usbeck"
year: 2025
github_repo: "https://github.com/semantic-systems/SIGSPATIAL2025-Georelating"
github_page: "https://semantic-systems.github.io/SIGSPATIAL2025-Georelating/"
abstract: "Accurately identifying disaster-affected areas is crucial for data-driven disaster resilience. In response, we introduce Georelating, a task that infers affected areas from textual reports containing complex locative expressions."
conference: "ACM SIGSPATIAL 2025"
doi: "https://doi.org/10.1145/3748636.3762733"
layout: publication
permalink: /publications/georelating-inferring-disaster-affected-areas/
---

<style>
  .publication-content {
    line-height: 1.78;
    color: var(--text-primary);
  }


  /* Teaser figure */
  .teaser {
    margin: 2.75rem 0;
    text-align: center;
  }
  .teaser img {
    width: 100%; border-radius: 10px;
    box-shadow: 0 4px 28px rgba(0,0,0,0.10);
    display: block;
  }
  .teaser figcaption {
    font-size: 0.85rem; color: var(--text-secondary);
    margin-top: 0.85rem; line-height: 1.6; text-align: left;
  }
  .teaser figcaption strong { color: var(--text-primary); }

  /* Pull quote */
  .pub-quote {
    border-left: 3px solid var(--c-granit-40);
    margin: 1.4rem 0;
    padding: 0.5rem 1.3rem;
    color: var(--text-secondary);
    font-style: italic;
  }

  /* TL;DR */
  .tldr {
    background: var(--c-granit-20);
    border-left: 3px solid var(--c-jaspis);
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.25rem;
    margin: 1.4rem 0 0;
    font-size: 0.95em;
  }
  .tldr strong { color: var(--c-jaspis); }

  /* Definition box */
  .definition {
    background: var(--c-granit-20);
    border: 1.5px solid var(--c-orange);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin: 1.75rem 0;
  }
  .definition .def-head {
    font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.07em;
    color: var(--c-orange); margin-bottom: 0.85rem;
  }
  .definition p { margin-bottom: 0.7em; }
  .definition ul { margin: 0.4rem 0 0.85rem 1.3rem; }

  /* Research questions */
  .rq {
    background: var(--c-granit-20);
    border-radius: 8px;
    padding: 0.75rem 1.2rem;
    margin: 0.85rem 0;
    font-style: italic;
  }
  .rq strong { font-style: normal; color: var(--c-jaspis); }

  /* Pipeline steps */
  .pipeline {
    display: flex;
    gap: 0;
    margin: 1.75rem 0;
    border: 1px solid var(--c-granit-40);
    border-radius: 10px;
    overflow: hidden;
  }
  .pipeline-step {
    flex: 1;
    padding: 1rem 1.1rem;
    border-right: 1px solid var(--c-granit-40);
  }
  .pipeline-step:last-child { border-right: none; }
  .step-num {
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--c-orange); margin-bottom: 0.3rem;
  }
  .step-title { font-weight: 600; margin-bottom: 0.3rem; color: var(--text-primary); }
  .step-desc { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.45; }

  /* Tables */
  .table-wrap { overflow-x: auto; margin: 1.5rem 0; border-radius: 8px; border: 1px solid var(--c-granit-40); }
  table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
  thead tr { background: var(--c-granit-20); }
  th, td { padding: 0.55rem 0.85rem; border-bottom: 1px solid var(--c-granit-40); text-align: center; white-space: nowrap; }
  th { font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }
  tbody tr:last-child td { border-bottom: none; }
  tbody tr:hover { background: var(--c-granit-20); }
  td:first-child, th:first-child { text-align: left; }
  .best { font-weight: 700; color: var(--c-jaspis); }
  .sota { font-weight: 700; color: var(--c-orange); }
  .table-note { font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.5; }

  /* Citation */
  .bibtex {
    background: var(--c-granit-20); border: 1px solid var(--c-granit-40); border-radius: 8px;
    padding: 1.25rem 1.5rem; font-family: monospace; font-size: 0.85rem;
    line-height: 1.75; overflow-x: auto; white-space: pre; position: relative;
  }
  .copy-btn {
    position: absolute; top: 0.75rem; right: 0.75rem;
    font-size: 0.8rem; font-weight: 500;
    padding: 0.22rem 0.65rem; border-radius: 5px; border: 1.5px solid var(--c-granit-40);
    background: var(--bg-primary); cursor: pointer; color: var(--text-secondary); transition: all 0.15s;
  }
  .copy-btn:hover { background: var(--c-jaspis); border-color: var(--c-jaspis); color: #fff; }

  @media (max-width: 640px) {
    .pipeline { flex-direction: column; }
    .pipeline-step { border-right: none; border-bottom: 1px solid var(--c-granit-40); }
    .pipeline-step:last-child { border-bottom: none; }
  }
</style>



<figure class="teaser">
  <img src="{{ '/assets/images/Georelating_overview.png' | relative_url }}" alt="Illustration of Georelating: a wildfire report mentioning landmarks Moorpark and Somis is parsed to a DGGS cell representing the area between them.">
  <figcaption>
    <strong>Figure 1.</strong> Georelating parses a natural disaster's impact area described in text to a Discrete Global Grid System (DGGS) cell by interpreting complex locative expressions, which contain <u>spatial relations</u> and <em>landmark toponyms</em> (highlighted in the disaster report). The output cell covers the unnamed area <em>between</em> the communities of Moorpark and Somis where the wildfire broke out.
  </figcaption>
</figure>

## Abstract
<p>Accurately identifying disaster-affected areas is crucial for data-driven disaster resilience. In response, we introduce <strong>Georelating</strong>, a task that infers affected areas from textual reports containing complex locative expressions, moving beyond traditional geoparsing approaches that rely on explicit point locations. Georelating instead combines resolving unnamed regions and reasoning about spatial relations to represent event-affected areas within standardized <strong>Discrete Global Grid Systems (DGGSs)</strong>.</p>

<p>We propose addressing Georelating with a pipeline capitalizing on the contextual understanding of large language model (LLM) agents to perform geospatial reasoning. Preliminary evaluation highlights the potential of this approach for the foundational geocoding stage and the novel Georelating task. We point out future paths for enhancing Georelating systems toward intuitive and efficient disaster information systems.</p>

<div class="tldr">
  <strong>TL;DR:</strong> We introduce Georelating — inferring unnamed disaster-affected areas from relational language in text — and solve it with a reflective LLM multi-agent pipeline grounded in GeoNames and H3 DGGS APIs, achieving near state-of-the-art geocoding without fine-tuning.
</div>

## Introduction

<p>The increasing frequency and impact of natural disasters necessitate robust resilience strategies, prompting the development of national and international frameworks. A core aspect of these strategies involves geo-referencing damage information to facilitate disaster risk management. Natural language (NL) reports, such as news articles, provide timely insights into the impacts of global disasters — but effectively using this data requires addressing the challenges of spatially describing these disasters.</p>

<p>Current geoparsing approaches often rely on identifying place names (toponyms) and mapping them to geographic coordinates. However, natural disasters rarely conform to administrative boundaries, and NL reports frequently employ relational language to define affected areas. Furthermore, exhaustively listing all vulnerable entities in text is often impractical. Instead of directly identifying impacted entities, we propose <em>inferring the area</em> affected by a disaster from NL reports and integrating this information with existing geographic and demographic knowledge.</p>

<p>This work dissects the challenges of Georelating and explores the potential of large language models (LLMs) to address them, centering on two research questions:</p>

<div class="rq">
  <strong>(RQ1)</strong> How can we formally define the task of Georelating?
</div>
<div class="rq">
  <strong>(RQ2)</strong> How to design an LLM agent architecture for Georelating?
</div>

<p>For <strong>RQ1</strong>, we discuss the limitations of current geo-referencing tasks that match toponyms to known locations. Georelating requires inferring areas defined by relational language that lack explicit boundaries. We represent a disaster's impact area using DGGS cells and leverage complex locative expressions with <em>landmarks</em> as reference points and <em>spatial relations</em> leading to the report's <em>trajector</em>.</p>

<p>For <strong>RQ2</strong>, we propose and implement a reflective, LLM-driven multi-agent architecture comprising a dynamic memory module, actor and critic agents for reasoning and self-correction, a validation procedure, and an external environment grounded in the GeoNames gazetteer and the H3 DGGS API.</p>

## The Georelating Task

<p>Consider the following example disaster report:</p>

<div class="pub-quote">
  "Firefighters at the scene of the brush fire, which broke out <u>between the communities of Moorpark and Somis</u>, 'were faced with a tough firefight,' Ventura County Fire Capt. Trevor Johnson said."
</div>

<p>Traditional geoparsing resolves toponyms such as "Moorpark," "Somis," and "Ventura" to point-based geographical database entries — the <em>landmarks</em> (blue markers in Figure 1). This fails to represent the <em>extent</em> of events like wildfires, i.e., the <em>trajector</em>. Georelating overcomes this by reasoning about spatial relations and context to represent unnamed impact areas.</p>

<p>The most relevant spatial relations for disaster reports are positional ones — particularly direction-based (e.g., cardinal direction "North," ternary relation "between") and distance-based (e.g., qualitative "near," quantitative "24 meters") calculi. Georelating becomes crucial for spatiotemporal events where positions evolve and are not readily available in gazetteers.</p>

<p>To represent such areas effectively, we propose using <strong>Discrete Global Grid Systems (DGGSs)</strong> — spatial indexing systems that partition Earth's surface into hierarchically organized, regularly tiling cells, each with a unique permanent identifier. DGGS representations facilitate scalable analysis, interoperability, cross-domain data integration with Geospatial Knowledge Graphs (GeoKGs), and intuitive visualization.</p>

<div class="definition">
  <div class="def-head">Definition 1 — Georelating</div>
  <p>Georelating is the task of inferring the index of the <strong>smallest cell</strong> in a DGGS that fully encompasses the area affected by a distinct geospatial-temporal event, as described in an NL report.</p>
  <p><strong>Input:</strong></p>
  <ul>
    <li>An NL report <em>R</em> containing one or more complex locative expressions involving toponyms used as landmarks and spatial relations.</li>
    <li>A DGGS partitioned into hierarchical levels, where <em>G_l</em> is the set of all cells at level <em>l</em> (higher <em>l</em> = finer resolution).</li>
  </ul>
  <p><strong>Define:</strong> Let <em>A</em> be the affected area inferred from <em>R</em>, and let <em>C_A</em> be the set of all cells at any level <em>l</em> that completely cover <em>A</em>.</p>
  <p><strong>Task:</strong> Select the minimally sized covering cell <em>c* = arg min size(c) = arg max l(c)</em> for <em>c in C_A</em>.</p>
  <p><strong>Output:</strong> The index of cell <em>c*</em> in the DGGS.</p>
</div>

<p>The central innovation is to combine resolving toponyms as landmarks with reasoning about spatial relations and article context to determine the unnamed, impacted region. The DGGS approach provides efficient representation and facilitates GeoKG integration.</p>

## LLM Agents for Georelating

<p>We present a reflective, LLM-based agentic architecture for Georelating, detailing its components, operations, and interplay.</p>

<h3>Architecture Components</h3>
<p>Our architecture comprises four key components: LLM-driven <em>language agents</em> for reasoning and task execution, a hybrid <em>memory</em> for integrating relevant information, <em>internal procedures</em> for validation and coordination, and access to an <em>external environment</em> via APIs for geographical grounding.</p>

<h4>Memory</h4>
<p>We employ a hybrid memory consisting of short-term, long-term, and working memory. <strong>Short-term memory</strong> stores positive examples for few-shot learning and feedback on errors within the current execution cycle. <strong>Long-term memory</strong> contains procedural knowledge (code and agent prompts, implemented with LangChain) and semantic knowledge (detailed instructions and API documentation). <strong>Working memory</strong> is dynamically constructed, including the input report, system prompt, task instructions, and relevant examples retrieved via semantic (cosine) similarity between vector embeddings of the example and the input report.</p>

<h4>Language Agents</h4>
<p>Inspired by reinforcement learning, our architecture uses <strong>actor</strong> and <strong>critic</strong> agents. Actors solve Georelating sub-tasks; critics provide verbal error feedback for self-correction. LLMs are leveraged for both, capitalizing on their NL understanding for geospatial reasoning across text domains (news articles, social media). Actors and critics run as independent, stateless instances.</p>

<h4>Internal Procedures &amp; External Environment</h4>
<p>LLM outputs are first validated for syntax, then undergo deterministic coherence validation (e.g., verifying referenced toponyms). Errors trigger analysis and reflection by the critic agent. Actors ground decisions in accurate geographical knowledge via read-only access to the <strong>GeoNames gazetteer</strong> and the <strong>H3 DGGS API</strong>, preventing persistent state changes.</p>

<h4>Learning and Refinement</h4>
<p>Three methods enhance performance throughout the pipeline: (I) instruction fine-tuned LLMs ensure task adherence; (II) few-shot learning provides contextual guidance; (III) the actor-critic framework enables iterative improvement — the critic analyzes unsuccessful generations and provides actionable feedback, and the actor's working memory is updated with this feedback and the current trajectory to facilitate task-specific learning. The model-independent design ensures compatibility with future LLMs.</p>

<h3>Georelating Pipeline</h3>
<p>The pipeline mirrors the structure of complex locative expressions: landmarks (toponyms) are resolved first, then spatial relations are reasoned over to locate the trajector. Based on the hypothesis that humans first identify landmarks and then reason about spatial relations, our pipeline consists of three steps:</p>

<div class="pipeline">
  <div class="pipeline-step">
    <div class="step-num">Step 1</div>
    <div class="step-title">Candidate Generation</div>
    <div class="step-desc">An actor queries the GeoNames API to identify potential toponym matches. Custom validation functions verify generated API parameters; failures trigger critic intervention and actor retry.</div>
  </div>
  <div class="pipeline-step">
    <div class="step-num">Step 2</div>
    <div class="step-title">Candidate Resolution</div>
    <div class="step-desc">A refined actor selects the best-fitting candidate per toponym. Due to potentially lengthy prompts (multiple toponyms, up to ten candidates each), one consistent one-shot example is provided.</div>
  </div>
  <div class="pipeline-step">
    <div class="step-num">Step 3</div>
    <div class="step-title">Geospatial Reasoning</div>
    <div class="step-desc">An actor interprets resolved coordinates and spatial relations to estimate the event's center and extent, then queries the H3 API to determine the DGGS cell index encompassing the predicted area.</div>
  </div>
</div>

<p>Toponyms are extracted as a preliminary step using the widely adopted <strong>Stanza Named Entity Recognition</strong> pipeline before candidate generation begins.</p>

## Preliminary Evaluation

<p>We briefly evaluate our architecture on the foundational candidate generation and resolution stages using the established <strong>Local-Global Lexicon corpus (LGL)</strong> for robust comparisons with prior work. For a first approximation to Georelating, we employ <strong>GeoCoDe</strong> as the only dataset explicitly tailored to complex location descriptions and polygon annotations.</p>

<h3>Evaluation Methodology</h3>
<p>For actors and critics, we evaluate three LLMs: the small and fast <strong>LLaMA 3.1 8B Instruct (8b)</strong>, the large <strong>LLaMA 3.3 70B Instruct (70b)</strong>, and <strong>Mistral Large Instruct (123b)</strong>.</p>
<p><strong>Candidate generation</strong> is evaluated with Recall@k — the proportion of ground truth GeoNames IDs among the top-k retrieved candidates — reporting R@10 for comparability. <strong>Candidate resolution</strong> uses Accuracy@k (A@161) and AUC over the distribution of geodesic error distances. <strong>Georelating</strong> is evaluated using areal F₁ — the harmonic mean of precision and recall over the overlap of predicted and ground truth polygons.</p>

<h3>Results</h3>

<h4>Candidate Generation &amp; Resolution (LGL)</h4>
<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Actor</th>
        <th>Critic</th>
        <th>R@10 &uarr;</th>
        <th>A@161 &uarr;</th>
        <th>AUC &darr;</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>8b</td><td>&mdash;</td><td>0.682</td><td>0.825</td><td>0.103</td></tr>
      <tr><td>8b</td><td>8b</td><td>0.767</td><td>0.825</td><td>0.101</td></tr>
      <tr><td>8b</td><td>123b</td><td>0.775</td><td>0.837</td><td>0.102</td></tr>
      <tr><td>70b</td><td>123b</td><td class="best">0.873</td><td class="best">0.862</td><td class="best">0.073</td></tr>
      <tr style="background:var(--bg-secondary);">
        <td colspan="2" style="color:var(--text-secondary);font-style:italic;">Previous State of the Art</td>
        <td class="sota">0.759</td><td class="sota">0.906</td><td class="sota">0.109</td>
      </tr>
    </tbody>
  </table>
</div>
<p class="table-note">All critics consistently improve R@10. The 8b + 8b pair already surpasses recent transformer-based models. The 70b + 123b combination achieves the best results across all metrics, with A@161 = 0.862 approaching the state-of-the-art 0.906, and AUC = 0.073 substantially improving upon the previously best reported 0.109. At least one toponym is resolved within 161 km in <strong>92% of all articles</strong>, supporting general event localization.</p>

<h4>Georelating (GeoCoDe)</h4>
<div class="table-wrap">
  <table>
    <thead>
      <tr><th>Model</th><th>A@161 &uarr;</th><th>AUC &darr;</th><th>Areal F₁ &uarr;</th></tr>
    </thead>
    <tbody>
      <tr><td>70b + 123b</td><td>1.000</td><td>0.213</td><td>0.170</td></tr>
    </tbody>
  </table>
</div>
<p class="table-note">The 70b model achieves perfect A@161 and low AUC on GeoCoDe, demonstrating strong spatial localization. The areal F₁ = 0.170 reflects the increased complexity of Georelating: the model substantially underestimates the area of described geographical units. Note that GeoCoDe contains named regions with fixed bounds, contrasting the goal of Georelating to resolve unnamed, evolving borders, which limits the explanatory power of these results.</p>

## Discussion &amp; Future Work

<p>Our reflective, LLM-driven agent architecture mirrors the structure of locative expressions by resolving toponyms before reasoning geospatially to approximate the extent and location of areas. Achieving geocoding performance comparable to specialized models on LGL news articles <em>without fine-tuning on labeled data</em>, it still requires further evaluation regarding the critic's influence and various LLMs.</p>

<p>The low areal F₁ highlights the increased complexity of the new Georelating task, though the explanatory power of these results is limited. GeoCoDe only contains named regions with fixed bounds, contrasting the goal of Georelating to resolve unnamed, evolving borders. Its polygon annotations also do not match the task definition's cell-based representation. We will therefore work on a <strong>new dataset</strong> of disaster reports containing relational geospatial descriptions annotated with DGGS identifiers, alongside tailored evaluation metrics capitalizing on the efficient DGGS grid hierarchy and traversal functions.</p>

<p>A current limitation is representing elongated areas with a single DGGS cell. We maintain, however, that DGGSs' representational and integrative advantages outweigh these drawbacks, and encourage future work on <strong>extending Georelating to multiple cells</strong> for more nuanced area resolution.</p>

<p>Because our method relies on textual descriptions, it is inherently bound by the precision of available sources. Nonetheless, textual information is abundant, making it practical for comprehensive and rapid disaster assessments. Future work could consider GeoAI methods to learn spatial representations directly from NL text, requiring geospatial reasoning for interpretation.</p>

## Conclusion

<p>We proposed <strong>Georelating</strong> — inferring the smallest DGGS cell fully encompassing the area affected by a geospatial-temporal event from NL reports, requiring the interpretation of spatial relations. By representing outputs as DGGS cells, Georelating enables integration with information stored in Geospatial Knowledge Graphs. We proposed an LLM agent architecture grounded in geographical knowledge, demonstrating highly competitive performance on geocoding foundational to Georelating. The system further shows its potential in geospatial reasoning to resolve regions.</p>

<p>We envision Georelating systems as a step toward intuitive disaster information systems that aggregate global event data, ultimately strengthening societal resilience.</p>

## Citation

<p>If you find this work useful, please cite:</p>

<div style="position:relative;">
<pre class="bibtex" id="bibtex-block">@inproceedings{moltzen2025georelating,
  author    = {Moltzen, Kai and Huang, Junbo and Usbeck, Ricardo},
  title     = {LLM Agents for Georelating - A New Task for Locating Events},
  booktitle = {Proceedings of the 33rd ACM SIGSPATIAL International Conference
               on Advances in Geographic Information Systems},
  year      = {2025},
  publisher = {ACM},
  url       = {https://github.com/semantic-systems/SIGSPATIAL2025-Georelating}
}</pre>
  <button class="copy-btn" onclick="copyBibtex()" id="copy-btn">Copy</button>
</div>

<script>
  function copyBibtex() {
    const text = document.getElementById('bibtex-block').innerText;
    navigator.clipboard.writeText(text).then(() => {
      const btn = document.getElementById('copy-btn');
      btn.textContent = 'Copied!';
      setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
    });
  }
</script>