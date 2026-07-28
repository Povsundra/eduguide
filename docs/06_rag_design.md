# 06. Retrieval-Augmented Generation (RAG) Design

**Document Version:** 1.0

**Project:** EduGuide – An Agentic Retrieval-Augmented Decision Support System for Personalized Higher Education Guidance in Cambodia

---

# 1. Purpose

This document defines the Retrieval-Augmented Generation (RAG) architecture of the EduGuide platform.

Unlike traditional chatbot architectures that rely solely on Large Language Models, EduGuide combines a Knowledge Graph, semantic vector retrieval, and Large Language Models into a Hybrid Graph RAG architecture capable of delivering accurate, explainable, and personalized educational guidance.

This document serves as the engineering blueprint for implementing the RAG subsystem.

It specifies:

- knowledge repository design
- knowledge ingestion pipeline
- document preprocessing
- semantic chunking
- embedding generation
- vector indexing
- query understanding
- graph retrieval
- semantic retrieval
- hybrid retrieval fusion
- response generation
- evaluation strategy

The RAG subsystem is designed to work together with the Knowledge Graph defined in **05_graph_design.md**, providing semantic understanding while preserving the structured reasoning capabilities of Neo4j.

---

# 2. Design Objectives

The RAG subsystem is designed to achieve the following objectives.

---

## 2.1 Provide Accurate Educational Information

Students should receive information grounded in official university knowledge rather than relying on the language model's internal knowledge.

All responses should originate from the EduGuide knowledge repository.

---

## 2.2 Support Explainable Recommendations

Every recommendation should be supported by evidence.

The system should be able to explain:

- why a university is recommended
- why a scholarship is suggested
- why a program matches the student's interests

The retrieved evidence should always be traceable back to the original knowledge source.

---

## 2.3 Combine Symbolic and Semantic Knowledge

Educational guidance requires two complementary retrieval methods.

Structured knowledge such as relationships between universities, programs, scholarships, and careers should be retrieved from the Knowledge Graph.

Descriptive knowledge such as curriculum descriptions, scholarship details, admission guides, and career information should be retrieved semantically from vector embeddings.

The RAG subsystem combines both retrieval methods before generating the final response.

---

## 2.4 Preserve Knowledge Consistency

The Knowledge Repository shall act as the single source of truth.

Both the Knowledge Graph and Vector Index must be generated from the same Markdown knowledge base to eliminate inconsistencies between structured and unstructured knowledge.

---

## 2.5 Support Personalized Educational Guidance

The RAG architecture should support personalized questions such as:

- Which university should I choose?
- Which scholarship fits my GPA?
- Which major matches my interests?
- What careers are suitable for me?

The retrieval process should consider user intent and available educational knowledge.

---

## 2.6 Minimize Hallucination

The language model should never answer educational questions without supporting evidence.

If sufficient evidence cannot be retrieved, the system should explicitly indicate that the information is unavailable instead of generating unsupported content.

---

# 3. Design Principles

The RAG subsystem follows the following engineering principles.

---

## 3.1 Knowledge-First Architecture

The LLM is not treated as the primary knowledge source.

Instead:

Knowledge Repository

↓

Knowledge Graph

+

Vector Index

↓

LLM

The language model is responsible for reasoning and language generation, while factual knowledge remains outside the model.

---

## 3.2 Single Source of Truth

All educational knowledge originates from standardized Markdown entity files.

Example

knowledge/

    universities/

    programs/

    curriculum/

    scholarships/

    admission/

    careers/

Every downstream component—including Neo4j, Vector Index, and Retrieval Pipeline—is generated from this repository.

---

## 3.3 Separation of Responsibilities

Each component has a clearly defined responsibility.

| Component | Responsibility |
|------------|----------------|
| Markdown Repository | Knowledge storage |
| Parser | Extract structured information |
| Neo4j | Structured reasoning |
| Chunking Module | Semantic segmentation |
| Embedding Module | Vector generation |
| Vector Index | Semantic retrieval |
| Retrieval Engine | Information retrieval |
| LLM | Response generation |

Each component performs one responsibility only.

---

## 3.4 Explainability

Every generated response must be explainable.

The retrieval pipeline should preserve:

- source file
- entity
- section
- graph path

allowing the system to justify every recommendation.

---

## 3.5 Modularity

Each subsystem should be independently replaceable.

Examples:

Embedding Model

↓

can be replaced

Neo4j Vector

↓

can be replaced

LLM

↓

can be upgraded

without affecting the remaining architecture.

---

## 3.6 Extensibility

Future educational entities should integrate without redesigning the retrieval architecture.

Future examples include:

- Faculty
- Subject
- Skill
- Occupation
- Internship

The retrieval pipeline should automatically support new entities through metadata rather than custom logic.

---

# 4. Hybrid Graph RAG Architecture

## 4.1 Overview

EduGuide adopts a **Hybrid Graph Retrieval-Augmented Generation (Graph RAG)** architecture that combines symbolic reasoning from a Knowledge Graph with semantic retrieval from a Vector Index.

Unlike conventional RAG systems that retrieve only semantically similar documents, EduGuide performs retrieval from two complementary knowledge sources:

- **Knowledge Graph** for structured educational facts and relationships.
- **Vector Index** for descriptive and contextual educational knowledge.

The two retrieval paths are orchestrated before passing the final context to the Large Language Model (LLM), enabling accurate, explainable, and context-aware responses.

This architecture directly supports the primary objectives of EduGuide:

- personalized university recommendation
- scholarship discovery
- admission guidance
- curriculum exploration
- career planning
- explainable AI

---

## 4.2 High-Level Architecture

