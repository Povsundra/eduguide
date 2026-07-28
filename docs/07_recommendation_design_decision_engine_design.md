# 07 Recommendation Engine Design

# 1. Purpose

## 1.1 Overview

The Recommendation Engine is responsible for providing personalized educational recommendations based on a student's academic background, interests, preferences, and eligibility.

Unlike the Retrieval-Augmented Generation (RAG) subsystem, which retrieves existing educational knowledge to answer user questions, the Recommendation Engine performs decision-making by evaluating multiple educational options and ranking them according to their suitability for the student.

The recommendation process integrates structured knowledge from the Knowledge Graph, semantic knowledge from the RAG subsystem, and student-specific information to generate explainable recommendations.

The Recommendation Engine serves as the core intelligence of the EduGuide platform.

---

## 1.2 Relationship with Other Components

The Recommendation Engine collaborates with several major subsystems.

```text
Student
      │
      ▼
Recommendation Engine
      │
      ├────────► Knowledge Graph
      │
      ├────────► RAG
      │
      ├────────► Student Profile
      │
      └────────► LLM
```

Each component contributes different information.

| Component | Responsibility |
|------------|----------------|
| Knowledge Graph | Structured educational facts |
| RAG | Educational explanations |
| Student Profile | Student characteristics |
| Recommendation Engine | Ranking and decision making |
| LLM | Natural language explanation |

The Recommendation Engine acts as the decision layer between knowledge retrieval and response generation.

---

# 2. Design Objectives

The Recommendation Engine is designed to achieve the following objectives.

---

## Personalized Recommendation

Recommendations should reflect the student's individual characteristics rather than generic popularity.

Student attributes may include:

- academic performance
- preferred subjects
- interests
- financial constraints
- language preference
- career goals
- preferred study location

---

## Explainable Recommendation

Every recommendation should include a clear explanation describing why it was selected.

Example

```text
Recommended Program

Data Science

Reason

Strong mathematics background

Interest in AI

Career goal aligns with data analytics

Eligible scholarship available
```

Students should understand why a recommendation is appropriate.

---

## Knowledge-Driven Recommendation

All recommendations should be derived from verified educational knowledge contained in the Knowledge Graph and Knowledge Repository.

The Recommendation Engine should not rely on assumptions or unsupported information.

---

## Multi-Criteria Decision Making

Educational decisions involve multiple factors.

Examples include:

- academic ability
- eligibility
- career opportunities
- scholarship availability
- admission requirements
- university reputation
- personal interests

The Recommendation Engine evaluates these factors collectively rather than independently.

---

## Extensibility

The recommendation framework should support additional recommendation domains without requiring architectural redesign.

Future recommendation targets may include:

- internships
- exchange programs
- research opportunities
- graduate programs
- professional certifications

---

# 3. Design Principles

The Recommendation Engine follows several guiding principles.

---

## Student-Centered Design

Recommendations should prioritize the student's goals, abilities, and preferences rather than institutional preferences.

---

## Explainability

Every recommendation must be supported by objective evidence retrieved from the Knowledge Graph and Knowledge Repository.

The system should never produce unexplained rankings.

---

## Transparency

The recommendation process should expose the major factors influencing each recommendation.

This enables students to understand and trust the system.

---

## Modularity

Each recommendation stage should be implemented independently.

Examples include:

- profile analysis
- candidate generation
- filtering
- scoring
- ranking
- explanation generation

This modular architecture simplifies maintenance and future enhancements.

---

## Fairness

The Recommendation Engine should evaluate educational opportunities consistently across institutions.

Recommendations should not favor particular universities unless justified by student preferences or eligibility.

---

# 4. High-Level Recommendation Architecture

The Recommendation Engine consists of six major stages.

```text
Student Profile
        │
        ▼
Profile Analysis
        │
        ▼
Candidate Generation
        │
        ▼
Eligibility Filtering
        │
        ▼
Recommendation Scoring
        │
        ▼
Ranking
        │
        ▼
Explanation Generation
        │
        ▼
LLM Response
```

Each stage progressively narrows the available educational options and improves recommendation quality.

---

# 5. Recommendation Workflow

The complete recommendation workflow is illustrated below.

