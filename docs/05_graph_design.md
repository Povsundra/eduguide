# 05. Knowledge Graph Design

**Document Version:** 1.0  
**Project:** EduGuide – An Agentic Retrieval-Augmented Decision Support System for Personalized Higher Education Guidance in Cambodia

---

# 1. Purpose

The Knowledge Graph Design defines how the conceptual ontology presented in Chapter 4 is transformed into an operational graph structure capable of supporting intelligent educational guidance within the EduGuide platform.

While the Domain Model identifies the educational concepts and the Ontology formally specifies their semantic meanings, the Knowledge Graph Design focuses on representing those concepts as interconnected graph elements that enable efficient storage, traversal, reasoning, and retrieval.

The resulting Knowledge Graph serves as the structured knowledge layer of EduGuide and provides the foundation for:

- Knowledge organization
- Multi-hop reasoning
- Personalized recommendation
- Explainable AI responses
- Retrieval-Augmented Generation (RAG)
- Future knowledge expansion

Unlike the Ontology, which remains implementation-independent, this document introduces the implementation-oriented graph representation while preserving the semantic integrity established by the ontology.

---

# 2. Design Objectives

The EduGuide Knowledge Graph is designed to satisfy six primary objectives.

---

## 2.1 Preserve Ontology Semantics

Every ontology class, relationship, and constraint should be represented within the graph without changing its semantic meaning.

The graph implementation must remain faithful to the conceptual knowledge defined in Chapter 4.

---

## 2.2 Support Efficient Graph Traversal

Educational knowledge is highly interconnected.

Students frequently ask questions that require traversing multiple related concepts, such as:

- Which scholarships are available for Computer Science?
- Which universities offer Data Science?
- Which careers are associated with Information Technology?
- What admission requirements apply to this scholarship?

The graph should enable these questions to be answered through short and meaningful traversal paths.

---

## 2.3 Enable Explainable Recommendations

Unlike traditional recommendation systems that often produce opaque results, EduGuide aims to generate recommendations that can be explained through explicit graph relationships.

For example:

```text
Student Interest
        │
        ▼
Program
        │
        ▼
Scholarship
        │
        ▼
University
```

Each recommendation should be traceable through identifiable graph paths, allowing the AI system to justify its suggestions.

---

## 2.4 Support Knowledge Reuse

The graph should avoid duplicating educational knowledge.

Instead, reusable concepts such as Admission Requirements, Careers, and Funders should exist only once and be referenced by multiple entities whenever appropriate.

This principle reduces redundancy, improves maintainability, and ensures consistency across the knowledge base.

---

## 2.5 Integrate with Retrieval-Augmented Generation

The Knowledge Graph is responsible for storing structured educational facts, while detailed textual information is maintained separately within the RAG document store.

Together, these components provide complementary capabilities:

- Graph → structured reasoning
- Vector database → semantic document retrieval
- LLM → natural language generation

This separation allows EduGuide to combine symbolic reasoning with semantic search while avoiding unnecessary duplication of information.

---

## 2.6 Support Future Expansion

The graph should remain extensible as EduGuide evolves.

Future educational concepts—including Subjects, Skills, Faculty, Industry, Occupation, and Internship Opportunities—should be incorporated through graph extensions rather than requiring structural redesign.

---

# 3. Knowledge Graph Design Principles

The following principles guided every modeling decision during the design of the Knowledge Graph.

---

## 3.1 Semantic Representation

Graph elements represent educational meaning rather than database implementation details.

Every node corresponds to an educational entity, and every relationship represents a meaningful semantic connection between two concepts.

The graph should describe how educational knowledge is connected, not how information is physically stored.

---

## 3.2 Traversal-Oriented Design

The graph is designed to optimize graph traversal rather than relational joins.

Relationships are created to support the natural exploration of educational knowledge.

For example:

```text
University
      │
   OFFERS
      │
Program
      │
LEADS_TO
      │
Career
```

This structure enables efficient multi-hop navigation while preserving semantic clarity.

---

## 3.3 Reusable Knowledge

Educational concepts that may be shared across multiple entities should be represented only once.

Examples include:

- Admission Requirement
- Career
- Funder

These entities are referenced through graph relationships rather than duplicated as node properties.

This design improves consistency and simplifies future updates.