```

```text
                         Student Question
                                │
                                ▼
                      Query Understanding
                                │
                ┌───────────────┴────────────────┐
                │                                │
                ▼                                ▼
       Graph Retrieval                  Vector Retrieval
          (Neo4j)                     (Neo4j Vector Index)
                │                                │
                └───────────────┬────────────────┘
                                ▼
                       Retrieval Fusion Engine
                                │
                                ▼
                         Context Construction
                                │
                                ▼
                     Large Language Model (LLM)
                                │
                                ▼
                  Grounded Educational Response
```

---

## 4.3 Core Components

The Hybrid Graph RAG architecture consists of eight primary components.

| Component | Responsibility |
|------------|----------------|
| Knowledge Repository | Stores all educational knowledge in Markdown format |
| Knowledge Graph | Stores structured educational entities and relationships |
| Vector Index | Stores semantic embeddings of document chunks |
| Query Understanding | Interprets user intent and extracts entities |
| Graph Retrieval | Retrieves structured educational facts |
| Vector Retrieval | Retrieves semantically relevant document chunks |
| Retrieval Fusion | Combines graph facts and semantic evidence |
| LLM | Generates the final grounded response |

Each component is designed independently and communicates through clearly defined interfaces.

---

## 4.4 Component Responsibilities

### Knowledge Repository

The Knowledge Repository is the single source of truth for EduGuide.

It contains all curated educational knowledge collected during the knowledge engineering phase.

Examples include:

- University profiles
- Academic programs
- Curricula
- Scholarships
- Admission requirements
- Career information

Knowledge is stored using standardized Markdown templates to ensure consistency across all educational entities.

The repository is version controlled and serves as the source for both graph construction and vector indexing.

---

### Knowledge Graph

The Knowledge Graph stores structured educational knowledge defined in **05_graph_design.md**.

It contains:

- entities
- properties
- semantic relationships
- graph topology

The graph is responsible for:

- graph traversal
- relationship reasoning
- recommendation
- eligibility checking
- multi-hop exploration

Typical graph queries include:

- Which universities offer Data Science?
- Which scholarships target Computer Science?
- Which careers are associated with Software Engineering?

The graph provides deterministic and explainable results.

---

### Vector Index

The Vector Index stores semantic embeddings generated from Markdown knowledge documents.

Unlike the Knowledge Graph, the Vector Index stores descriptive educational content such as:

- university overview
- scholarship details
- curriculum descriptions
- admission explanations
- career descriptions

The Vector Index enables semantic search when the user's question cannot be answered using graph traversal alone.

Example:

"What is it like to study Data Science at ITC?"

The answer requires descriptive information rather than structured relationships.

---

### Query Understanding

The Query Understanding module converts natural language into a structured query representation.

Its responsibilities include:

- intent detection
- entity recognition
- attribute extraction
- query classification

Example

Student Question

```
I want scholarships for Data Science at ITC.
```

Structured Query

```json
{
  "intent": "scholarship_search",
  "entity": "Scholarship",
  "university": "ITC",
  "program": "Data Science",
  "constraints": []
}
```

This structured representation determines the retrieval strategy.

---

### Retrieval Engine

The Retrieval Engine coordinates both graph retrieval and semantic retrieval.

Depending on the query type, the engine may perform:

- Graph Retrieval only
- Vector Retrieval only
- Hybrid Retrieval

Most educational questions require Hybrid Retrieval.

---

### Retrieval Fusion Engine

The Retrieval Fusion Engine combines information retrieved from both knowledge sources.

Responsibilities include:

- merge graph facts
- merge semantic evidence
- remove duplicate entities
- preserve citations
- prepare context for the LLM

Graph results are treated as high-confidence facts, while vector results provide supporting explanations.

---

### Large Language Model

The Large Language Model is responsible only for language generation.

It does not function as the knowledge source.

The LLM receives:

- graph facts
- retrieved document chunks
- user question
- conversation history

Its responsibilities include:

- synthesizing retrieved evidence
- generating fluent responses
- explaining recommendations
- producing natural conversation

The LLM is explicitly instructed not to invent educational facts.

---

## 4.5 End-to-End Data Flow

The complete data flow of the EduGuide RAG architecture is illustrated below.

```text
                 Markdown Knowledge Repository
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
      Knowledge Graph Builder      Chunking Pipeline
              │                             │
              ▼                             ▼
          Neo4j Graph              Embedding Generator
                                            │
                                            ▼
                                  Neo4j Vector Index

──────────────────────────────────────────────────────

                   Student submits question
                             │
                             ▼
                   Query Understanding
                             │
             ┌───────────────┴────────────────┐
             ▼                                ▼
      Graph Retrieval                  Vector Retrieval
             │                                │
             └───────────────┬────────────────┘
                             ▼
                     Retrieval Fusion
                             ▼
                  Context Construction
                             ▼
                      Large Language Model
                             ▼
                  Explainable AI Response
```

This pipeline ensures that every response is grounded in verified educational knowledge while leveraging the reasoning capabilities of the LLM.

---

# 5. Knowledge Repository Design

## 5.1 Purpose

The Knowledge Repository serves as the foundational knowledge source for the EduGuide platform.

Unlike traditional RAG systems that ingest heterogeneous documents from multiple external sources, EduGuide maintains a curated repository of standardized Markdown files.

This approach provides three major advantages:

- consistent document structure
- high-quality educational knowledge
- traceability between structured and unstructured knowledge

Every downstream component—including the Knowledge Graph and Vector Index—is generated from this repository.

---

## 5.2 Repository Structure

The repository is organized by entity type.

```text
knowledge/

