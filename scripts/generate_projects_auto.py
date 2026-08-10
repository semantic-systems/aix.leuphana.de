import os

out_dir = "/Users/murat/Documents/SHK/Sysadmin/semantic-systems/aix.leuphana.de/aix.leuphana.de/_projects"
os.makedirs(out_dir, exist_ok=True)

projects = [
    {
        "filename": "provider.md",
        "title": "PROVIDER",
        "date": "2026-01-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "A BMFTR project to develop dynamic simulations and self-learning LLM agents for anticipating supply shortages. AIX leads work on neuro-symbolic information extraction and explainable event analysis.",
        "content": """The collaborative project PROVIDER develops an AI-supported early warning system for the early detection, analysis, and simulation of potential supply bottlenecks in Germany. The focus is on supply chains and supply systems that are relevant for everyday supply security, but do not necessarily belong to classical critical infrastructure. Many of these goods, logistics, and service chains are highly optimized, internationally interconnected, and particularly susceptible to disruptions from extreme weather events, geopolitical conflicts, production failures, transport issues, or societal crises.

PROVIDER aims to transition from reactive post-hoc analyses to a continuously operating, predictive system. For this purpose, heterogeneous data sources, current news flows, public data, economic information, and knowledge graphs are combined. On this basis, dynamic simulations are created to estimate potential bottlenecks and cascade effects over a period of several months. The project combines Knowledge Graphs, Large Language Models, agent-based simulation, Deep Reinforcement Learning, and Adversarial Resilience Learning.

The sub-project of Leuphana University Lüneburg focuses on neuro-symbolic AI for explainable information extraction and event analysis. The goal is to develop methods to detect, semantically classify, and make relevant events from structured and unstructured data sources (especially news flows) usable for the parameterization and evaluation of simulations. A special focus is on the use and adaptation of Large Language Models, the linkage with knowledge graphs, and the development of LLM-based agents that can generically access external interfaces.

Furthermore, Leuphana is developing an interactive evaluation tool with a natural language interface within the project. Users without computer science expertise should be able to query simulation results, visualize values and trends, and trace the origin and reasoning of the results. Thus, the sub-project contributes to making complex simulation results understandable, explainable, and usable for decision-making processes.

## Objectives
- Develop an AI-supported early warning system for supply bottlenecks.
- Combine heterogeneous data sources including knowledge graphs and large language models.
- Create dynamic simulations to estimate cascade effects.
- Develop an interactive evaluation tool with a natural language interface.
"""
    },
    {
        "filename": "rescue-mate.md",
        "title": "RESCUE-MATE",
        "date": "2024-01-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "A BMFTR project that uses real-time, geospatial, and social-media data to create dynamic crisis situation pictures and decision support for rescue services.",
        "content": """The RESCUE-MATE project aims to leverage real-time, geospatial, and social media data to construct dynamic situational awareness pictures during crises. By providing advanced decision support systems, the project assists rescue services in making informed and timely decisions during complex emergencies.

## Objectives
- Integrate real-time geospatial and social media data.
- Develop dynamic crisis situation pictures.
- Provide advanced decision support for rescue services.
"""
    },
    {
        "filename": "nfdi4datascience.md",
        "title": "NFDI4DataScience (NFDI4DS)",
        "date": "2024-01-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "DFG project on national research data infrastructure connecting publications, datasets, software, and models to make Data Science and AI research more FAIR, reproducible, and searchable.",
        "content": """NFDI4DataScience (NFDI4DS) follows a vision: for Data Science and the advancements in Artificial Intelligence, it is essential to fully support all steps of the complex and interdisciplinary lifecycle for research data, i.e., the collection/creation, processing, analysis, publication, archiving, and reuse of various resources. The paradigm shift in recent years has meant that the most powerful computational methods are increasingly achieved through data-driven approaches, especially Deep Learning. This has led to the establishment of Data Science as an independent and ubiquitous scientific discipline, driven by advances in computer science, but drawing its great significance from the diverse results in almost all scientific disciplines.

The challenges for Data Science and AI lie in mastering modern Data Science methods by implementing the principles of transparency, reproducibility, and fairness for digital objects (i.e., for the combination of code, models, and data used for training). Due to the outstanding importance of Data Science and AI for computer science and for the broader spectrum of many scientific disciplines, NFDI4DS will open its research data infrastructures to bring all available resources such as code, models, data, or publications into the scientific communities.

NFDI4DS pursues the development, establishment, and maintenance of a national research data infrastructure for the Data Science and Artificial Intelligence communities in Germany. This also offers advantages for a broader community that relies on data analysis solutions (e.g., within the NFDI). The ultimate goal is that all digital artifacts are made available, linked together, and innovative tools and services are offered to enable new and innovative research through diverse reuse.

In the initial phase, NFDI4DS will focus on four application areas that are particularly prominent in data science: language technology, life sciences, information sciences, and social sciences.

## Objectives
- Support the entire lifecycle of research data in Data Science and AI.
- Ensure transparency, reproducibility, and FAIRness of models, data, and code.
- Build a national research data infrastructure for the AI and Data Science communities.
- Foster collaboration across disciplines including language technology, life sciences, information, and social sciences.
"""
    },
    {
        "filename": "llms-clinical-research.md",
        "title": "LLMs for Clinical-Research Data Extraction",
        "date": "2024-09-01",
        "status": "Completed",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "BMFTR project with DZHK and UKE, which uses large language models to extract structured clinical information from discharge letters and other medical documents.",
        "content": """Acute heart failure including cardiogenic shock is a life-threatening condition with high 30-day mortality up to 60%. In order to understand these critical conditions better, large registries are being established. These are most valuable primarily in generating hypotheses for further assessment, usually performed in randomized controlled trials (RCTs). These trials permit insights into causal relationships between medical interventions (like the use of novel medical drugs or mechanical circulatory support devices like the veno-arterial extracorporeal membrane oxygenation, so-called VA-ECMO) and patient outcomes.

Unfortunately, building the registries as well as performing RCTs are labor-intensive endeavors and, thus, both time-consuming and costly. Leveraging existing data collected from clinical routine is of utmost importance to advance the research in understanding critical conditions. Increasing the rate of patient recruitment by better embedding research-related tasks into clinical routine will reduce RCT durations necessary to obtain sufficient numbers of patients.

Applying artificial intelligence (AI) through large language models (LLMs) addresses this need: Much information of interest to the clinical researcher is contained in discharge letters from hospitals in a more or less structured way. Instead of spending labor force to collect these data, applying AI is a valuable and cost-saving alternative.

## Objectives
- Automate data extraction from clinical discharge letters using LLMs.
- Support the creation of large registries for critical conditions like acute heart failure.
- Reduce the time and cost associated with conducting randomized controlled trials (RCTs).
- Improve patient recruitment by integrating research tasks into the clinical routine.
"""
    },
    {
        "filename": "creative-space.md",
        "title": "Creative Space for Human and Artificial Intelligence",
        "date": "2025-10-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "An open, project-based experimentation, learning, and advisory space where students from all disciplines explore AI and data literacy through hands-on, curiosity-driven, interdisciplinary collaboration.",
        "content": """Based on the Creative Space concept (open, project-based experimentation spaces in technologically complex research areas like Artificial Intelligence for all students at Leuphana), we want to establish a Creative Space with this project. Especially in the various fields of AI, conveying complex technological backgrounds is difficult (abstraction, complexity reduction without simplification), while at the same time it will be essential for students of all disciplines to engage with these key technologies. A basic AI competence and Data Literacy in this area is helpful to necessary for all disciplines looking into the future.

The Creative Space serves as a place that is experimentally open, acts as a first point of contact and advisory center for students, and integrates skills and teaching modules across disciplinary boundaries.

The Creative Space relies on three basic principles to support the free, self-determined, and joyful design of learning and design experiences for students:

- **Boundary Objects as objects for debates:** Artifacts that can be interpreted differently by different disciplines and therefore promote discussions and interdisciplinary communication.
- **Improvisation and Curiosity-driven Research:** With this approach, the focus is on playful and exploratory discovery. Instead of strictly adhering to predetermined methods or results, students are encouraged to gain new insights and develop innovative projects through spontaneous ideas and their own curiosity.
- **Strict Inter- to Transdisciplinarity:** By incorporating knowledge and methods from different disciplines, a more comprehensive and flexible problem-solving approach is enabled.

## Objectives
- Establish a Creative Space for AI and Data Literacy for students of all disciplines.
- Foster interdisciplinary and transdisciplinary collaboration.
- Encourage curiosity-driven research and playful exploration of AI technologies.
"""
    },
    {
        "filename": "mobile-ai-workstations.md",
        "title": "Mobile AI Workstations",
        "date": "2025-10-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "A SQM project provides mobile, GPU-capable workstations to enable equitable student access to AI development.",
        "content": """Artificial Intelligence is rapidly gaining importance – in research, business, and society. To prepare students of all disciplines specifically for this development, they need access to powerful tools and development environments. Currently, many – especially outside the Business Informatics and Data Science programs – lack suitable hardware to realize their own, more complex AI applications.

As a smaller university with limited resources, Leuphana cannot currently provide all students in interdisciplinary programs with the necessary infrastructure. However, it is essential that all students are given the opportunity to not only understand key technologies like AI theoretically but to test them practically.

This project addresses exactly this issue: The plan is to purchase four mobile, fully equipped AI workstations. These are based on the concept of a temporary, nomadic experimentation laboratory and contain a powerful NVIDIA SPARK AI chip, two monitors, input devices, and materials for group work – safely housed in robust flight cases.

Thanks to their mobility, the stations can be flexibly integrated into various teaching formats – from seminars and projects to Leuphana-wide events like the Starting Week or Teaching Day, up to public events like the Minor AI Conference or exhibitions. They not only strengthen teaching but also increase the visibility of student work and AI competence at Leuphana in connection with the Leuphana AI Campus (LAICA).

## Objectives
- Provide equitable access to high-performance AI hardware for students across all disciplines.
- Procure and deploy four mobile, fully equipped AI workstations.
- Integrate the mobile labs into diverse teaching formats and public events.
"""
    },
    {
        "filename": "student-ai-server.md",
        "title": "Student AI Server",
        "date": "2025-10-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "An SQM project establishes and operates a shared GPU server infrastructure for students’ machine learning and AI projects.",
        "content": """The Artificial Intelligence and Explainability (AIX) research group led by Prof. Dr. Ricardo Usbeck has applied for funding for a student assistant (SHK) to set up and maintain a computing server equipped with graphics processing units (GPUs), hosted at the MIZ. The goal is to improve the education of our disciplinary students in the areas of Artificial Intelligence, Deep Learning, and related entrepreneurial skills.

Currently, students at Leuphana lack the necessary infrastructure to train, test, and deploy AI models using GPU computing. This project closes this critical gap. We are securing the funding for the server hardware separately and will virtualize it into two instances: one for hosting AI demonstrations developed by students in our courses, thereby promoting the visibility of projects and mutual learning. The second instance will be used for teaching and practical application in the training and fine-tuning of Deep Learning models, including small to medium-sized LLMs. The SHK will ensure intuitive and accessible use of the server for students.

## Objectives
- Establish and operate a shared GPU server infrastructure for students.
- Host student-developed AI demonstrations to promote visibility and mutual learning.
- Provide a platform for practical application in training and fine-tuning Deep Learning models.
- Ensure intuitive and accessible usage for all students.
"""
    },
    {
        "filename": "lstartuplab.md",
        "title": "LStartupLab – Leuphana Startup Lab for Innovation, Transformation & Entrepreneurship",
        "date": "2025-08-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "EFRE central startup platform combining qualification programs, innovation spaces, and partner networks, with a particular focus on Data Science and AI.",
        "content": """With the LStartupLab, a central platform for the promotion of business start-ups is being created at Leuphana University Lüneburg. The project bundles qualification programs for university members interested in founding a company, modernly equipped innovation spaces, and a strong network of regional and national partners on campus. It places a special focus on Data Science and Artificial Intelligence.

## Objectives
- Establish a central platform on campus for business start-ups and entrepreneurship.
- Provide qualification programs, innovation spaces, and a strong partner network.
- Focus specifically on fostering start-ups in the areas of Data Science and Artificial Intelligence.
"""
    },
    {
        "filename": "hdn-ds3.md",
        "title": "HdN – Lower Saxony Digital Science Support Space (DS³)",
        "date": "2025-07-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "State-wide joint project building shared digital research infrastructure, computing resources, research-data services, and local support structures for researchers across Lower Saxony.",
        "content": """The Lower Saxony Digital Science Support Space (DS³) is a state-wide joint project aimed at building a shared digital research infrastructure. Supported by the Lower Saxony Ministry of Science and Culture and the Volkswagen Foundation, this initiative provides comprehensive computing resources, research-data services, and local support structures to empower researchers across Lower Saxony.

## Objectives
- Build a robust and shared digital research infrastructure across Lower Saxony.
- Provide accessible computing resources and research-data services.
- Establish local support structures to assist researchers in their digital science endeavors.
"""
    },
    {
        "filename": "humaine.md",
        "title": "HumAIne - Learning from Humans",
        "date": "2025-08-01",
        "status": "Ongoing",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "EFRE/STEP research infrastructure initiative for human-centered AI, concerned with integrating AI into working processes while improving working and living conditions.",
        "content": """HumAIne is an EFRE/STEP research infrastructure initiative focused on human-centered AI. The project is primarily concerned with integrating Artificial Intelligence into everyday working processes, ensuring that these technological advancements lead to improvements in both working and living conditions for individuals.

## Objectives
- Promote the development and adoption of human-centered AI.
- Integrate AI smoothly into existing working processes.
- Ensure AI applications improve overall working and living conditions.
"""
    },
    {
        "filename": "coypu.md",
        "title": "CoyPu – Cognitive Economy Intelligence Platform for Resilience of Economic Ecosystems",
        "date": "2021-06-01",
        "status": "Completed",
        "thumbnail": "/assets/images/blank.png",
        "excerpt": "BMWK project to develop an AI platform using linked knowledge graphs to analyze supply chains, economic ecosystems, and crisis-related risks, particularly for SMEs.",
        "content": """The project "Cognitive Economy Intelligence Platform for Economic Ecosystem Resilience (CoyPu)" addresses AI methods for resilient ecosystems.

Partners include DATEV eG, Siemens AG, Infineon Technologies AG, the German Institute for Economic Research (DIW), the Hamburger Informatik Technologie-Center e.V. (HITeC), the Research Center L3S, the Leibniz Information Center Technology and Natural Sciences (TIB) of the University of Hannover, eccenca GmbH, Implisense GmbH, and Selbstregulierung Informationswirtschaft e.V.

AIX (formerly SEMS at HITeC e.V.) is the core technology partner leading the work package on artificial intelligence and explainability. We will explore methods for knowledge extraction, event prediction, and explainability. We will rely on a combination of Hybrid AI, deep learning, and knowledge graphs.

## Objectives
- Develop an AI platform using linked knowledge graphs to analyze economic ecosystems.
- Enhance the resilience of supply chains and assess crisis-related risks, especially for SMEs.
- Explore methods for knowledge extraction, event prediction, and explainability through Hybrid AI.

**Video:** CoyPu Introduction Video - https://coypu.org/media/MST_02_CoyPu_Forschungsprojekt_21-036.mp4  
**Project website:** [coypu.org](https://coypu.org)  
**Twitter:** @CoypuProject  
"""
    }
]

template = '''---
layout: project
title: "{title}"
date: {date} # Format exactly like this: YYYY-MM-DD. This controls the sorting order (newest first)
status: "{status}" # e.g. "Ongoing", "Completed", "In Review"
thumbnail: "{thumbnail}" # Square preview image for the main Projects list
image: "{thumbnail}" # Large banner image inside the actual project page (optional)
excerpt: "{excerpt}"
published: true # Change this to 'true' when you want it to appear on the live website!
---

{content}
'''

for proj in projects:
    file_content = template.format(**proj)
    filepath = os.path.join(out_dir, proj["filename"])
    with open(filepath, "w") as f:
        f.write(file_content)

print("Generated 11 projects successfully.")