---

## 3.4 Explainable Relationships

Every relationship in the graph should correspond to a real-world educational relationship.

For example:

- Universities offer Programs.
- Scholarships target Programs.
- Programs lead to Careers.

Relationships are intentionally modeled to support explanation generation by AI agents.

---

## 3.5 Minimal Redundancy

Duplicated knowledge increases maintenance complexity and may introduce inconsistencies.

Whenever possible, the graph represents each real-world concept only once.

Shared concepts are connected through relationships instead of repeated across multiple nodes.

---

## 3.6 Separation of Structured and Unstructured Knowledge

The graph is designed to store structured knowledge only.

Examples include:

- entities
- relationships
- identifiers
- numeric values
- categorical information

Long-form textual descriptions remain outside the graph and are managed by the Retrieval-Augmented Generation (RAG) subsystem.

This separation ensures that each component is optimized for its intended purpose.

---

## 3.7 Extensibility

The graph structure should accommodate future educational concepts without requiring major redesign.

New node labels and relationship types should integrate naturally into the existing graph while preserving backward compatibility.

---

# 4. Graph Modeling Decisions

The Knowledge Graph Design translates ontology concepts into graph structures through a series of modeling decisions.

Rather than directly mapping every ontology element into Neo4j, each concept was evaluated according to graph modeling principles to determine whether it should be represented as a node, relationship, or property.

---

## 4.1 Node Modeling Decisions

A concept is represented as a graph node if it satisfies one or more of the following criteria:

- possesses an independent identity;
- contains its own attributes;
- participates in multiple semantic relationships;
- may be referenced by multiple entities;
- may evolve independently over time.

Applying these criteria resulted in the identification of seven core node labels.

| Ontology Class | Graph Node | Justification |
|----------------|------------|---------------|
| University | `:University` | Independent educational institution |
| Program | `:Program` | Primary recommendation target |
| Curriculum | `:Curriculum` | Independent academic structure with versioning |
| Scholarship | `:Scholarship` | Independent financial opportunity |
| Admission Requirement | `:AdmissionRequirement` | Reusable eligibility concept |
| Career | `:Career` | Shared professional pathway |
| Funder | `:Funder` | Independent funding organization |

No ontology class was reduced to a simple property because each possesses meaningful semantics and participates in multiple relationships.

---

## 4.2 Relationship Modeling Decisions

Relationships represent semantic associations between educational entities rather than implementation shortcuts.

Relationship direction follows real-world educational meaning instead of query frequency.

Because Neo4j supports bidirectional traversal, only one direction is stored for each semantic relationship.

The graph therefore defines the following relationship types:

| Relationship | Meaning |
|--------------|----------|
| OFFERS | University provides Program |
| HAS_CURRICULUM | Program contains Curriculum |
| HAS_ADMISSION_REQUIREMENT | Program requires Admission Requirement |
| TARGETS | Scholarship supports Program |
| AVAILABLE_AT | Scholarship is available at University |
| FUNDED_BY | Scholarship receives funding from Funder |
| HAS_REQUIREMENT | Scholarship requires Admission Requirement |
| LEADS_TO | Program prepares students for Career |

Each relationship directly reflects the educational semantics established by the ontology.

---

## 4.3 Property Modeling Decisions

Properties describe intrinsic characteristics of nodes rather than relationships.

Several modeling rules were adopted:

- Every node possesses one immutable unique identifier.
- Human-readable names are stored separately from identifiers.
- Enumerations are represented as strings.
- Dates use native date data types.
- Numeric values use native numeric types.
- Long descriptive text is minimized within the graph.

This approach ensures consistency while avoiding unnecessary complexity.

---

## 4.4 Design Decision Log

Several alternative graph representations were evaluated before selecting the final design.

| Design Problem | Alternatives Considered | Selected Design | Justification |
|----------------|------------------------|-----------------|---------------|
| Curriculum | Property or Node | Node | Independent academic structure and versioning |
| Admission Requirement | Property or Node | Node | Reusable across Programs and Scholarships |
| Scholarship | Child of University or Independent | Independent Node | Supports external funding organizations |
| Career | Text Property or Node | Node | Shared career pathways across Programs |
| Funder | Enumeration or Node | Node | Represents reusable organizations |
| Relationship Direction | Query-oriented or Semantic | Semantic | Improves readability and preserves educational meaning |