├── universities/
│     ├── itc.md
│     ├── rupp.md
│     └── ...
│
├── programs/
│     ├── data_science.md
│     ├── computer_science.md
│     └── ...
│
├── curriculum/
│
├── scholarships/
│
├── admission/
│
├── careers/
│
└── funders/
```

Each Markdown file represents exactly one educational entity and follows a standardized template defined during the knowledge collection phase.

This organization simplifies maintenance, validation, and automated processing.

---

## 5.3 Entity-Centric Knowledge Design

EduGuide adopts an **entity-centric knowledge model**, where each Markdown file corresponds to a single graph entity.

For example:

- `itc.md` → University
- `data_science.md` → Program
- `itc_government_scholarship.md` → Scholarship
- `software_engineer.md` → Career

This one-to-one mapping ensures consistency between the Knowledge Repository, the Knowledge Graph, and the Vector Index.

The unique entity identifier defined in the Knowledge Graph (`university_id`, `program_id`, `scholarship_id`, etc.) is reused throughout the entire retrieval pipeline to maintain traceability and simplify integration.

# 6. Knowledge Ingestion Pipeline

## 6.1 Purpose

The Knowledge Ingestion Pipeline transforms the EduGuide Knowledge Repository into two complementary knowledge representations:

- a structured Knowledge Graph for symbolic reasoning; and
- a semantic Vector Index for document retrieval.

Rather than maintaining two independent knowledge sources, both representations are generated from the same Markdown repository. This ensures consistency between graph facts and semantic documents while minimizing duplicated knowledge.

The ingestion process is performed offline whenever new educational knowledge is added or existing information is updated.

---

## 6.2 Design Objectives

The Knowledge Ingestion Pipeline is designed to achieve the following objectives.

### Single Source of Truth

All educational knowledge originates from the standardized Markdown repository.

No educational information should be manually inserted into Neo4j or the Vector Index.

---

### Automated Knowledge Processing

The entire ingestion pipeline should execute automatically.

When a new Markdown file is added, the system should:

- parse the document;
- validate its structure;
- construct graph entities;
- generate semantic chunks;
- compute embeddings; and
- update the retrieval indexes.

No manual intervention should be required.

---

### Consistency Between Knowledge Sources

The Knowledge Graph and Vector Index must always represent the same educational knowledge.

Every vector chunk should be traceable to its corresponding graph entity.

Likewise, every graph entity should maintain a reference to its associated semantic documents.

---

### Extensibility

The ingestion pipeline should support future educational entities without requiring architectural changes.

Adding a new entity type should only require:

- a new Markdown template;
- a parser configuration; and
- metadata mapping.

---

# 6.3 Knowledge Ingestion Workflow

The complete ingestion workflow is illustrated below.

```text
                Markdown Knowledge Repository
                           │
                           ▼
                  Markdown Document Parser
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
    Graph Entity Builder         Semantic Section Extractor
            │                             │
            ▼                             ▼
       Neo4j Graph                Chunk Generator
                                          │
                                          ▼
                                 Metadata Generator
                                          │
                                          ▼
                                Embedding Generator
                                          │
                                          ▼
                                 Neo4j Vector Index
```

The Knowledge Graph and Vector Index are therefore synchronized because they originate from the same Markdown source.

---

# 6.4 Markdown Parsing

## Purpose

Convert standardized Markdown documents into structured educational objects.

---

## Input

Markdown entity file

Example

```text
knowledge/programs/data_science.md
```

---

## Output

Structured entity object.

Example

```json
{
  "entity_type": "Program",
  "entity_id": "program_ds_itc",
  "title": "Bachelor of Engineering in Data Science",
  "sections": [...]
}
```

---

## Responsibilities

The Markdown Parser performs the following tasks.

- Read Markdown files.
- Validate required sections.
- Extract metadata.
- Preserve section hierarchy.
- Normalize formatting.
- Detect missing fields.
- Generate internal document identifiers.

---

## Validation Rules

Each Markdown file must satisfy its corresponding template.

For example, a Scholarship document should contain:

- Basic Information
- Overview
- Eligibility
- Benefits
- Application Process
- Required Documents

Missing required sections should generate validation warnings before ingestion continues.

---

# 6.5 Graph Entity Construction

## Purpose

Transform parsed Markdown entities into Neo4j nodes and relationships.

---

## Responsibilities

The Graph Builder performs the following operations.

### Create Nodes

Example

```text
Program

Scholarship

Career

University
```

---

### Populate Properties

Properties defined in **05_graph_design.md** are extracted directly from the Markdown document.

Example

```text
program_id

name

degree_level

duration

language
```

---

### Create Relationships

Relationships are generated using entity references inside Markdown.

Example

```text
University

OFFERS

Program
```

```text
Scholarship

TARGETS

Program
```

```text
Program

LEADS_TO

Career
```

The graph structure is therefore generated automatically rather than manually maintained.

---

# 6.6 Semantic Section Extraction

## Purpose

Identify meaningful semantic sections before chunk generation.

Rather than treating the entire document as one block of text, the ingestion pipeline preserves the logical structure of educational knowledge.

Example

Scholarship

```text
Overview

Eligibility

Benefits

Application Process

Required Documents
```

Each section represents a complete educational concept.

Preserving section boundaries significantly improves retrieval quality.

---

## Why Section-Based Processing?

Traditional RAG systems split documents into arbitrary token windows.

However, EduGuide already stores knowledge using standardized templates.

Breaking a document inside a section would reduce semantic coherence and make retrieval less accurate.

Therefore, semantic sections become the primary unit of chunk generation.

---

# 6.7 Chunk Generation

## Purpose

Transform semantic sections into retrievable knowledge chunks.

Each chunk represents one coherent educational topic.

Example

```text
Chunk 1