```text
Student Input
        │
        ▼
Student Profile Construction
        │
        ▼
Knowledge Graph Expansion
        │
        ▼
Candidate Generation
        │
        ▼
Eligibility Checking
        │
        ▼
Scoring
        │
        ▼
Ranking
        │
        ▼
Top-N Recommendations
        │
        ▼
RAG Explanation
        │
        ▼
Final Response
```

Unlike a traditional search engine, the Recommendation Engine evaluates educational opportunities before presenting results.

---

# 6. Recommendation Categories

EduGuide supports multiple recommendation types.

| Recommendation Type | Description |
|----------------------|-------------|
| University Recommendation | Recommend suitable universities |
| Program Recommendation | Recommend academic programs |
| Scholarship Recommendation | Recommend eligible scholarships |
| Career Recommendation | Recommend future careers |
| Learning Path Recommendation | Recommend learning progression |
| Combined Recommendation | Recommend complete education pathways |

Each category may use different evaluation criteria while sharing the same recommendation framework.

# 7. Student Profile Modeling

## 7.1 Purpose

The Student Profile represents the educational characteristics, preferences, and constraints used by the Recommendation Engine to generate personalized recommendations.

Rather than recommending educational opportunities based on general popularity, EduGuide evaluates each recommendation according to the individual student's profile.

The Student Profile acts as the primary input to the recommendation process.

---

# 7.2 Student Profile Structure

The Student Profile consists of several categories of information.

```text
Student Profile

├── Academic Information
├── Subject Performance
├── Interests
├── Skills
├── Career Goals
├── Financial Information
├── Study Preferences
└── Constraints
```

Each category contributes to different stages of the recommendation process.

---

# 7.3 Academic Information

Academic information describes the student's educational background.

Typical attributes include:

| Attribute | Description |
|-----------|-------------|
| Education Level | Grade 12, Undergraduate, etc. |
| Current School | Student's current institution |
| GPA | Current cumulative GPA |
| Graduation Year | Expected graduation year |
| National Examination Results | Optional examination scores |

Example

```json
{
    "education_level": "Grade 12",
    "gpa": 3.82,
    "graduation_year": 2027
}
```

Academic information is primarily used for eligibility checking.

---

# 7.4 Subject Performance

Many educational programs require strong performance in specific subjects.

The Recommendation Engine therefore models subject-level performance.

Example

| Subject | Grade |
|----------|-------|
| Mathematics | A |
| Physics | A |
| Chemistry | B+ |
| Biology | B |
| English | A |

This information is used to estimate academic suitability for different programs.

For example:

- Engineering programs emphasize Mathematics and Physics.
- Medical programs emphasize Biology and Chemistry.
- Business programs emphasize Mathematics and English.

---

# 7.5 Interests

Interests describe the student's preferred fields of study.

Examples include:

- Artificial Intelligence
- Data Science
- Civil Engineering
- Business
- Architecture
- Cybersecurity

Students may select multiple interests.

Example

```json
{
    "interests": [
        "Artificial Intelligence",
        "Data Science",
        "Software Development"
    ]
}
```

Interest matching is one of the strongest signals during recommendation.

---

# 7.6 Skills

Students may also provide their existing skills.

Examples include:

- Programming
- Mathematics
- Public Speaking
- Graphic Design
- Research
- Problem Solving

Skill information complements academic performance when evaluating program suitability.

---

# 7.7 Career Goals

Students may specify long-term career objectives.

Examples

- Data Scientist
- Software Engineer
- Civil Engineer
- Entrepreneur
- Researcher

Career goals allow the Recommendation Engine to recommend educational pathways that support the student's future aspirations.

---

# 7.8 Financial Information

Financial constraints significantly influence educational opportunities.

Examples include:

- Tuition budget
- Need for financial aid
- Scholarship preference
- Living expense considerations

This information is used during scholarship recommendation and university selection.

---

# 7.9 Study Preferences

Students may express personal preferences regarding their educational experience.

Examples include:

| Preference | Example |
|------------|---------|
| Preferred Language | Khmer, English |
| Preferred Province | Phnom Penh |
| Preferred Degree | Bachelor |
| Preferred University Type | Public, Private |
| Preferred Study Mode | Full-time |