The selected design prioritizes semantic correctness, knowledge reuse, graph traversal efficiency, and long-term extensibility over implementation convenience.

---

# Summary

This chapter establishes the engineering principles that transform the conceptual ontology into an operational Knowledge Graph.

The next sections define the concrete graph schema, including node labels, relationship types, properties, graph constraints, and indexing strategies that implement these design decisions within the EduGuide platform.

# 5. Knowledge Graph Schema

The Knowledge Graph Schema defines the structural representation of the ontology within the graph database.

The schema specifies the graph elements used to represent educational knowledge, including node labels, relationship types, node properties, relationship properties, and graph cardinality.

Unlike the Ontology, which describes conceptual semantics, the graph schema defines how those concepts are represented within the operational Knowledge Graph.

---

# 5.1 Node Labels

Each ontology class is implemented as a Neo4j node label.

A node label represents an independent educational entity that possesses its own identity, properties, and relationships.

The EduGuide Knowledge Graph contains seven node labels.

| Node Label | Represents | Description |
|------------|------------|-------------|
| `University` | Higher Education Institution | Educational provider offering academic programs |
| `Program` | Academic Program | Degree or study program offered by a university |
| `Curriculum` | Academic Structure | Curriculum associated with a program |
| `Scholarship` | Financial Opportunity | Scholarship available to eligible students |
| `AdmissionRequirement` | Eligibility Requirement | Admission or scholarship requirement |
| `Career` | Professional Pathway | Career commonly associated with a program |
| `Funder` | Funding Organization | Organization providing scholarship funding |

---

## Node Design

Each node satisfies the following characteristics:

- possesses a globally unique identifier;
- stores intrinsic properties only;
- participates in one or more semantic relationships;
- can be traversed independently within the graph.

Example:

```text
(:University)

(:Program)

(:Scholarship)

(:Career)
```

No node exists solely as a container for another node.

---

# 5.2 Relationship Types

Relationships represent semantic connections between educational entities.

Unlike relational databases where relationships are implied through foreign keys, relationships are first-class citizens within the Knowledge Graph.

The EduGuide graph defines eight relationship types.

| Relationship | Source | Target | Meaning |
|--------------|--------|--------|---------|
| OFFERS | University | Program | University provides a Program |
| HAS_CURRICULUM | Program | Curriculum | Program contains Curriculum |
| HAS_ADMISSION_REQUIREMENT | Program | AdmissionRequirement | Program requires Admission Requirement |
| TARGETS | Scholarship | Program | Scholarship supports Program |
| AVAILABLE_AT | Scholarship | University | Scholarship available at University |
| FUNDED_BY | Scholarship | Funder | Scholarship funded by Organization |
| HAS_REQUIREMENT | Scholarship | AdmissionRequirement | Scholarship eligibility requirement |
| LEADS_TO | Program | Career | Program prepares graduates for Career |

---

## Relationship Design Rules

Relationship direction follows educational semantics rather than query frequency.

For example,

```text
University

↓

OFFERS

↓

Program
```

is preferred over

```text
Program

↓

BELONGS_TO

↓

University
```

because the University performs the educational action of offering a Program.

Neo4j supports traversal in both directions, making duplicate reverse relationships unnecessary.

---

# 5.3 Node Properties

Node properties describe intrinsic characteristics of educational entities.

Properties do not represent relationships.

---

## University

| Property | Type | Description |
|----------|------|-------------|
| university_id | String | Unique identifier |
| name | String | Official university name |
| abbreviation | String | University abbreviation |
| type | String | Public or Private |
| location | String | Province or City |
| website | String | Official website |
| established_year | Integer | Year established |
| description | String | Short institutional overview |
| doc_ref | String | Reference to RAG documents |

---

## Program

| Property | Type |
|----------|------|
| program_id | String |
| name | String |
| degree_level | String |
| duration | Integer |
| language | String |
| overview | String |
| doc_ref | String |

---

## Curriculum

| Property | Type |
|----------|------|
| curriculum_id | String |
| academic_year | String |
| total_credits | Integer |
| duration | Integer |
| description | String |
| doc_ref | String |

---

## Scholarship

