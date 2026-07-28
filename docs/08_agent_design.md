# 08 Agent Design

# 1. Purpose

## 1.1 Overview

The Agent Layer is responsible for orchestrating the intelligent components of the EduGuide platform.

Rather than directly answering user questions, the Agent Layer coordinates specialized services such as the Recommendation Engine, Hybrid Graph RAG subsystem, and Large Language Model (LLM) to solve educational tasks.

The primary objective of the Agent Layer is to determine:

- what the user wants,
- which subsystem should be invoked,
- in what order tasks should be executed, and
- how intermediate results should be combined into a final response.

By separating orchestration from knowledge retrieval and recommendation logic, the system becomes more modular, maintainable, and extensible.

---

## 1.2 Role in the EduGuide Architecture

The Agent Layer operates above the Knowledge Graph, RAG subsystem, and Recommendation Engine.

```text
                        Student
                           │
                           ▼
                    Agent Layer
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Recommendation      Hybrid Graph RAG     Comparison
      Engine
        │                  │
        └──────────────┬───┘
                       ▼
                 Large Language Model
                       ▼
                Final AI Response
```

The Agent Layer coordinates these components without duplicating their internal logic.

---

# 2. Design Objectives

The Agent Layer is designed to achieve the following objectives.

## Intelligent Task Planning

Interpret user requests and determine the appropriate execution workflow.

---

## Modular Orchestration

Assign responsibilities to specialized agents rather than allowing one component to perform every task.

---

## Efficient Resource Utilization

Invoke only the services required to answer a particular question.

---

## Explainability

Maintain traceable execution steps and preserve supporting evidence throughout the workflow.

---

## Extensibility

Allow future educational services to be integrated without redesigning the entire architecture.

---

# 3. Design Principles

The Agent Layer follows several architectural principles.

---

## Single Responsibility

Each agent performs one clearly defined responsibility.

---

## Service Reuse

Agents coordinate existing services rather than reimplementing them.

---

## Structured Communication

Agents exchange structured data instead of natural language.

---

## Shared Workflow State

All agents operate on a shared execution state.

---

## Framework Independence

The design does not depend on a specific orchestration framework such as LangGraph, CrewAI, or AutoGen.

---

# 4. Coordinator-Based Multi-Agent Architecture

EduGuide adopts a Coordinator-Based Multi-Agent Architecture.

A central Planner Agent coordinates specialized agents responsible for recommendation, retrieval, comparison, and response generation.

```text
                          Student
                              │
                              ▼
                      Planner Agent
                              │
      ┌──────────────┬────────┴────────┬──────────────┐
      ▼              ▼                 ▼              ▼
Recommendation   Retrieval Agent  Comparison Agent  Response Agent
    Agent
      │              │                 │
      ▼              ▼                 ▼
Recommendation   Hybrid Graph RAG   Comparison Logic
    Engine
      │              │
      └──────────────┴───────────────┐
                                     ▼
                           Large Language Model
                                     │
                                     ▼
                               Final Response
```

The Planner Agent never performs retrieval or recommendation itself.

Instead, it coordinates specialized components.

---

# 5. Agent Responsibilities

The Agent Layer consists of five specialized agents.

| Agent | Primary Responsibility |
|--------|------------------------|
| Planner Agent | Workflow orchestration |
| Recommendation Agent | Personalized recommendation |
| Retrieval Agent | Hybrid Graph RAG retrieval |
| Comparison Agent | Educational comparison |
| Response Agent | Response generation |

Each agent performs a single well-defined role.

---

# 6. Planner Agent

## Purpose

The Planner Agent serves as the central coordinator of the EduGuide platform.

It analyzes the student's request and determines which specialized agents should be invoked.

---

## Responsibilities

The Planner Agent is responsible for:

- query understanding;
- intent detection;
- task decomposition;
- workflow planning;
- execution coordination;
- result aggregation.

---

## Example

Student Question

```text
Which university is best for AI,
what scholarships are available,
and compare the top two universities?
```

Execution Plan

```text
1. Recommend programs
2. Recommend universities
3. Retrieve scholarships
4. Compare universities
5. Generate response
```

The Planner Agent coordinates these tasks sequentially.

---

# 7. Recommendation Agent

## Purpose

The Recommendation Agent is responsible for generating personalized educational recommendations.

Rather than implementing recommendation logic directly, it invokes the Recommendation Engine defined in Document 07.

---

## Responsibilities

- construct student profile;
- invoke Recommendation Engine;
- receive ranked recommendations;
- return structured recommendation results.