These preferences help personalize recommendations beyond academic suitability.

---

# 7.10 Constraints

Constraints eliminate educational options that do not satisfy mandatory requirements.

Examples include:

- Minimum GPA requirements
- Geographic limitations
- Financial limitations
- Language requirements
- Degree availability

Constraints are treated as hard filters during recommendation.

---

# 8. User Preference Modeling

## 8.1 Purpose

While the Student Profile describes objective information, User Preference Modeling captures subjective preferences that influence recommendation ranking.

Preferences are not strict requirements but help prioritize suitable educational opportunities.

---

## Preference Categories

Examples include:

- preferred university
- preferred city
- preferred teaching language
- preferred tuition range
- preferred campus environment
- preferred scholarship type

These preferences adjust recommendation scores without excluding valid options.

---

## Preference Weighting

Each preference contributes a configurable weight to the final recommendation score.

For example:

| Preference | Weight |
|------------|-------:|
| Interest Match | 0.35 |
| Career Alignment | 0.25 |
| Academic Suitability | 0.20 |
| Financial Match | 0.10 |
| Location Preference | 0.05 |
| Language Preference | 0.05 |

The weights can be tuned during evaluation based on user feedback and recommendation performance.

---

# 9. Candidate Generation

## 9.1 Purpose

Candidate Generation identifies educational entities that may satisfy the student's profile before detailed scoring is performed.

Rather than evaluating every entity in the Knowledge Graph, the Recommendation Engine first creates a smaller set of relevant candidates.

This improves both efficiency and recommendation quality.

---

# 9.2 Candidate Sources

Candidate entities are retrieved from multiple knowledge sources.

| Source | Purpose |
|---------|---------|
| Knowledge Graph | Structured relationships |
| Vector Index | Semantic similarity |
| Student Profile | Personal constraints |

Each source contributes different evidence to the recommendation process.

---

# 9.3 Candidate Generation Workflow

```text
Student Profile
        │
        ▼
Knowledge Graph Search
        │
        ▼
Retrieve Candidate Entities
        │
        ▼
Remove Duplicates
        │
        ▼
Candidate Set
```

The resulting candidate set becomes the input for eligibility filtering.

---

# 9.4 Example

Student Interest

```text
Artificial Intelligence
```

Knowledge Graph

```text
Artificial Intelligence

↓

RELATED_TO

↓

Data Science

↓

Computer Science

↓

Software Engineering
```

Generated Candidates

- Bachelor of Data Science
- Bachelor of Computer Science
- Bachelor of Software Engineering

Instead of searching every available program, the Recommendation Engine focuses only on relevant candidates.

---

# 10. Knowledge Graph Expansion

## 10.1 Purpose

The Knowledge Graph enables the Recommendation Engine to discover related educational opportunities through graph traversal.

This allows recommendations to go beyond exact keyword matching.

---

## Example

Student Interest

```text
Machine Learning
```

Graph Traversal

```text
Machine Learning

↓

RELATED_TO

↓

Artificial Intelligence

↓

Program

↓

University

↓

Scholarship

↓

Career
```

The Recommendation Engine can therefore recommend:

- relevant academic programs;
- universities offering those programs;
- associated scholarships;
- related career opportunities.

---

## Advantages

Knowledge Graph expansion enables:

- discovery of related entities;
- richer recommendation candidates;
- explainable recommendation paths;
- improved coverage for incomplete student queries.

---

# 11. Eligibility Filtering

## 11.1 Purpose

Eligibility Filtering removes recommendation candidates that do not satisfy mandatory requirements.

This prevents unsuitable recommendations from reaching the ranking stage.

---

## Typical Eligibility Rules

Examples include:

- GPA requirement
- Education level
- Subject prerequisites
- Scholarship eligibility
- Language requirement
- Citizenship requirement (where applicable)

Only candidates satisfying mandatory criteria proceed to scoring.

---

## Example

Student

```text
GPA = 3.2
```

Scholarship Requirement

```text
Minimum GPA = 3.5
```

Result

```text
Filtered Out
```

---

## Output

The output of this stage is a validated candidate set that satisfies all mandatory eligibility conditions.

Only these candidates are forwarded to the Recommendation Scoring module.


