# 04. Ontology

**Document Version:** 1.0  
**Project:** EduGuide – An Agentic Retrieval-Augmented Decision Support System for Personalized Higher Education Guidance in Cambodia

---

# 1. Purpose

The EduGuide Ontology formally defines the conceptual knowledge model of Cambodia's higher education ecosystem used throughout the EduGuide platform.

Its purpose is to establish a shared semantic understanding of educational concepts, their meanings, properties, relationships, and constraints. The ontology provides a common vocabulary that enables different system components—including the Knowledge Graph, Recommendation Engine, Retrieval-Augmented Generation (RAG), AI Agents, and backend services—to interpret educational knowledge consistently.

Unlike the Domain Model, which describes real-world educational concepts from a business perspective, the ontology transforms those concepts into a formal conceptual model suitable for computational reasoning while remaining independent of any implementation technology.

The ontology serves as the semantic foundation upon which all intelligent capabilities of EduGuide are built.

---

# 2. Scope

Ontology Version 1 models only the educational concepts required to support personalized higher education guidance for Cambodian students.

The current ontology consists of seven core classes:

- University
- Program
- Curriculum
- Scholarship
- Admission Requirement
- Career
- Funder

These classes represent the minimum conceptual knowledge required to answer educational questions such as:

- Which university offers this program?
- Which scholarships are available?
- What admission requirements are required?
- What careers are related to this program?

The ontology intentionally excludes concepts outside the current research scope, including:

- Faculty
- Subject
- Skill
- Degree
- Industry
- Internship
- Student
- Lecturer
- Research Project
- Learning Outcome

These concepts are reserved for future ontology versions.

---

# 3. Ontology Design Principles

The EduGuide Ontology follows several fundamental design principles.

## 3.1 Semantic Clarity

Each ontology class represents exactly one educational concept.

Relationships describe meaningful educational semantics rather than database implementation details.

---

## 3.2 Technology Independence

The ontology is independent of implementation technologies such as Neo4j, RDF, OWL, SQL databases, APIs, or programming languages.

Implementation decisions are defined separately in the Graph Design document.

---

## 3.3 Reusability

Educational concepts should be reusable whenever possible.

For example, an Admission Requirement such as "High School Diploma" should be represented once and referenced by multiple Programs and Scholarships instead of being duplicated.

---

## 3.4 Extensibility

The ontology should support future expansion without requiring significant structural redesign.

Additional educational concepts can be incorporated through new classes and relationships while preserving existing semantics.

---

## 3.5 Explainability

Every relationship within the ontology should correspond to a meaningful real-world educational relationship that can be explained to students and educational stakeholders.

---

## 3.6 Minimalism

Only concepts required to satisfy the objectives of EduGuide Version 1 are included.

Concepts without immediate practical value are intentionally postponed to future versions.

---

# 4. Ontology Overview

The EduGuide Ontology models the core concepts of Cambodia's higher education ecosystem and the semantic relationships between them.

The ontology consists of seven core classes connected through eight object properties.

Each class represents an independent educational concept, while each relationship represents a meaningful semantic connection between those concepts.

The ontology is intentionally designed as a conceptual knowledge model rather than a database schema.

---

## 4.1 Core Ontology Structure

```text
University
 ├── OFFERS ─────────────────────────► Program
 │                                       ├── HAS_CURRICULUM ─────────────► Curriculum
 │                                       ├── HAS_ADMISSION_REQUIREMENT ─► AdmissionRequirement
 │                                       └── LEADS_TO ───────────────────► Career
 │
 └── AVAILABLE_AT ◄──────────────────── Scholarship
                                         ├── TARGETS ────────────────────► Program
                                         ├── FUNDED_BY ──────────────────► Funder
                                         └── HAS_REQUIREMENT ────────────► AdmissionRequirement
```

### Notes

- AdmissionRequirement is intentionally modeled as a reusable ontology class shared by both Programs and Scholarships.

- Scholarship is modeled as an independent class because financial sponsorship is conceptually separate from educational institutions.

- Curriculum exists only within the context of an academic Program.

- Career represents common professional pathways associated with graduates rather than guaranteed employment outcomes.

---

# 5. Ontology Classes