Scholarship Overview

----------------------

Chunk 2

Eligibility

----------------------

Chunk 3

Benefits

----------------------

Chunk 4

Application Process
```

---

## Chunking Strategy

EduGuide adopts **semantic section chunking** instead of fixed-size chunking.

Each section becomes one chunk whenever possible.

If a section exceeds the embedding model's maximum context length, recursive splitting is applied while preserving paragraph boundaries.

---

## Chunk Design Principles

Each chunk should:

- describe one educational concept;
- preserve semantic meaning;
- remain understandable independently;
- reference exactly one educational entity.

Chunks should never combine information from multiple entities.

---

# 6.8 Metadata Generation

Each chunk is enriched with metadata before indexing.

Metadata enables filtering, traceability, and graph integration.

---

## Metadata Schema

| Field | Description |
|---------|-------------|
| chunk_id | Unique chunk identifier |
| entity_id | Corresponding graph entity |
| entity_type | University, Program, Scholarship, etc. |
| entity_name | Human-readable name |
| section_name | Markdown section title |
| source_file | Original Markdown file |
| language | Khmer or English |
| version | Knowledge version |
| last_updated | Timestamp |
| embedding_version | Embedding model version |

---

## Example Metadata

```json
{
  "chunk_id":"chunk_001",
  "entity_type":"Scholarship",
  "entity_id":"sch_itc_pm_2026",
  "entity_name":"ITC Prime Minister Scholarship",
  "section_name":"Eligibility",
  "source_file":"scholarships/itc_prime_minister.md",
  "language":"English"
}
```

Metadata plays a critical role in Hybrid Graph RAG because retrieved chunks can be directly linked back to their corresponding graph entities.

---

# 6.9 Embedding Generation

## Purpose

Convert semantic chunks into dense vector representations suitable for similarity search.

---

## Input

Semantic chunk.

---

## Output

Embedding vector.

---

## Design Decision

Only descriptive educational knowledge is embedded.

Examples include:

- overview
- curriculum description
- scholarship benefits
- career description
- admission guidance

Structured properties such as IDs, dates, GPA values, and relationship information are not embedded because they are more efficiently retrieved through the Knowledge Graph.

---

## Embedding Workflow

```text
Chunk

↓

Embedding Model

↓

Dense Vector

↓

Vector Index
```

The embedding model should support multilingual retrieval to accommodate both Khmer and English educational content.

---

# 6.10 Vector Index Construction

## Purpose

Build the semantic retrieval index used by the Hybrid Graph RAG system.

---

## Index Contents

Each vector record consists of:

- embedding vector
- chunk text
- metadata
- entity identifier

The Vector Index therefore stores both semantic meaning and traceable educational context.

---

## Metadata Filtering

During retrieval, metadata can be used to reduce the search space.

Example filters include:

- entity_type = Scholarship
- university = ITC
- language = Khmer
- academic_year = 2026

Filtering improves retrieval precision while reducing unnecessary similarity comparisons.

---

## Synchronization Strategy

Whenever a Markdown document changes:

1. Re-parse the document.
2. Update graph entities.
3. Regenerate affected chunks.
4. Recompute embeddings.
5. Replace outdated vector records.

This incremental synchronization ensures the Knowledge Graph and Vector Index remain consistent without rebuilding the entire knowledge base.


# 7. Retrieval Design

## 7.1 Purpose

The Retrieval subsystem is responsible for identifying and collecting the most relevant educational knowledge required to answer a student's question.

Unlike traditional Retrieval-Augmented Generation systems that rely solely on semantic similarity, EduGuide adopts a **Hybrid Graph Retrieval** approach that combines symbolic reasoning with semantic retrieval.

The retrieval subsystem must:

- understand the user's intent;
- identify educational entities;
- retrieve structured graph facts;
- retrieve descriptive document evidence;
- combine multiple knowledge sources;
- provide explainable context for the LLM.

The output of this subsystem is a grounded context that contains all information required to generate an accurate response.

---

# 7.2 Retrieval Workflow

The retrieval workflow consists of eight stages.

```text
Student Question
        │
        ▼
Query Understanding
        │
        ▼
Intent Detection
        │
        ▼
Entity Recognition
        │
        ▼
Query Decomposition
        │
        ▼
Graph Retrieval
        │
        ▼
Metadata Filtering
        │
        ▼
Vector Retrieval
        │
        ▼
Retrieval Fusion
        │
        ▼
Reranking
        │
        ▼
Context Construction
```

Each stage progressively refines the available knowledge before it is passed to the Large Language Model.

---

# 7.3 Query Understanding

## Purpose

Interpret a student's natural language question and convert it into a structured query representation that downstream retrieval modules can process.

Natural language is often ambiguous.

For example,

> I want to study AI. Which university has good scholarships?

contains multiple intentions:

- academic program
- university
- scholarship
- recommendation

The Query Understanding module extracts these concepts before retrieval begins.

---

## Responsibilities

The module performs the following tasks:

- normalize user input;
- detect query intent;
- recognize educational entities;
- identify constraints;
- classify retrieval strategy.

---

## Input

Natural language question.

Example

```text
I want to study Data Science at ITC.
Are there any scholarships?
```

---

## Output

Structured query object.

Example

```json
{
    "intent": "ScholarshipSearch",
    "entities": {
        "program": "Data Science",
        "university": "ITC"
    },
    "constraints": {},
    "retrieval_strategy": "Hybrid"
}
```

The structured query serves as the input for subsequent retrieval stages.

---

# 7.4 Intent Detection

## Purpose

Determine what the student wants to accomplish.

Intent detection influences which retrieval modules should be executed.

---

## Supported Intents

| Intent | Description |
|----------|-------------|
| University Search | Find universities |
| Program Search | Find academic programs |
| Scholarship Search | Discover scholarships |
| Career Exploration | Explore career pathways |
| Admission Inquiry | Admission requirements |
| Curriculum Inquiry | Curriculum information |
| Comparison | Compare multiple entities |
| Recommendation | Personalized guidance |
| General Question | Educational information |

---

## Example

Question

```text
What scholarships are available for Computer Science?
```

Detected Intent

```text
Scholarship Search
```

---

Question

```text
What careers can I pursue after Civil Engineering?
```

Detected Intent

```text
Career Exploration
```

---

# 7.5 Entity Recognition

## Purpose

Identify educational entities mentioned in the question.

Recognized entities are linked to Knowledge Graph nodes.

---

## Supported Entity Types

- University
- Program
- Scholarship
- Career
- Admission Requirement
- Funder

---

## Example

Question

```text
I want scholarships at ITC.
```

Extracted entities

```text
University