| Property | Type |
|----------|------|
| scholarship_id | String |
| name | String |
| scholarship_type | String |
| coverage | String |
| application_deadline | Date |
| description | String |
| doc_ref | String |

---

## AdmissionRequirement

| Property | Type |
|----------|------|
| requirement_id | String |
| name | String |
| category | String |
| mandatory | Boolean |
| description | String |

---

## Career

| Property | Type |
|----------|------|
| career_id | String |
| title | String |
| industry | String |
| description | String |
| doc_ref | String |

---

## Funder

| Property | Type |
|----------|------|
| funder_id | String |
| name | String |
| organization_type | String |
| website | String |
| description | String |

---

## Property Modeling Rules

The following rules apply to all node properties.

- Every node contains one immutable unique identifier.
- Human-readable names are stored separately from identifiers.
- Enumerations are represented using strings.
- Dates use Neo4j native DATE values.
- Numeric values use native numeric types.
- Large documents are not stored as node properties.
- Every knowledge entity linked to the RAG subsystem contains a `doc_ref` property.

---

# 5.4 Relationship Properties

Most educational relationships within EduGuide represent semantic connections and therefore do not require additional properties.

For Version 1, relationship properties are intentionally minimized.

| Relationship | Properties |
|--------------|------------|
| OFFERS | None |
| HAS_CURRICULUM | None |
| HAS_ADMISSION_REQUIREMENT | None |
| TARGETS | None |
| AVAILABLE_AT | None |
| FUNDED_BY | None |
| HAS_REQUIREMENT | None |
| LEADS_TO | None |

Keeping relationships lightweight improves traversal performance and simplifies graph maintenance.

Future versions may introduce relationship properties such as:

- scholarship priority
- admission year
- curriculum effective date
- confidence score
- recommendation weight

---

# 5.5 Graph Cardinality

Cardinality defines how many instances of one node may be connected to another.

| Relationship | Cardinality |
|--------------|------------|
| University → Program | One-to-Many |
| Program → Curriculum | One-to-Many |
| Program → AdmissionRequirement | Many-to-Many |
| Scholarship → Program | Many-to-Many |
| Scholarship → University | Many-to-Many |
| Scholarship → AdmissionRequirement | Many-to-Many |
| Scholarship → Funder | Many-to-One |
| Program → Career | Many-to-Many |

These cardinalities directly implement the semantic constraints defined by the Ontology.

---

## 5.6 Graph Schema Overview

The complete graph schema is summarized below.

```text
(:University)
      │
      ├──[:OFFERS]────────────────────────────►(:Program)
      │                                            │
      │                                            ├──[:HAS_CURRICULUM]────────────►(:Curriculum)
      │                                            │
      │                                            ├──[:HAS_ADMISSION_REQUIREMENT]►(:AdmissionRequirement)
      │                                            │
      │                                            └──[:LEADS_TO]──────────────────►(:Career)
      │
(:Scholarship)
      │
      ├──[:AVAILABLE_AT]──────────────────────────►(:University)
      │
      ├──[:TARGETS]───────────────────────────────►(:Program)
      │
      ├──[:FUNDED_BY]─────────────────────────────►(:Funder)
      │
      └──[:HAS_REQUIREMENT]───────────────────────►(:AdmissionRequirement)
```

The schema preserves the semantics defined by the Ontology while providing a traversal-oriented representation suitable for recommendation, reasoning, and Retrieval-Augmented Generation.

---

# 6. Graph Constraints

Graph constraints maintain data integrity and ensure semantic consistency across the Knowledge Graph.

---

## 6.1 Identity Constraints

Each node possesses one globally unique identifier.

| Node | Unique Property |
|------|-----------------|
| University | university_id |
| Program | program_id |
| Curriculum | curriculum_id |
| Scholarship | scholarship_id |
| AdmissionRequirement | requirement_id |
| Career | career_id |
| Funder | funder_id |

These identifiers prevent duplicate representations of the same real-world entity.

---

## 6.2 Semantic Constraints

The following constraints preserve the educational semantics established by the ontology.

- Every Program belongs to exactly one University.
- Every Curriculum belongs to exactly one Program.
- Every Scholarship is funded by exactly one Funder.
- Every Scholarship targets at least one Program or is available at one University.
- Every Career is associated with at least one Program.
- Admission Requirements may be shared by multiple Programs and Scholarships.
- Universities may exist without Scholarships.
- Programs cannot exist independently of Universities.
- Curricula cannot exist independently of Programs.

