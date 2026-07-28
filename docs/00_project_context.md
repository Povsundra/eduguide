## Knowledge Sources & Source of Truth

EduGuide integrates multiple knowledge sources. Each source has a clearly defined responsibility to ensure data consistency, explainability, and maintainability.

### Source of Truth

| Knowledge Domain | Primary Source | Purpose |
|------------------|----------------|---------|
| Universities | Knowledge Graph | University metadata, relationships, location, faculties, programs |
| Faculties | Knowledge Graph | Faculty hierarchy and relationships |
| Academic Programs / Majors | Knowledge Graph | Recommendation reasoning and graph traversal |
| Subjects | Knowledge Graph | Curriculum relationships and prerequisite knowledge |
| Skills | Knowledge Graph | Skill-to-major and skill-to-career matching |
| Careers | Knowledge Graph | Career pathways and required competencies |
| Scholarships | Knowledge Graph + Documents | Relationship reasoning with supporting evidence |
| Curriculum | Knowledge Graph + Documents | Program structure with detailed course information |
| Admission Requirements | Knowledge Graph + Documents | Structured requirements with official details |
| Tuition & Fees | Knowledge Graph + Documents | Structured comparison with official references |
| Government Policies | Documents | Official educational policies and regulations |
| University Regulations | Documents | University-specific policies and academic regulations |
| Career Information | Documents | Career descriptions, labor market information, and guidance |
| Student Profile | PostgreSQL | Assessment results, preferences, and extracted user profile |
| Conversation History | PostgreSQL | Multi-turn conversation memory |
| Retrieved Context | Qdrant | Retrieved document chunks used as evidence |
| Recommendation Scores | Runtime | Generated dynamically by the recommendation engine and never stored |
| LLM Responses | Runtime | Generated dynamically from retrieved evidence and never stored |

---

### Knowledge Sources

The knowledge base is constructed exclusively from trusted and publicly available educational resources.

#### Government Sources

- Ministry of Education, Youth and Sport (MoEYS)
- Cambodia Qualifications Framework
- National Education Strategic Plans
- Cambodia Digital Skills Development Roadmap
- Other official educational policies and publications

#### University Sources

- Official university websites
- Faculty pages
- Academic program descriptions
- Curriculum handbooks
- Admission guides
- Tuition fee schedules
- Scholarship announcements

#### Scholarship Sources

- University scholarships
- Government scholarships
- International scholarship programs
- Industry-sponsored scholarships

#### Career Sources

- National Employment Agency (NEA)
- Cambodia Digital Skills Roadmap
- Ministry publications
- Official career guidance resources

---

### Knowledge Boundary Policy

EduGuide only retrieves and reasons over knowledge that exists within its curated knowledge base.

If requested information is unavailable:

1. Never generate unsupported facts or hallucinated answers.
2. Clearly inform the user that the requested information is not available in the current knowledge base.
3. Provide any related verified information that is available.
4. Suggest alternative questions or related topics that the system can answer.
5. Every factual response should be grounded in the Knowledge Graph, retrieved documents, or both.

This policy ensures that recommendations remain trustworthy, explainable, and reproducible.