ITC
```

---

Question

```text
Data Science scholarships.
```

Extracted entities

```text
Program

Data Science
```

---

## Entity Resolution

Recognized entities are matched against Neo4j identifiers.

Example

```text
ITC

↓

university_itc
```

```text
Data Science

↓

program_ds_itc
```

This mapping enables deterministic graph traversal.

---

# 7.6 Query Decomposition

## Purpose

Complex educational questions frequently contain multiple retrieval tasks.

Instead of processing the entire question as one search request, EduGuide decomposes the question into smaller subqueries.

---

## Example

Student Question

```text
Which university offers Data Science,
what scholarships are available,
and what careers can I pursue afterwards?
```

Decomposed into

Query A

University offering Data Science

Query B

Scholarships targeting Data Science

Query C

Careers related to Data Science

Each subquery is retrieved independently before being merged.

This approach improves retrieval quality and supports multi-step reasoning.

---

# 7.7 Graph Retrieval

## Purpose

Retrieve structured educational knowledge from Neo4j.

Graph retrieval is responsible for deterministic reasoning rather than semantic similarity.

---

## Suitable Questions

Examples include:

- Which university offers Data Science?
- Which scholarships target AI?
- Which careers follow Computer Science?
- What admission requirements exist?

These questions correspond directly to graph traversal.

---

## Graph Retrieval Process

```text
Structured Query

↓

Generate Cypher

↓

Execute Neo4j

↓

Retrieve Graph Facts
```

---

## Example

Question

```text
Which scholarships target Data Science?
```

Cypher

```cypher
MATCH (s:Scholarship)-[:TARGETS]->(p:Program)
WHERE p.name="Data Science"
RETURN s
```

Output

```text
Scholarship

Scholarship

Scholarship
```

Graph retrieval provides precise educational facts.

---

# 7.8 Metadata Filtering

## Purpose

Reduce unnecessary semantic search by restricting candidate documents before vector retrieval.

Instead of searching the entire knowledge base, EduGuide first filters chunks using metadata.

---

## Example

Detected Intent

Scholarship Search

Entity

ITC

Metadata Filter

```text
entity_type

Scholarship

university

ITC
```

Only scholarship chunks associated with ITC are searched.

---

## Advantages

- faster retrieval;
- reduced noise;
- improved precision;
- lower computational cost.

---

# 7.9 Vector Retrieval

## Purpose

Retrieve descriptive educational information using semantic similarity.

Vector retrieval complements graph retrieval by providing contextual explanations.

---

## Suitable Questions

Examples

- Tell me about Data Science.
- What is student life like?
- What are the benefits of this scholarship?
- Explain the curriculum.

---

## Retrieval Process

```text
Query

↓

Embedding

↓

Similarity Search

↓

Top-K Chunks
```

---

## Retrieval Output

Each retrieved chunk includes

- chunk text;
- similarity score;
- metadata;
- entity identifier.

The metadata enables seamless integration with graph retrieval.

---

# 7.10 Contextual Retrieval

Semantic similarity alone may not preserve sufficient context.

Therefore, each chunk is enriched with contextual information before embedding.

Example

Instead of embedding

```text
Minimum GPA 3.0
```

EduGuide embeds

```text
This section describes the eligibility requirements of the
ITC Government Scholarship for Data Science students.

Minimum GPA 3.0.
```

This additional context improves semantic retrieval accuracy.

---

# 7.11 Hybrid Retrieval Fusion

## Purpose

Merge graph facts and semantic evidence into one retrieval result.

---

## Fusion Strategy

Graph retrieval provides

- entities;
- relationships;
- structured properties.

Vector retrieval provides

- descriptions;
- explanations;
- contextual information.

Both results are merged before generation.

---

## Fusion Workflow

```text
Graph Facts

+

Semantic Chunks

↓

Merge

↓

Remove Duplicates

↓

Rank

↓