---

## 6.3 Data Integrity Constraints

To prevent inconsistent graph structures:

- Duplicate AdmissionRequirement nodes are prohibited.
- Duplicate Career nodes are prohibited.
- Duplicate Funder nodes are prohibited.
- Relationship direction follows semantic conventions.
- Circular relationships between identical entity types are not permitted unless explicitly modeled.

---

# 7. Index Strategy

Indexes improve query performance by reducing the number of nodes scanned during graph traversal.

---

## 7.1 Lookup Indexes

| Node | Indexed Property |
|------|------------------|
| University | name |
| Program | name |
| Scholarship | name |
| Career | title |

These indexes accelerate common user searches.

---

## 7.2 Filtering Indexes

| Property | Purpose |
|----------|---------|
| application_deadline | Scholarship deadline filtering |
| category | Admission Requirement filtering |
| organization_type | Funder filtering |
| type | University type filtering |

---

## 7.3 Performance Considerations

The graph is optimized for:

- short traversal paths;
- semantic relationship exploration;
- recommendation generation;
- explainable reasoning;
- integration with the Retrieval-Augmented Generation subsystem.

Rather than optimizing for complex relational joins, the graph prioritizes efficient navigation between interconnected educational entities.

# 8. Graph Traversal Design

The primary advantage of a Knowledge Graph over traditional relational databases is its ability to efficiently traverse interconnected knowledge.

Rather than performing multiple table joins, Neo4j follows explicit semantic relationships between educational entities.

Within EduGuide, graph traversal enables the system to answer educational questions, discover related knowledge, and generate explainable recommendations.

---

# 8.1 Traversal Principles

The graph traversal strategy follows four principles.

## 1. Short Traversal Paths

Most educational queries should be answered within one to three relationship hops.

Short traversal paths improve query performance while making recommendation explanations easier to understand.

---

## 2. Semantic Navigation

Traversal follows educational meaning rather than database structure.

For example,

```text
University
      │
OFFERS
      │
Program
      │
LEADS_TO
      │
Career
```

represents the educational progression from institution to employment pathway.

---

## 3. Explainable Reasoning

Every recommendation should be supported by one or more explicit graph paths.

Rather than producing opaque recommendations, the system can explain why a recommendation was generated by referencing the traversed relationships.

---

## 4. Relationship Reuse

Traversal should reuse existing relationships instead of creating shortcut edges.

For example,

the graph does not require a direct

```text
University

↓

Career
```

relationship because

```text
University

↓

Program

↓

Career
```

already represents the educational pathway.

---

# 8.2 Common Traversal Patterns

The following traversal patterns support the primary educational services provided by EduGuide.

---

## Pattern A — Program Discovery

User Question

> Which programs are offered by ITC?

Traversal

```text
University

↓

OFFERS

↓

Program
```

Traversal Depth

1 Hop

Purpose

Program search.

---

## Pattern B — University Discovery

User Question

> Which universities offer Data Science?

Traversal

```text
Program

↑

OFFERS

↑

University
```

Traversal Depth

1 Hop

Purpose

University comparison.

---

## Pattern C — Scholarship Discovery

User Question

> Which scholarships are available for Data Science?

Traversal

```text
Scholarship

↓

TARGETS

↓

Program
```

Traversal Depth

1 Hop

Purpose

Scholarship recommendation.

---

## Pattern D — Scholarship Availability

User Question

> Which scholarships are available at CADT?

Traversal

```text
Scholarship

↓

AVAILABLE_AT

↓

University
```

Traversal Depth

1 Hop

Purpose

Institution-specific scholarship search.

---

## Pattern E — Career Exploration

User Question

> What careers can I pursue after Software Engineering?

Traversal

```text
Program

↓

LEADS_TO

↓

Career
```

Traversal Depth

1 Hop

Purpose

Career guidance.

---

## Pattern F — Admission Checking

User Question

> What are the admission requirements for Computer Science?

Traversal

```text
Program

↓

HAS_ADMISSION_REQUIREMENT

↓

AdmissionRequirement
```