The ontology defines seven core classes that collectively represent the educational knowledge required by EduGuide.

Each class specifies its semantic purpose, attributes, object properties, and conceptual constraints.

---

# 5.1 University

## Purpose

Represents a recognized higher education institution that provides academic programs.

Universities serve as the primary educational providers within the EduGuide ecosystem.

---

## Definition

A University is an accredited institution responsible for delivering one or more academic programs leading to recognized educational qualifications.

---

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | String | Yes | Official university name |
| abbreviation | String | No | Common abbreviation |
| type | Enum | Yes | Public or Private |
| location | String | Yes | Province or city |
| website | URL | No | Official website |
| established_year | Integer | No | Year established |
| description | Text | No | Institutional overview |

---

## Object Properties

| Relationship | Target Class |
|--------------|--------------|
| OFFERS | Program |
| AVAILABLE_AT (inverse) | Scholarship |

---

## Conceptual Constraints

- Every University must have a unique identity.
- A University may offer multiple Programs.
- Universities exist independently of Programs and Scholarships.

---

# 5.2 Program

## Purpose

Represents an academic degree program offered by a university.

Programs are the primary recommendation target of EduGuide.

---

## Definition

A Program is a structured educational offering that leads to an academic qualification and prepares students for one or more professional career pathways.

---

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | String | Yes | Official program name |
| degree_level | Enum | Yes | Undergraduate, Graduate, Certificate |
| duration | Integer | Yes | Study duration |
| language | String | No | Instruction language |
| overview | Text | No | Program description |

---

## Object Properties

| Relationship | Target Class |
|--------------|--------------|
| BELONGS_TO (inverse) | University |
| HAS_CURRICULUM | Curriculum |
| HAS_ADMISSION_REQUIREMENT | Admission Requirement |
| LEADS_TO | Career |
| TARGETED_BY (inverse) | Scholarship |

---

## Conceptual Constraints

- Every Program belongs to exactly one University.
- Every Program must have at least one Curriculum.
- Every Program may have multiple Admission Requirements.
- Every Program may lead to multiple Career pathways.

---

# 5.3 Curriculum

## Purpose

Represents the official academic structure of a Program.

---

## Definition

A Curriculum defines the organization, sequence, and academic content of a Program throughout its duration.

The Curriculum has no independent meaning outside the Program to which it belongs.

---

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| academic_year | String | Yes | Curriculum version |
| total_credits | Integer | No | Total academic credits |
| duration | Integer | No | Number of study years |
| description | Text | No | Curriculum overview |

---

## Object Properties

| Relationship | Target Class |
|--------------|--------------|
| BELONGS_TO | Program |

---

## Conceptual Constraints

- Every Curriculum belongs to exactly one Program.
- A Program may have multiple Curriculum versions.
- Curriculum cannot exist independently of a Program.

---

# 5.4 Scholarship

## Purpose

Represents financial assistance available to eligible students pursuing higher education.

---

## Definition

A Scholarship is an independent financial opportunity funded by an organization and made available to one or more Universities and Programs according to defined eligibility requirements.

---

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | String | Yes | Scholarship name |
| scholarship_type | Enum | Yes | Merit, Need-based, Government, Industry, etc. |
| coverage | String | No | Tuition, stipend, accommodation, etc. |
| application_deadline | Date | No | Closing date |
| description | Text | No | Scholarship overview |

---

## Object Properties

| Relationship | Target Class |
|--------------|--------------|
| FUNDED_BY | Funder |
| TARGETS | Program |
| AVAILABLE_AT | University |
| HAS_REQUIREMENT | Admission Requirement |

---

## Conceptual Constraints

- Every Scholarship must have one Funder.
- A Scholarship may support multiple Programs.
- A Scholarship may be available at multiple Universities.
- Every Scholarship may define one or more eligibility requirements.

---

**End of Part 1**

The remaining ontology classes (Admission Requirement, Career, and Funder), object properties, semantic constraints, ontology rules, ontology boundary, versioning, and summary will be presented in **Part 2**.


# 5.5 Admission Requirement

## Purpose

Represents a condition that an applicant must satisfy before being admitted to an academic program or becoming eligible for a scholarship.

