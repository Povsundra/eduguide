id: curriculum_aupp_computer_science

entity: Curriculum

basic_information:
  curriculum_year: 2025
  program: Bachelor of Science in ITM / Computer Science
  university: American University of Phnom Penh (AUPP)
  duration: 4 years
  total_credits: 121

curriculum_overview:
  educational_structure:
    - General Education
    - Information Technology Major
    - Elective Courses

  learning_progression:
    foundation:
      Students complete General Education and foundation mathematics/computing courses.

    specialization:
      Students complete Information Technology and Computer Science major courses.

    concentration:
      Students select upper-division electives based on their interests and career goals.

    experiential_learning:
      Students complete an internship and a compulsory Final Year Project.

  focus_areas:
    - Computer Science
    - Software Engineering
    - Programming
    - Web Development
    - Database Systems
    - Operating Systems
    - Networking
    - Information Technology Management

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
      - Learn core computer science principles.
    core_topics:
      - Computer Science
      - Data Structures
      - Computing Fundamentals

  year_3:
    learning_objectives:
      - Build professional software development skills.
    core_topics:
      - Operating Systems
      - Software Engineering
      - Web Development
      - Database Systems

  year_4:
    learning_objectives:
      - Apply knowledge through advanced electives and industry experience.
    core_topics:
      - Internship
      - Final Year Project
      - Advanced Electives

course_structure:

  general_education:

    required_credits: 46

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
      - Course selections may vary between students while meeting the required 46 credits.

  major:

    required_credits: 56

    selection_method:
      All major courses are compulsory.

    foundation_courses:

      - code: MATH 234A
        course: Analytic Geometry and Calculus I
        credits: 5

      - code: ITM 340
        course: Maths for Computing
        credits: 3

    required_courses:

      - code: CSCI 111
        course: Survey of Computer Science
        credits: 3

      - code: CSCI 121
        course: Computer Science I
        credits: 3

      - code: CSCI 221
        course: Computer Science II
        credits: 3

      - code: CSCI 241
        course: Foundations of Computing
        credits: 3

      - code: CSCI 251
        course: Data Structures
        credits: 3

      - code: CSCI 321A
        course: Assembly Language
        credits: 3

      - code: CSCI 331
        course: Operating Systems
        credits: 3

      - code: CSCI 421
        course: Programming Languages
        credits: 3

      - code: CSCI 431
        course: Computer Graphics
        credits: 3

      - code: CSCI 441
        course: Software Engineering
        credits: 3

      - code: INF 250
        course: Introduction to Web Development
        credits: 3

      - code: INF 651
        course: Front-end Web Development
        credits: 3

      - code: INF 652
        course: Database Design and Programming
        credits: 3

      - code: INF 653
        course: Back-end Web Development
        credits: 3

      - code: INTS 400
        course: Internship
        credits: 3

      - code: ITM 201
        course: Java Programming I
        credits: 3

  electives:

    required_credits: 19

    selection_method:
      Students must complete 19 credits of upper-division (300-level or above)
      elective courses. ITM 475 Final Year Project is compulsory within the
      elective requirement. Students select the remaining elective courses
      according to their interests and academic advisor approval.

    available_courses:

      - code: BUSN 370
        course: Management of Information Systems
        credits: 3

      - code: BUSN 370L
        course: Management of Information Systems Lab
        credits: 1

      - code: ITM 301
        course: Java Programming II
        credits: 3

      - code: ITM 305
        course: Cyber Security I
        credits: 3

      - code: ITM 350
        course: Project Management System
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

      - code: ITM 470
        course: Knowledge Management System
        credits: 3

      - code: ITM 475
        course: Final Year Project
        credits: 3
        compulsory: true

      - code: ITM 495
        course: Special Topics (ITM)
        credits: 3

      - code: MGMT 320
        course: Operations Management
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

  total_credits: 121

  internship:
    required: true

  capstone:
    required: true

  thesis:
    required: false

  minimum_gpa: 2.00

  other_requirements:
    - Complete all General Education requirements.
    - Complete all required Major courses.
    - Complete 19 elective credits.
    - Earn at least 45 upper-division (300-level or above) credits.
    - Maintain a minimum cumulative GPA of 2.00 for both AUPP and FHSU coursework.

related_entity_ids:
  program:
    - program_aupp_computer_science

source:
  - https://www.aupp.edu.kh/faculty-of-digital-technologies/bachelor-of-science-in-itm-computer-science/
  - https://www.aupp.edu.kh/general-education/

notes:
  - AUPP follows a flexible credit-based curriculum rather than a fixed semester-by-semester curriculum.
  - Students register for courses each semester with guidance from an academic advisor and must satisfy credit requirements in General Education, Major, and Elective categories.
  - General Education course selections vary among students, while all Major courses are compulsory. Elective courses are chosen from the program's approved upper-division elective list, with the Final Year Project being mandatory.