Traversal Depth

1 Hop

Purpose

Eligibility guidance.

---

## Pattern G — Scholarship Eligibility

User Question

> Does this scholarship require IELTS?

Traversal

```text
Scholarship

↓

HAS_REQUIREMENT

↓

AdmissionRequirement
```

Traversal Depth

1 Hop

Purpose

Scholarship eligibility verification.

---

## Pattern H — Multi-Hop Educational Recommendation

User Question

> I want to become a Data Scientist. Which university and scholarship should I consider?

Traversal

```text
Career

↑

LEADS_TO

↑

Program

↑

TARGETS

↑

Scholarship

↓

AVAILABLE_AT

↓

University
```

Traversal Depth

3 Hops

Purpose

Explainable educational recommendation.

---

# 8.3 Traversal Complexity

Traversal complexity was evaluated during graph design.

| Query Type | Typical Hops |
|------------|-------------|
| University Lookup | 1 |
| Program Lookup | 1 |
| Scholarship Search | 1 |
| Career Search | 1 |
| Admission Search | 1 |
| Recommendation | 2–3 |
| Compound Educational Queries | 3 |

No common educational query requires more than three graph hops.

This demonstrates that the graph structure remains efficient while avoiding unnecessary shortcut relationships.

---

# 9. Graph–RAG Integration

The EduGuide architecture combines symbolic knowledge representation with semantic document retrieval.

Rather than storing all information in a single database, structured and unstructured knowledge are separated according to their characteristics.

---

## 9.1 Knowledge Boundary

The Knowledge Graph stores structured educational knowledge.

The RAG subsystem stores unstructured educational knowledge.

The Large Language Model combines both sources to generate personalized responses.

```text
                    User Question
                          │
                          ▼
                Retrieval Orchestrator
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
         Knowledge Graph      Vector Database
        (Structured Facts)   (Document Chunks)
                 │                   │
                 └─────────┬─────────┘
                           ▼
                    Large Language Model
                           ▼
                 Explainable Recommendation
```

---

## 9.2 Responsibilities

### Knowledge Graph

Stores

- entities
- identifiers
- relationships
- structured attributes
- graph topology

Supports

- graph traversal
- recommendation
- reasoning
- filtering

---

### Vector Database

Stores

- curriculum documents
- scholarship announcements
- university descriptions
- admission guides
- career articles
- text embeddings

Supports

- semantic retrieval
- contextual evidence
- document grounding

---

### Large Language Model

Combines

- graph facts
- retrieved documents
- user profile
- conversation history

Produces

- personalized recommendations
- natural language explanations
- grounded responses

---

## 9.3 Shared Entity Identity

To maintain consistency between the Knowledge Graph and the Vector Database, each educational entity is assigned a shared identifier.

Example

```text
Program

program_id

↓

doc_ref

↓

Vector Document
```

Example

```text
Program

program_ds_itc

↓

doc_ref

↓

program_ds_itc.pdf
```

This shared identifier enables retrieved documents to be linked back to their corresponding graph entities.

---

## 9.4 Retrieval Workflow

The retrieval workflow consists of six stages.

### Step 1

Student submits a natural-language question.

↓

### Step 2

Semantic retrieval identifies the most relevant document chunks.

↓

### Step 3

Retrieved chunks contain associated entity identifiers.

↓

### Step 4

Entity identifiers are used to retrieve structured graph facts from Neo4j.

↓

### Step 5

Retrieved documents and graph facts are merged into a unified context.

↓

### Step 6

The Large Language Model generates an explainable recommendation.

This hybrid workflow combines semantic understanding with symbolic reasoning.

---

# 10. Design Validation

The Knowledge Graph Design was evaluated against the functional requirements established in the Domain Model and Ontology.

---

## 10.1 Functional Validation

The graph successfully supports:

✓ University discovery

✓ Program exploration

✓ Scholarship recommendation

✓ Career guidance

✓ Admission checking

✓ Multi-hop reasoning

✓ Explainable recommendations

✓ Integration with RAG

---

## 10.2 Structural Validation

The graph satisfies the following design objectives.

| Objective | Status |
|-----------|--------|
| Preserve ontology semantics | ✓ |
| Avoid duplicated knowledge | ✓ |
| Support graph traversal | ✓ |
| Enable recommendation | ✓ |
| Support explainability | ✓ |
| Integrate with RAG | ✓ |
| Future extensibility | ✓ |

