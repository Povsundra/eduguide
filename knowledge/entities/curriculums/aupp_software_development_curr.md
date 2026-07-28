id: curriculum_aupp_software_development

entity: Curriculum

basic_information:
  curriculum_year: 2025
  program: Bachelor of Science in Software Development
  university: American University of Phnom Penh (AUPP)
  duration: 4 years
  total_credits: 120

curriculum_overview:
  educational_structure:
    - General Education
    - Software Development Major
    - Core Major
    - Elective Courses

  learning_progression:
    foundation:
      Students complete General Education together with mathematics, programming, and computer science foundation courses.

    specialization:
      Students complete Software Development core courses covering software engineering, full-stack web development, software quality assurance, and modern development practices.

    concentration:
      Students select upper-division elective courses based on their interests and career goals.

    experiential_learning:
      Students complete a compulsory Internship and Final Year Project.

  focus_areas:
    - Software Development
    - Software Engineering
    - Full-Stack Web Development
    - Backend Development
    - Frontend Development
    - Software Quality Assurance
    - Linux
    - Version Control

year_structure:

  year_1:
    learning_objectives:
      - Develop university-level communication skills.
      - Build mathematics and programming foundations.
    core_topics:
      - General Education
      - Mathematics
      - Programming

  year_2:
    learning_objectives:
      - Learn core computer science and software development principles.
    core_topics:
      - Computer Science
      - Data Structures
      - Networking
      - Software Analysis and Design

  year_3:
    learning_objectives:
      - Develop professional software engineering and web development skills.
    core_topics:
      - Software Engineering
      - Frontend Development
      - Backend Development
      - Software Quality Assurance

  year_4:
    learning_objectives:
      - Apply software engineering knowledge through advanced electives and industry experience.
    core_topics:
      - Internship
      - Final Year Project
      - Advanced Electives

course_structure:

  general_education:

    required_credits: 31

    selection_method:
      Students complete the university's General Education curriculum.
      ITEC 101 is a required General Education course.
      Remaining courses are selected from approved General Education categories
      according to university graduation requirements.

    required_course:
      - code: ITEC 101
        course: Introduction to Information Technology
        credits: 3

    elective_categories:
      - English Composition
      - Oral Communication
      - Mathematics
      - Natural Sciences
      - Humanities
      - Social Sciences
      - Arts
      - Wellness
      - Other General Education courses defined by the AUPP Catalog

    notes:
      - Students work with their academic advisor to satisfy all General Education requirements.
      - Course selections may vary between students while meeting the required 31 credits.

  major:

    required_credits: 44

    selection_method:
      All major courses are compulsory.

    foundation_courses:

      - code: MATH 234A
        course: Analytical Geometry and Calculus I
        credits: 5

      - code: ITM 340
        course: Maths for Computing
        credits: 3

    required_courses:

      - code: COSC 111
        course: Computer Science Survey
        credits: 3

      - code: COSC 121
        course: Computer Science A
        credits: 3

      - code: COSC 221
        course: Computer Science B
        credits: 3

      - code: COSC 241
        course: Computing Science Fundamentals
        credits: 3

      - code: COSC 251
        course: Data Structure
        credits: 3

      - code: COSC 331
        course: Operating Systems
        credits: 3

      - code: COSC 340
        course: Networking Essentials
        credits: 3

      - code: ICT 301
        course: Software Analysis and Design
        credits: 3

      - code: ICT 320
        course: Cybersecurity Technician
        credits: 3

      - code: INFO 652
        course: Programming and Database Design
        credits: 3

      - code: ITM 201
        course: Java Programming I
        credits: 3

      - code: ITM 340
        course: Maths for Computing
        credits: 3

      - code: ITM 350
        course: Project Management
        credits: 3

      - code: MATH 234A
        course: Analytical Geometry and Calculus I
        credits: 5

  core_major:

    required_credits: 27

    selection_method:
      All Core Major courses are compulsory.

    required_courses:

      - code: SFW 371
        course: Introduction to Web Development
        credits: 3

      - code: SFW 372
        course: Software Engineering Fundamentals and Life Cycle
        credits: 3

      - code: SFW 373
        course: Frontend Web Development Using JavaScript
        credits: 3

      - code: SFW 374
        course: Software Quality Assurance
        credits: 3

      - code: SFW 375
        course: Linux Fundamentals & Version Control
        credits: 3

      - code: SFW 450
        course: Backend Web Development Using NodeJS
        credits: 3

      - code: SFW 451
        course: Backend Web Development Using Java
        credits: 3

      - code: ITM 475
        course: Final Year Project
        credits: 3

      - code: INTS 400
        course: Internship
        credits: 3

  electives:

    required_credits: 18

    selection_method:
      Students must complete 18 credits of approved upper-division elective
      courses. Students select elective courses according to their interests
      and academic advisor approval.

    available_courses:

      - code: ICT 401
        course: Innovation and Design Thinking
        credits: 3

      - code: ICT 405
        course: Ethical Hacking
        credits: 3

      - code: ICT 406
        course: Advance Ethical Hacking
        credits: 3

      - code: ITM 360
        course: Artificial Intelligence
        credits: 3

      - code: ITM 370
        course: Data Analytics
        credits: 3

      - code: ITM 380
        course: Cloud Computing
        credits: 3

      - code: ITM 381
        course: Cloud Solutions Architect
        credits: 3

      - code: ITM 390
        course: Machine Learning
        credits: 3

      - code: ITM 454
        course: Natural Language Processing
        credits: 3

practical_components:

  laboratory:
    available: true

  internship:
    required: true
    course: INTS 400
    credits: 3

  capstone:
    required: true
    course: ITM 475 Final Year Project
    credits: 3

  projects:
    - Final Year Project

  research:
    - Final Year Project

  field_work:
    available: false

graduation_requirements:

  total_credits: 120

  internship:
    required: true

  capstone:
    required: true

  thesis:
    required: false

  minimum_gpa: 2.00

  other_requirements:
    - Complete 31 General Education credits.
    - Complete all required Major courses.
    - Complete all Core Major courses.
    - Complete 18 elective credits.
    - Maintain a minimum cumulative GPA of 2.00.

related_entity_ids:
  program:
    - program_aupp_software_development

source:
  - https://www.aupp.edu.kh/faculty-of-digital-technologies/bachelor-of-science-in-software-development/
  - https://www.aupp.edu.kh/general-education/

notes:
  - AUPP follows a flexible credit-based curriculum rather than a fixed semester-by-semester curriculum.
  - Students register for courses each semester with guidance from an academic advisor.
  - All Major and Core Major courses are compulsory.
  - Students complete approved elective courses to satisfy the 18-credit elective requirement.
  - Internship and Final Year Project are compulsory graduation requirements.