---

## Inputs

- student profile;
- recommendation request.

---

## Outputs

```json
{
    "recommended_programs": [...],
    "recommended_universities": [...],
    "recommended_scholarships": [...]
}
```

---

# 8. Retrieval Agent

## Purpose

The Retrieval Agent provides grounded educational knowledge by invoking the Hybrid Graph RAG subsystem.

It retrieves both structured graph facts and semantic document evidence.

---

## Responsibilities

- graph retrieval;
- vector retrieval;
- metadata filtering;
- retrieval fusion;
- citation collection.

---

## Inputs

Structured retrieval request.

---

## Outputs

```json
{
    "graph_facts": [...],
    "semantic_chunks": [...],
    "citations": [...]
}
```

The Retrieval Agent never generates natural language responses.

---

# 9. Comparison Agent

## Purpose

The Comparison Agent performs structured comparisons between educational entities.

Supported comparisons include:

- universities;
- programs;
- scholarships;
- curricula.

---

## Responsibilities

- retrieve comparable entities;
- identify comparable attributes;
- organize structured comparison results.

---

## Example

```text
Compare

ITC

and

CADT
```

Output

```json
{
    "comparison": {...}
}
```

---

# 10. Response Agent

## Purpose

The Response Agent transforms structured outputs into a natural language response.

It is the only agent that communicates with the Large Language Model.

---

## Responsibilities

- assemble context;
- construct prompts;
- invoke the LLM;
- generate explanations;
- preserve citations;
- format responses.

---

## Inputs

- recommendation results;
- retrieved knowledge;
- comparison results.

---

## Outputs

Student-friendly educational response.

---

# 11. Shared Workflow State

All agents share a common execution state.

```text
Workflow State

├── Student Profile
├── Current Task
├── Recommendation Results
├── Retrieved Knowledge
├── Comparison Results
├── Conversation Context
└── Execution History
```

Agents update this shared state rather than communicating through free-form text.

---

# 12. Agent Communication

Agents exchange structured messages.

Example

Planner Agent

↓

```json
{
    "task":"recommend_program",
    "student_profile": {...}
}
```

Recommendation Agent

↓

```json
{
    "recommended_programs":[...]
}
```

Planner Agent

↓

```json
{
    "task":"retrieve_program_information"
}
```

Retrieval Agent

↓

```json
{
    "graph_facts":[...],
    "semantic_chunks":[...]
}
```

This communication protocol simplifies debugging and future expansion.

---

# 13. Workflow Orchestration

The following example illustrates a complete execution workflow.

Student Question

```text
I enjoy Artificial Intelligence.

My GPA is 3.8.

Which university should I attend?

Can I apply for scholarships?
```

Execution

```text
Planner Agent

↓

Recommendation Agent

↓

Recommendation Engine

↓

Retrieval Agent

↓

Hybrid Graph RAG

↓

Response Agent

↓

LLM

↓

Final Response
```

Each component performs only its designated responsibility.

---

# 14. Error Handling

The Agent Layer includes recovery strategies for common failures.

| Failure | Recovery Strategy |
|----------|-------------------|
| Recommendation Engine unavailable | Continue with informational retrieval only |
| Neo4j unavailable | Fall back to semantic retrieval |
| Vector Index unavailable | Return graph facts only |
| LLM unavailable | Return structured information without natural language generation |

These strategies improve system robustness.

---

# 15. Future Extensions

The modular architecture enables additional agents to be introduced in future versions.

Examples include:

- Scholarship Agent
- Admission Agent
- Career Planning Agent
- Internship Recommendation Agent
- Exchange Program Agent
- Interview Preparation Agent

Each new agent can be integrated without modifying existing components.

---

# 16. Evaluation

The Agent Layer is evaluated according to:

- workflow correctness;
- task routing accuracy;
- response latency;
- successful task completion;
- agent collaboration;
- fault recovery.

These metrics ensure that the orchestration layer operates reliably.

---

# 17. Summary

The Agent Layer serves as the intelligent orchestration component of the EduGuide platform.

Rather than replacing the Recommendation Engine or Hybrid Graph RAG subsystem, the Agent Layer coordinates these specialized services to solve complex educational tasks.

The Coordinator-Based Multi-Agent Architecture promotes modularity, maintainability, and scalability by assigning each agent a single responsibility while maintaining a shared workflow state and structured communication protocol.

This design provides a robust foundation for future AI capabilities while remaining independent of any specific agent framework or implementation technology.