---

## 10.3 Traversal Validation

Representative educational queries were evaluated.

| User Question | Traversal Depth |
|--------------|----------------|
| Programs offered by ITC | 1 Hop |
| Scholarships for Data Science | 1 Hop |
| Careers after Computer Science | 1 Hop |
| Admission requirements | 1 Hop |
| Scholarship eligibility | 1 Hop |
| Career → Scholarship → University recommendation | 3 Hops |

The evaluation demonstrates that the graph efficiently supports educational reasoning while maintaining low traversal complexity.

---

# Summary

This chapter transformed the ontology into an operational Knowledge Graph optimized for educational reasoning, recommendation, and retrieval.

Through traversal-oriented graph design, reusable knowledge representation, and explicit semantic relationships, the Knowledge Graph enables EduGuide to efficiently answer educational questions while supporting explainable recommendations.

The integration of the Knowledge Graph with the Retrieval-Augmented Generation subsystem establishes a hybrid architecture in which symbolic reasoning complements semantic document retrieval, providing accurate, explainable, and context-aware guidance for Cambodian students.

# 11. Future Evolution

The EduGuide Knowledge Graph is designed as an extensible knowledge representation rather than a fixed database schema.

Although Version 1 focuses on the seven core educational entities required to support personalized university guidance, the graph architecture has been intentionally designed to accommodate future educational knowledge without requiring structural redesign.

Future extensions will be introduced by adding new node labels and relationship types while preserving the existing graph structure.

---

## 11.1 Planned Graph Extensions

Future versions of EduGuide will introduce additional educational concepts to enrich recommendation quality and reasoning capabilities.

### Version 2

The following academic entities are planned.

| Node Label | Purpose |
|------------|---------|
| Faculty | Organizational structure within universities |
| Subject | Individual courses within a curriculum |
| Skill | Competencies acquired through study |
| Degree | Academic qualification awarded upon graduation |
| Industry | Employment sectors |
| Occupation | Standardized professional occupations |

These entities will support curriculum-level recommendations, skill gap analysis, and career matching.

---

### Version 3

Future student-service entities include:

| Node Label | Purpose |
|------------|---------|
| Internship | Practical training opportunities |
| Exchange Program | International study opportunities |
| Student Organization | Extracurricular activities |
| Professional Certification | Industry-recognized certifications |
| Learning Outcome | Educational competency framework |

These additions will further enhance personalized educational planning.

---

## 11.2 Future Graph Structure

The current graph can naturally evolve without redesign.

Example:

```text
(:University)
        │
        └──[:OFFERS]
                  │
            (:Program)
                  │
        ┌─────────┴─────────┐
        │                   │
[:HAS_CURRICULUM]      [:LEADS_TO]
        │                   │
(:Curriculum)        (:Career)
        │
[:HAS_SUBJECT]
        │
(:Subject)
        │
[:TEACHES]
        │
(:Skill)
        │
[:REQUIRED_BY]
        │
(:Occupation)
```

This extension illustrates how new educational knowledge can be integrated while preserving the existing graph topology.

---

## 11.3 Scalability Considerations

The Knowledge Graph has been designed to scale in three dimensions.

### Knowledge Scalability

Additional educational concepts can be introduced without modifying existing entities.

---

### Data Scalability

The graph supports continuous ingestion of:

- Universities
- Programs
- Scholarships
- Curricula
- Careers

without affecting existing graph semantics.

---

### Functional Scalability

Future intelligent services may include:

- Skill-based recommendation
- Curriculum comparison
- Personalized learning pathways
- Internship recommendation
- Career pathway planning
- Alumni network exploration

These services can reuse the existing graph structure.

---

# 12. Summary

This chapter presented the Knowledge Graph Design of the EduGuide platform.

Starting from the conceptual ontology defined in Chapter 4, the educational concepts were transformed into a graph representation capable of supporting efficient traversal, explainable reasoning, and intelligent recommendation.

The chapter introduced:

- Knowledge Graph design objectives;
- graph modeling principles;
- node and relationship design decisions;
- graph schema;
- graph constraints;
- indexing strategy;
- traversal patterns;
- integration with the Retrieval-Augmented Generation subsystem; and
- future graph evolution.