# 12. Recommendation Scoring

## 12.1 Purpose

The Recommendation Scoring module evaluates each eligible candidate and assigns a numerical score representing its suitability for the student.

Rather than relying on a single criterion, EduGuide adopts a multi-criteria scoring approach that considers academic suitability, personal interests, career goals, financial needs, and student preferences.

The final recommendation score reflects how well an educational opportunity aligns with the student's overall profile.

---

# 12.2 Scoring Framework

Each recommendation candidate is evaluated using multiple scoring dimensions.

```text
Student Profile
        │
        ▼
Academic Score
        │
Interest Score
        │
Career Score
        │
Financial Score
        │
Preference Score
        │
Knowledge Graph Score
        │
        ▼
Final Recommendation Score
```

Each dimension captures a different aspect of suitability.

---

# 12.3 Scoring Dimensions

The Recommendation Engine evaluates six primary dimensions.

| Dimension | Description |
|-----------|-------------|
| Academic Suitability | Matches academic background with program requirements |
| Interest Alignment | Measures similarity between interests and programs |
| Career Alignment | Evaluates alignment with career goals |
| Financial Compatibility | Evaluates affordability and scholarship opportunities |
| Preference Match | Measures satisfaction of personal preferences |
| Graph Relationship Strength | Measures semantic closeness in the Knowledge Graph |

---

## Academic Suitability

Academic suitability estimates whether the student's educational background matches the requirements of the recommended program.

Evaluation factors include:

- GPA
- Mathematics performance
- Science performance
- English proficiency
- Required prerequisite subjects

Example

```text
Student

Mathematics = A

Physics = A

↓

Computer Science

Academic Score = 0.95
```

---

## Interest Alignment

Interest alignment measures how closely a student's interests correspond to a recommended program.

Example

```text
Interest

Artificial Intelligence

↓

Program

Data Science

Interest Score = 0.98
```

Knowledge Graph relationships may also contribute to interest matching.

---

## Career Alignment

Programs leading toward the student's desired career receive higher scores.

Example

```text
Career Goal

Data Scientist

↓

Program

Data Science

Career Score = 1.00
```

Programs with indirect relationships receive lower scores.

---

## Financial Compatibility

Financial compatibility evaluates affordability.

Examples include:

- tuition fee
- scholarship availability
- financial aid
- living expenses

Programs satisfying the student's financial constraints receive higher scores.

---

## Preference Match

Preference matching evaluates subjective preferences.

Examples include:

- preferred university
- preferred province
- preferred language
- preferred institution type

Preference matching personalizes recommendations without acting as strict eligibility requirements.

---

## Graph Relationship Strength

The Knowledge Graph provides additional signals through graph connectivity.

Example

```text
Student Interest

AI

↓

RELATED_TO

↓

Machine Learning

↓

Program

↓

University
```

Shorter graph paths generally indicate stronger semantic relationships.

---

# 12.4 Score Normalization

Each scoring dimension may use different numerical scales.

Before aggregation, all scores are normalized to a common range.

```text
0.0

↓

Least Suitable

1.0

↓

Most Suitable
```

Normalization ensures that no individual criterion dominates due to scale differences.

---

# 12.5 Weighted Score Calculation

The final recommendation score is computed as a weighted combination of all scoring dimensions.

Example

| Criterion | Weight |
|-----------|--------|
| Academic Suitability | 30% |
| Interest Alignment | 25% |
| Career Alignment | 20% |
| Financial Compatibility | 10% |
| Preference Match | 10% |
| Graph Relationship Strength | 5% |

The weights represent the relative importance of each criterion.

> **Implementation Note:** These weights are initial design values. During implementation, they should be configurable and tuned using user feedback, evaluation results, or learning-based optimization rather than remaining fixed.

---

# 12.6 Recommendation Score

Each candidate receives a final suitability score.

Example

| Candidate | Final Score |
|-----------|------------:|
| Data Science – ITC | 0.94 |
| Computer Science – RUPP | 0.89 |
| Software Engineering – CADT | 0.86 |

Higher scores indicate better overall suitability.

---

# 13. Ranking Algorithm

## 13.1 Purpose

After scoring, candidates are ranked according to their overall suitability.