Context
```

Duplicate chunks are removed using the shared entity identifier generated during ingestion.

---

# 7.12 Reranking

Initial retrieval is based on similarity.

However, similarity alone may not reflect the student's actual intent.

A reranking stage reorders retrieved documents according to relevance.

---

## Inputs

- graph facts;
- retrieved chunks;
- original question.

---

## Outputs

Ranked retrieval context.

---

## Responsibilities

- prioritize relevant educational entities;
- remove irrelevant chunks;
- improve evidence ordering.

Only the highest-quality context is forwarded to the language model.

---

# 7.13 Retrieval Output

The final retrieval result contains two complementary knowledge sources.

## Structured Facts

Retrieved from Neo4j.

Examples

- university
- scholarship
- deadline
- eligibility
- relationships

---

## Semantic Evidence

Retrieved from the Vector Index.

Examples

- scholarship overview
- curriculum description
- admission explanation
- career information

---

## Unified Retrieval Context

The retrieval subsystem produces a unified context object.

```json
{
    "graph_facts": [...],
    "semantic_chunks": [...],
    "citations": [...],
    "entities": [...]
}
```

This unified context becomes the input to the Response Generation subsystem described in the following section.

# 8. Response Generation

## 8.1 Purpose

The Response Generation subsystem transforms retrieved educational knowledge into natural language responses that are accurate, explainable, and grounded in the EduGuide knowledge base.

Unlike a conventional chatbot where the Large Language Model (LLM) generates answers directly from its internal knowledge, EduGuide constrains the LLM to generate responses only from verified information retrieved by the Retrieval subsystem.

The responsibilities of this subsystem include:

- constructing retrieval context;
- building the prompt;
- generating grounded responses;
- preserving factual accuracy;
- providing supporting evidence;
- minimizing hallucination.

---

# 8.2 Response Generation Workflow

The response generation workflow consists of six stages.

```text
Retrieved Context
        │
        ▼
Context Construction
        │
        ▼
Prompt Construction
        │
        ▼
LLM Generation
        │
        ▼
Grounding Validation
        │
        ▼
Citation Generation
        │
        ▼
Final Response
```

Each stage progressively transforms retrieved knowledge into a student-friendly answer.

---

# 8.3 Context Construction

## Purpose

Construct a structured context for the Large Language Model using the output produced by the Retrieval subsystem.

The context should contain only information relevant to the student's question.

Providing excessive or irrelevant information increases latency, token usage, and the risk of inaccurate responses.

---

## Context Components

The response context consists of four components.

| Component | Purpose |
|------------|----------|
| User Question | Original student query |
| Graph Facts | Structured educational information |
| Semantic Evidence | Retrieved document chunks |
| Conversation Context | Previous messages (if applicable) |

---

## Graph Facts

Structured information retrieved from Neo4j.

Example

```text
University

Institute of Technology of Cambodia

Program

Data Science

Scholarship

ITC Government Scholarship

Deadline

2026-09-30
```

These facts are treated as authoritative.

---

## Semantic Evidence

Descriptive information retrieved from the Vector Index.

Example

```text
Scholarship Overview

This scholarship supports talented Cambodian students pursuing engineering degrees...

Eligibility

Applicants must...
```

These chunks provide detailed explanations that complement graph facts.

---

## Context Assembly

The assembled context follows the structure below.

```text
Question

↓

Graph Facts

↓

Retrieved Chunks

↓

Conversation Context
```

This organization allows the LLM to distinguish between structured facts and descriptive evidence.

---

# 8.4 Prompt Construction

## Purpose

Guide the Large Language Model to generate accurate educational responses using only the retrieved context.

The prompt explicitly defines the model's role, constraints, and expected output format.

---

## System Prompt

The system prompt instructs the model to behave as an educational guidance assistant.

Responsibilities include:

- answer only from retrieved information;
- do not fabricate facts;
- clearly indicate when information is unavailable;
- provide concise and helpful explanations;
- preserve factual values such as GPA, deadlines, and scholarship amounts.

---

## Prompt Structure

The complete prompt contains four sections.

```text
System Instructions

↓

Retrieved Knowledge

↓

Student Question

↓

Response Instructions
```

---

## Response Instructions

The model should:

- answer the student's question directly;
- explain recommendations using retrieved evidence;
- preserve factual accuracy;
- avoid unsupported assumptions;
- use a clear and student-friendly writing style.

---

# 8.5 Response Generation

## Purpose

Generate the final educational response using the constructed prompt.

The LLM should function as a reasoning and language generation engine rather than a knowledge source.

---

## Responsibilities

The model should:

- summarize retrieved knowledge;
- combine graph facts and semantic evidence;
- explain educational recommendations;
- organize information logically;
- maintain conversational quality.

---

## Example

Student Question

```text
Which scholarships are available for Data Science at ITC?
```

Retrieved Facts

```text
ITC Government Scholarship

Prime Minister Scholarship
```

Retrieved Chunks

```text
Eligibility

Benefits

Application Process
```

Generated Response

```text
The Institute of Technology of Cambodia offers two scholarships that support students interested in the Data Science program.

The ITC Government Scholarship is intended for academically strong students and covers tuition fees. Applicants must satisfy the eligibility requirements published by ITC.

The Prime Minister Scholarship also targets qualified engineering students and provides financial support based on academic performance.

Both scholarships require applicants to complete the official application process before the published deadline.
```

The response is entirely derived from retrieved knowledge.

---

# 8.6 Citation Generation

## Purpose

Increase transparency by linking generated statements to their original knowledge sources.

Every factual statement should be traceable to the EduGuide Knowledge Repository.

---

## Citation Sources

Each citation references:

- Markdown file;
- entity identifier;
- section name.

Example

```text
Source

knowledge/scholarships/itc_government.md

Section

Eligibility
```

---

## Citation Workflow

```text
Retrieved Chunk

↓

Metadata

↓

Citation

↓

Response
```

---

## Example

```text
ITC Government Scholarship

Source

Scholarship Entity

Eligibility Section
```

This enables explainable recommendations and simplifies knowledge verification.

---

# 8.7 Grounding Validation

## Purpose

Verify that the generated response is fully supported by retrieved knowledge before it is returned to the student.

Grounding validation reduces hallucination and improves trustworthiness.

---

## Validation Rules

The response should satisfy the following conditions.

- every university exists in the retrieved graph;
- every scholarship exists in the retrieved graph;
- every career exists in the retrieved graph;
- numeric values match retrieved facts;
- deadlines match retrieved facts;
- no unsupported entities appear.

---

## Validation Process

```text
Generated Response