Unlike traditional relational databases, the Knowledge Graph models educational knowledge through explicit semantic relationships, enabling efficient multi-hop reasoning while preserving the meaning of educational concepts.

The resulting graph serves as the structured knowledge foundation of EduGuide and provides the basis for personalized recommendation, explainable artificial intelligence, and hybrid Retrieval-Augmented Generation.

The following chapter builds upon this graph by introducing the recommendation design, which utilizes the Knowledge Graph to identify suitable universities, programs, scholarships, and career pathways for individual students.

---

# Appendix A — Graph Modeling Standards

To ensure consistency throughout the EduGuide Knowledge Graph, the following modeling standards are adopted.

## Node Naming

Node labels use PascalCase.

Examples:

```text
University
Program
Curriculum
Scholarship
AdmissionRequirement
Career
Funder
```

---

## Relationship Naming

Relationship types use uppercase snake case.

Examples:

```text
OFFERS

HAS_CURRICULUM

HAS_ADMISSION_REQUIREMENT

TARGETS

AVAILABLE_AT

FUNDED_BY

HAS_REQUIREMENT

LEADS_TO
```

---

## Property Naming

Properties use lowercase snake case.

Examples

```text
program_id

application_deadline

organization_type

degree_level
```

---

## Identifier Convention

Every node possesses one immutable identifier.

Examples

```text
program_id

career_id

scholarship_id

funder_id
```

These identifiers are never reused or modified after creation.

---

# Appendix B — Design Decision Log

The following table summarizes the major graph modeling decisions made during the design process.

| Design Problem | Alternatives Considered | Selected Design | Justification |
|----------------|------------------------|-----------------|---------------|
| University | Node / Property | Node | Independent institution |
| Program | Node / Property | Node | Primary recommendation target |
| Curriculum | Embedded / Node | Node | Supports versioning |
| Scholarship | Child of University / Independent | Independent Node | Supports multiple funding organizations |
| Admission Requirement | Property / Node | Node | Shared eligibility concept |
| Career | Property / Node | Node | Reusable professional pathway |
| Funder | Enumeration / Node | Node | Independent funding organization |
| Relationship Direction | Query-oriented / Semantic | Semantic | Improves readability and explanation |

---

# Appendix C — Example Cypher Queries

The following example queries illustrate how the graph supports educational reasoning.

## Programs Offered by a University

```cypher
MATCH (u:University)-[:OFFERS]->(p:Program)
WHERE u.name = "Institute of Technology of Cambodia"
RETURN p;
```

---

## Scholarships for Data Science

```cypher
MATCH (s:Scholarship)-[:TARGETS]->(p:Program)
WHERE p.name = "Data Science"
RETURN s;
```

---

## Careers After Computer Science

```cypher
MATCH (p:Program)-[:LEADS_TO]->(c:Career)
WHERE p.name = "Computer Science"
RETURN c;
```

---

## Admission Requirements

```cypher
MATCH (p:Program)-[:HAS_ADMISSION_REQUIREMENT]->(r:AdmissionRequirement)
WHERE p.name = "Civil Engineering"
RETURN r;
```

---

## Scholarship Eligibility

```cypher
MATCH (s:Scholarship)-[:HAS_REQUIREMENT]->(r:AdmissionRequirement)
WHERE s.name = "ITC Government Scholarship"
RETURN r;
```

---

# Appendix D — Complete Knowledge Graph

```text
                    (:University)
                          │
                   [:OFFERS]
                          │
                    (:Program)
                  ┌────┴────┐
                  │         │
      [:HAS_CURRICULUM]   [:LEADS_TO]
                  │         │
          (:Curriculum)  (:Career)
                  │
                  │
          (:AdmissionRequirement)
                  ▲
                  │
 [:HAS_ADMISSION_REQUIREMENT]
                  │
             (:Program)

(:Scholarship)
      ├────────────[:TARGETS]────────────►(:Program)
      ├────────────[:AVAILABLE_AT]───────►(:University)
      ├────────────[:FUNDED_BY]──────────►(:Funder)
      └────────────[:HAS_REQUIREMENT]────►(:AdmissionRequirement)
```

---

# End of Chapter 5