Admission Requirements are modeled as reusable concepts because the same requirement may apply to multiple Programs and Scholarships.

---

## Definition

An Admission Requirement represents an academic, administrative, financial, or documentary condition that must be fulfilled before admission or scholarship eligibility can be granted.

Unlike Curricula, Admission Requirements are independent ontology classes that can be shared across multiple educational entities.

---

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | String | Yes | Requirement name |
| category | Enum | Yes | Academic, Document, Financial |
| description | Text | No | Detailed explanation |
| mandatory | Boolean | No | Indicates whether the requirement is compulsory |

---

## Object Properties

| Relationship | Target Class |
|--------------|--------------|
| REQUIRED_BY (inverse) | Program |
| REQUIRED_BY (inverse) | Scholarship |

---

## Conceptual Constraints

- Admission Requirements are reusable.
- One Admission Requirement may apply to many Programs.
- One Admission Requirement may apply to many Scholarships.
- Admission Requirements have meaning independent of Programs.

---

# 5.6 Career

## Purpose

Represents professional career pathways commonly associated with graduates of an academic program.

Career entities enable EduGuide to explain potential employment opportunities after graduation.

---

## Definition

A Career represents a professional occupation that graduates of one or more academic Programs commonly pursue.

The relationship represents educational preparation rather than guaranteed employment.

---

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| title | String | Yes | Career title |
| industry | String | No | Related industry |
| description | Text | No | Career overview |

---

## Object Properties

| Relationship | Target Class |
|--------------|--------------|
| RELATED_TO (inverse) | Program |

---

## Conceptual Constraints

- A Career may be associated with multiple Programs.
- A Career exists independently of educational institutions.
- Career relationships describe common educational outcomes rather than employment guarantees.

---

# 5.7 Funder

## Purpose

Represents the organization responsible for financing scholarships.

Funders allow EduGuide to distinguish between university-funded, government-funded, NGO-funded, and industry-funded scholarship opportunities.

---

## Definition

A Funder is an organization that provides financial support for one or more Scholarships.

Funding organizations are independent educational stakeholders rather than educational providers.

---

## Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| name | String | Yes | Organization name |
| organization_type | Enum | Yes | Government, University, NGO, Industry, International |
| website | URL | No | Official website |
| description | Text | No | Organization overview |

---

## Object Properties

| Relationship | Target Class |
|--------------|--------------|
| FUNDS (inverse) | Scholarship |

---

## Conceptual Constraints

- One Funder may finance multiple Scholarships.
- Every Scholarship must have exactly one Funder.
- Funders exist independently of Universities.

---

# 6. Object Properties

Object Properties define the semantic relationships between ontology classes.

Unlike data properties, which describe attributes of a class, object properties describe how two concepts are related within the educational domain.

---

## 6.1 OFFERS

**Domain**

University

**Range**

Program

**Definition**

Indicates that a University officially provides an academic Program.

**Cardinality**

One University → Many Programs

**Inverse Relationship**

BELONGS_TO

---

## 6.2 HAS_CURRICULUM

**Domain**

Program

**Range**

Curriculum

**Definition**

Indicates that a Program is defined by one or more Curriculum versions.

**Cardinality**

One Program → One or More Curricula

**Inverse Relationship**

BELONGS_TO

---

## 6.3 HAS_ADMISSION_REQUIREMENT

**Domain**

Program

**Range**

Admission Requirement

**Definition**

Specifies the admission conditions required before students can enroll in a Program.

**Cardinality**

Many Programs ↔ Many Admission Requirements

**Inverse Relationship**

REQUIRED_BY

---

## 6.4 TARGETS

**Domain**

Scholarship

**Range**

Program

**Definition**

Indicates that a Scholarship is intended for students enrolled in specific academic Programs.

**Cardinality**

Many Scholarships ↔ Many Programs

**Inverse Relationship**

TARGETED_BY

---

## 6.5 AVAILABLE_AT

**Domain**

Scholarship

**Range**

University

**Definition**

Indicates that a Scholarship can be used at a specific University.

**Cardinality**

Many Scholarships ↔ Many Universities

**Inverse Relationship**

HAS_SCHOLARSHIP

---