↓

Extract Entities

↓

Compare with Retrieved Facts

↓

Pass

or

Regenerate
```

If unsupported information is detected, the response should be regenerated or rejected.

---

# 8.8 No-Answer Strategy

## Purpose

Handle situations where sufficient knowledge cannot be retrieved.

Rather than generating speculative responses, EduGuide explicitly communicates the absence of supporting evidence.

---

## Examples

Instead of

```text
I think the scholarship may...
```

The system responds

```text
I could not find sufficient information about that scholarship in the current EduGuide knowledge base.

You may consult the university's official website or ask another question related to available scholarships.
```

This policy prioritizes reliability over completeness.

---

# 8.9 Response Formatting

Responses should be optimized for readability.

The presentation format depends on the user's intent.

---

## Information Lookup

Suitable for:

- admission requirements;
- scholarship details;
- university information.

Format

- concise paragraphs;
- bullet lists where appropriate.

---

## Comparison

Suitable for:

- university comparison;
- scholarship comparison;
- program comparison.

Format

Markdown tables.

---

## Recommendation

Suitable for:

- personalized educational guidance;
- university selection;
- career planning.

Format

1. Recommendation
2. Explanation
3. Supporting Evidence
4. Suggested Next Steps

---

## Multi-Step Questions

Complex educational questions should be divided into logical sections.

Example

```text
Scholarships

Admission Requirements

Career Opportunities
```

This structure improves readability and allows students to quickly identify relevant information.

---

# 8.10 Response Quality Objectives

The generated response should satisfy the following quality objectives.

| Objective | Description |
|------------|-------------|
| Accuracy | Information matches retrieved knowledge |
| Groundedness | Every statement is supported by evidence |
| Explainability | Recommendations include supporting reasons |
| Completeness | Answer addresses all parts of the question |
| Readability | Clear and student-friendly language |
| Consistency | Terminology matches the Knowledge Graph |

Meeting these objectives ensures that EduGuide provides reliable educational guidance while maintaining transparency and user trust.

# 9. Evaluation and Performance Optimization

## 9.1 Purpose

The objective of this section is to define how the EduGuide RAG subsystem is evaluated and optimized.

A successful RAG system is not measured solely by its ability to generate fluent responses. It must also retrieve relevant knowledge, preserve factual accuracy, provide explainable recommendations, and maintain acceptable response latency.

The evaluation framework therefore measures the performance of the complete retrieval pipeline rather than the language model alone.

---

# 9.2 Evaluation Objectives

The evaluation process aims to verify that the RAG subsystem satisfies the following objectives.

- retrieve relevant educational knowledge;
- generate accurate responses;
- minimize hallucination;
- provide explainable recommendations;
- maintain acceptable response time;
- support future scalability.

These objectives align with the overall goals of the EduGuide platform.

---

# 9.3 Evaluation Levels

The EduGuide RAG subsystem is evaluated at four levels.

```text
Knowledge Repository

↓

Knowledge Ingestion

↓

Retrieval

↓

Response Generation
```

Each level is validated independently before evaluating the complete system.

---

# 9.4 Knowledge Repository Validation

The Knowledge Repository should satisfy the following quality requirements.

## Completeness

Every educational entity should follow the standardized Markdown template.

Example

```text
University

✓ Basic Information

✓ Overview

✓ Programs

✓ Admission

✓ Scholarships
```

---

## Consistency

All entity identifiers must be unique.

Examples

```text
program_id

scholarship_id

career_id
```

Duplicate identifiers are prohibited.

---

## Structural Validation

Each Markdown document must satisfy its predefined schema.

Missing required sections should be reported during ingestion.

---

# 9.5 Knowledge Ingestion Validation

The ingestion pipeline should correctly transform Markdown knowledge into graph entities and semantic chunks.

Validation includes:

- parser correctness;
- graph construction;
- chunk generation;
- metadata generation;
- embedding generation.

---

## Parser Validation

Verify that every required field is successfully extracted.

Example

Markdown

↓

Program Object

↓

Neo4j Node

---

## Graph Validation

Verify that graph entities and relationships are created correctly.

Example

```text
University

↓

OFFERS

↓

Program
```

The generated graph should match the Knowledge Graph Design defined in Document 05.

---

## Chunk Validation

Every semantic section should produce at least one chunk.

Chunks should satisfy:

- semantic completeness;
- correct metadata;
- valid entity reference.

---

# 9.6 Retrieval Evaluation

Retrieval quality directly influences response quality.

Evaluation focuses on both graph retrieval and semantic retrieval.

---

## Graph Retrieval Accuracy

Graph retrieval is evaluated by executing predefined Cypher queries.

Example queries include:

- programs offered by ITC;
- scholarships targeting Data Science;
- careers related to Computer Science;
- admission requirements.

The returned graph entities should exactly match the Knowledge Graph.

---

## Vector Retrieval Accuracy

Vector retrieval is evaluated using manually prepared test questions.

Example

Question

```text
Tell me about the ITC Government Scholarship.
```

Expected Retrieval

```text
Overview

Eligibility

Benefits