Ranking determines the order in which recommendations are presented.

---

## Ranking Workflow

```text
Candidate Set

↓

Recommendation Scores

↓

Sort Descending

↓

Top-N Results
```

The highest-ranked candidates become the final recommendations.

---

## Top-N Recommendation

Rather than recommending only one option, EduGuide returns the top-ranked candidates.

Example

```text
Top 3 Programs

1. Data Science
2. Computer Science
3. Software Engineering
```

Providing multiple options allows students to compare alternatives and make informed decisions.

---

# 14. Score Fusion

## 14.1 Purpose

Different recommendation modules may produce independent scores.

For example:

- program recommendation;
- university recommendation;
- scholarship recommendation;
- career recommendation.

Score Fusion combines these results into a coherent educational pathway.

---

## Example

Program Score

```text
0.94
```

University Score

```text
0.91
```

Scholarship Score

```text
0.88
```

Combined Recommendation

```text
Institute of Technology of Cambodia

↓

Bachelor of Data Science

↓

ITC Government Scholarship
```

This creates an integrated recommendation rather than isolated suggestions.

---

# 15. Explanation Generation

## 15.1 Purpose

Every recommendation should include an explanation describing why it was selected.

Explainability increases user trust and helps students understand the recommendation process.

---

## Explanation Sources

The explanation is generated using:

- recommendation scores;
- Knowledge Graph relationships;
- retrieved educational knowledge;
- student profile.

---

## Example

Recommendation

```text
Bachelor of Data Science
```

Explanation

```text
Recommended because:

• Your mathematics and physics performance strongly matches the program requirements.

• Your interests in Artificial Intelligence and Data Science closely align with the curriculum.

• The program supports your goal of becoming a Data Scientist.

• You are eligible for scholarships associated with this program.
```

The explanation is grounded in objective evidence rather than generic statements.

---

# 16. Recommendation Evaluation

## Purpose

The Recommendation Engine should be evaluated to ensure it produces useful, accurate, and trustworthy recommendations.

---

## Evaluation Criteria

| Metric | Description |
|---------|-------------|
| Relevance | Recommendations match student needs |
| Personalization | Different profiles receive different results |
| Explainability | Recommendations include clear reasons |
| Eligibility Accuracy | Ineligible options are excluded |
| Diversity | Multiple suitable alternatives are presented |
| User Satisfaction | Students find recommendations useful |

---

## Example Test Case

Student Profile

```text
Interest

Artificial Intelligence

Career Goal

Data Scientist

Mathematics

A

Physics

A
```

Expected Recommendation

```text
✓ Data Science

✓ Computer Science

✓ Software Engineering
```

Recommendations unrelated to the student's profile should receive lower scores.

---

# 17. Future Improvements

Several enhancements are planned for future versions of the Recommendation Engine.

---

## Adaptive Weight Learning

Instead of predefined weights, future versions may learn scoring weights from historical interactions and user feedback.

---

## Collaborative Recommendation

Recommendations may incorporate anonymous behavioral patterns from similar students to complement profile-based recommendations.

---

## Dynamic User Profiles

Student profiles can evolve over time as interests, academic performance, and career goals change.

The Recommendation Engine should periodically update recommendations to reflect these changes.

---

## Reinforcement Learning

Future versions may optimize recommendation quality by learning from user acceptance, rejection, and follow-up interactions.

---

# 18. Summary

The Recommendation Engine is the decision-making component of the EduGuide platform.

Unlike the Retrieval-Augmented Generation subsystem, which retrieves and explains educational knowledge, the Recommendation Engine evaluates educational opportunities and ranks them according to each student's unique profile.

The design presented in this document includes:

- student profile modeling;
- preference modeling;
- candidate generation;
- Knowledge Graph expansion;
- eligibility filtering;
- multi-criteria recommendation scoring;
- ranking;
- score fusion;
- explanation generation; and
- evaluation.

By combining structured knowledge from the Knowledge Graph, contextual information from the RAG subsystem, and student-specific information, EduGuide provides personalized, explainable, and evidence-based educational recommendations.

The modular architecture also enables future enhancements such as adaptive weighting, collaborative recommendation, and learning-based optimization without requiring fundamental changes to the overall system.