## 6.6 FUNDED_BY

**Domain**

Scholarship

**Range**

Funder

**Definition**

Identifies the organization responsible for financing a Scholarship.

**Cardinality**

Many Scholarships → One Funder

**Inverse Relationship**

FUNDS

---

## 6.7 HAS_REQUIREMENT

**Domain**

Scholarship

**Range**

Admission Requirement

**Definition**

Specifies the eligibility requirements applicants must satisfy before receiving a Scholarship.

**Cardinality**

Many Scholarships ↔ Many Admission Requirements

**Inverse Relationship**

REQUIRED_BY

---

## 6.8 LEADS_TO

**Domain**

Program

**Range**

Career

**Definition**

Represents the professional career pathways commonly associated with graduates of a Program.

This relationship represents educational preparation rather than guaranteed employment.

**Cardinality**

Many Programs ↔ Many Careers

**Inverse Relationship**

RELATED_TO

---

# 7. Semantic Constraints

The ontology follows the following semantic constraints.

1. Every Program must belong to exactly one University.

2. Every Curriculum must belong to exactly one Program.

3. Every Scholarship must have exactly one Funder.

4. Every Scholarship must target at least one Program or be available at one University.

5. Every Career must be associated with at least one Program.

6. Admission Requirements are reusable across Programs and Scholarships.

7. Universities exist independently of Programs.

8. Scholarships exist independently of Universities.

9. Curriculum cannot exist independently of a Program.

10. Programs cannot exist independently of a University.

---

# 8. Ontology Rules

The ontology follows several domain-specific semantic rules.

---

## Rule 1

Educational providers are represented only by the University class.

---

## Rule 2

Programs are the primary recommendation targets within EduGuide.

---

## Rule 3

Curricula define the internal academic structure of Programs and cannot exist independently.

---

## Rule 4

Scholarships are independent educational opportunities rather than components of a University.

---

## Rule 5

Admission Requirements represent reusable educational concepts.

The same requirement may apply to multiple Programs and Scholarships.

---

## Rule 6

Career relationships represent educational pathways rather than employment guarantees.

---

## Rule 7

Ontology relationships describe semantic meaning only.

Implementation details such as graph databases, APIs, or storage models are defined separately.

---

# 9. Ontology Boundary

The EduGuide Ontology intentionally models only educational knowledge required for personalized higher education guidance.

Version 1 excludes the following concepts:

- Student Profiles
- Conversation History
- User Preferences
- Faculty Members
- Individual Subjects
- Course Prerequisites
- Skills
- Internship Opportunities
- Research Projects
- Employment Statistics
- University Rankings

These concepts belong to future ontology versions or other system components.

---

# 10. Ontology Versioning

## Version 1.0

Current ontology classes:

- University
- Program
- Curriculum
- Scholarship
- Admission Requirement
- Career
- Funder

---

## Planned Version 2

Additional educational concepts:

- Faculty
- Subject
- Degree
- Skill
- Industry
- Occupation

---

## Planned Version 3

Future ecosystem concepts:

- Internship
- Exchange Program
- Student Organization
- Learning Outcome
- Professional Certification

---

# 11. Relationship with Other Design Documents

The ontology provides the semantic foundation for subsequent system design documents.

```text
03.5 Domain Model
        │
        ▼
04 Ontology
        │
        ▼
05 Graph Design
        │
        ▼
06 Recommendation Design
        │
        ▼
07 RAG Design
```

The Domain Model explains the educational domain.

The Ontology formalizes educational concepts.

The Graph Design implements those concepts within Neo4j.

The Recommendation Engine reasons over the ontology.

The RAG system retrieves evidence associated with ontology concepts.

---

# 12. Summary

The EduGuide Ontology establishes the formal conceptual representation of Cambodia's higher education knowledge.

By defining standardized ontology classes, object properties, semantic constraints, reusable concepts, and knowledge boundaries, the ontology provides a shared semantic vocabulary for every intelligent component of the EduGuide platform.

This ontology serves as the conceptual bridge between the Domain Model and the Graph Design, ensuring that all subsequent implementation decisions remain consistent with the educational semantics of the domain while supporting future expansion of the EduGuide knowledge ecosystem.