Application Process
```

The retrieved chunks should be relevant to the question.

---

## Hybrid Retrieval Evaluation

Hybrid retrieval should successfully combine graph facts and semantic evidence.

Evaluation criteria include:

- relevant graph entities retrieved;
- relevant document chunks retrieved;
- duplicate removal;
- correct entity mapping.

---

# 9.7 Response Evaluation

Generated responses are evaluated using multiple quality dimensions.

| Metric | Description |
|----------|-------------|
| Accuracy | Information matches retrieved knowledge |
| Completeness | All parts of the question are answered |
| Explainability | Recommendations include supporting evidence |
| Groundedness | Every statement is supported by retrieved knowledge |
| Readability | Easy for students to understand |
| Consistency | Terminology matches the Knowledge Graph |

Responses failing these criteria should be reviewed and improved.

---

# 9.8 Hallucination Evaluation

Hallucination occurs when the language model generates unsupported educational information.

The system should verify that:

- every university exists in Neo4j;
- every scholarship exists in Neo4j;
- every career exists in Neo4j;
- all numeric values match retrieved facts;
- no unsupported entities appear.

Unsupported responses should be regenerated or rejected.

---

# 9.9 Performance Evaluation

The RAG subsystem should provide interactive response times suitable for conversational applications.

Performance is evaluated for each pipeline component.

| Component | Evaluation |
|------------|------------|
| Graph Retrieval | Query execution time |
| Vector Retrieval | Similarity search latency |
| Retrieval Fusion | Processing time |
| LLM Generation | Response generation time |
| End-to-End | Total response time |

The objective is to minimize latency while maintaining retrieval quality.

---

# 9.10 Optimization Strategy

Performance optimization is applied throughout the retrieval pipeline.

---

## Query Optimization

Generated Cypher queries should use indexed properties whenever possible.

Examples include:

- university name;
- program name;
- scholarship name.

This reduces graph traversal time.

---

## Metadata Filtering

Metadata filtering is applied before semantic retrieval.

Instead of searching the entire vector index, the search space is restricted using metadata.

Example

```text
entity_type

Scholarship

University

ITC
```

Filtering improves retrieval precision and reduces computational cost.

---

## Embedding Optimization

Embeddings are generated only when knowledge changes.

Existing embeddings are reused whenever possible.

This avoids unnecessary recomputation.

---

## Chunk Optimization

Semantic section chunking is preferred over fixed-size chunking.

Advantages include:

- higher semantic coherence;
- better retrieval precision;
- easier citation generation.

---

## Index Optimization

Both graph indexes and vector indexes should be updated incrementally.

Only modified documents should trigger reindexing.

This significantly reduces ingestion time.

---

# 9.11 Scalability Considerations

The RAG subsystem is designed to support future growth in both knowledge volume and user demand.

---

## Knowledge Scalability

New educational entities can be added by creating new Markdown files.

The ingestion pipeline automatically updates:

- Knowledge Graph;
- Vector Index;
- Retrieval Metadata.

No architectural changes are required.

---

## User Scalability

The retrieval pipeline should support concurrent users.

Future deployment may introduce:

- distributed vector indexes;
- Neo4j clustering;
- embedding cache;
- response cache.

These enhancements improve system throughput.

---

## Functional Scalability

Future versions of EduGuide may support:

- multilingual retrieval;
- voice-based interaction;
- document upload;
- personalized learning paths;
- internship recommendation;
- agent collaboration.

The modular architecture allows these capabilities to be integrated without redesigning the existing pipeline.

---

# 10. Future Improvements

Although the current Hybrid Graph RAG architecture satisfies the requirements of EduGuide Version 1, several enhancements are planned for future releases.

---

## 10.1 Personalized Retrieval

Future versions will incorporate student profiles into the retrieval process.

Examples include:

- academic interests;
- GPA;
- preferred location;
- financial constraints;
- language preference.

These attributes can improve retrieval relevance and recommendation quality.

---

## 10.2 Agentic Retrieval

Instead of executing a single retrieval workflow, future versions may employ multiple specialized AI agents.

Example

```text
Student Question

↓

Planning Agent

↓

Scholarship Agent

Program Agent

Career Agent

↓

Evidence Aggregation

↓

Final Response
```

Each agent focuses on a specific educational domain before combining results.

---

## 10.3 Conversational Memory

Future versions may maintain long-term conversation context.

Examples include:

- previously recommended universities;
- selected programs;
- saved scholarships;
- user preferences.

This enables more personalized multi-turn conversations.

---

## 10.4 Multimodal Knowledge

The current system focuses on textual educational knowledge.

Future versions may incorporate:

- curriculum flowcharts;
- university campus maps;
- admission infographics;
- scholarship brochures;
- promotional videos.

These resources can enrich retrieval and improve the student experience.

---

## 10.5 Continuous Knowledge Synchronization

Future versions may automatically monitor official university websites.

When changes are detected:

- updated content is collected;
- Markdown knowledge is regenerated;
- graph entities are updated;
- embeddings are regenerated.

This reduces manual maintenance while ensuring information remains current.

---

# 11. Summary

This document presented the Retrieval-Augmented Generation (RAG) Design of the EduGuide platform.

The RAG subsystem extends the Knowledge Graph defined in Document 05 by combining symbolic reasoning with semantic document retrieval to provide accurate, explainable, and personalized educational guidance.

The design introduced:

- a Markdown-based Knowledge Repository as the single source of truth;
- an automated Knowledge Ingestion Pipeline for constructing the Knowledge Graph and Vector Index;
- a Hybrid Graph Retrieval architecture that integrates graph traversal and semantic search;
- a response generation workflow that grounds LLM outputs in retrieved evidence;
- an evaluation framework for measuring retrieval quality, factual accuracy, and system performance; and
- a roadmap for future enhancements, including personalized retrieval, agentic workflows, conversational memory, and multimodal knowledge integration.

By separating structured knowledge, semantic knowledge, and language generation into dedicated components, the EduGuide RAG architecture provides a scalable and maintainable foundation for intelligent educational guidance.

This design ensures that future development can focus on expanding knowledge coverage and improving retrieval strategies without fundamentally changing the system architecture.

