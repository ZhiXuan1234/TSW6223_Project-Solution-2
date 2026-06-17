# TSW6223 Solution 2: Semantic Career Path / Skill Gap Analysis

## 1. Solution Overview

Solution 2 focuses on the education domain, specifically the subdomain of Career Path / Skill Gap Analysis. The purpose of this solution is to help students understand how close their current skills are to a selected career path and what skills they still need to learn.

The system is designed as a semantic web-based prototype that uses XML as the structured data layer, XSD as the validation layer, RDF/RDFS as the semantic representation layer, SPARQL as the query layer, and Python as the implementation language.

The main idea is that a student can enter their current skills and select a target career. The system then compares the student's skills with the required skills of that career and produces a skill gap analysis. The output includes matched skills, missing skills, missing skill priority, career readiness score, recommended courses, and alternative career suggestions.

## 2. Problem Addressed

Students often struggle to choose suitable courses and career paths because they may not clearly understand the relationship between their current skills, course learning outcomes, and career requirements. A normal course list does not clearly show which skills are needed for a particular career or which courses can help close a skill gap.

This solution addresses the problem by structuring career, skill, and course data in a machine-readable format and using semantic web technologies to represent and query the relationships between them.

## 3. Planned System Architecture

The planned architecture for Solution 2 is:

```text
Real-world occupation and skill reference
        ↓
Selected prototype dataset
        ↓
career_skill_data.xml
        ↓ validated by
career_skill_schema.xsd
        ↓ parsed by Python
XML validation + input normalisation
        ↓
Convert XML to RDF/RDFS triples
        ↓
SPARQL query
        ↓
Terminal-based user interface output
```

The system will be built in stages:

1. Prepare the XML dataset.
2. Prepare the XSD schema for XML validation.
3. Validate the XML file using Python.
4. Parse the XML data using Python.
5. Normalise user skill input, including alias matching and typo handling.
6. Convert XML data into RDF/RDFS triples.
7. Use SPARQL queries to retrieve career, skill, and course relationships.
8. Display the skill gap analysis through a terminal-based user interface.
9. Conduct functional testing and document the results.

## 4. Semantic Web Technologies Used

### 4.1 XML

XML is used as the main structured data format. It stores data about sources, skills, careers, courses, and sample student profiles. XML is suitable because it allows the data to be organised in a clear hierarchical structure before being transformed into semantic triples.

### 4.2 XSD

XSD is used to validate the XML file. It ensures that the XML follows the correct structure and that important values are controlled. For example, the XSD checks that skill priority can only be `High`, `Medium`, or `Low`, and that career level can only be `Beginner`, `Intermediate`, or `Advanced`.

The XSD also validates references between elements. For example, when a career requires skill `SK001`, the schema ensures that `SK001` exists in the skills section.

### 4.3 RDF/RDFS

RDF/RDFS will be used after the XML data is parsed. The XML data will be converted into RDF triples so that relationships such as the following can be represented semantically:

```text
AI Engineer requiresSkill Machine Learning
Machine Learning isTaughtBy Machine Learning Fundamentals
Student hasSkill Python
```

RDFS will be used to define the classes and properties, such as `Student`, `Career`, `Skill`, `Course`, `hasSkill`, `requiresSkill`, and `teachesSkill`.

### 4.4 SPARQL

SPARQL will be used to query the RDF graph. Example query purposes include:

- Retrieve all skills required by a selected career.
- Retrieve all courses that teach missing skills.
- Retrieve prerequisite skills for recommended courses.
- Compare skill requirements across different careers.
- Support alternative career suggestions based on skill match percentage.

### 4.5 Python

Python is used to implement the system logic. Python will handle XML parsing, XML validation, skill input normalisation, RDF generation, SPARQL queries, skill gap calculation, and terminal-based output.

## 5. Dataset Preparation and Source Usage

The dataset is prepared as a small prototype dataset based on selected real-world occupation information from O*NET OnLine. O*NET is used because it provides occupation profiles, worker requirements, software skills, essential skills, and occupation-related information.

The system does not directly scrape or fetch live data from O*NET during runtime. Instead, a small selected chunk of relevant occupation information is manually reviewed and transformed into XML. This makes the prototype more stable for development, testing, and demonstration.

The dataset currently uses one source:

| Source ID | Source Name | Source URL | Usage |
|---|---|---|---|
| SRC001 | O*NET OnLine | https://www.onetonline.org/ | Used as the real-world reference for occupation descriptions, worker requirements, software skills, essential skills, and career-skill relationships. |

## 6. Career Mapping Used in the Dataset

Some modern job titles are not always available as exact O*NET occupation titles. Therefore, the project career names are mapped to the closest available O*NET occupation profiles.

| Project Career Name | O*NET Occupation Title Used | O*NET Code | Reason for Mapping |
|---|---|---|---|
| Data Analyst | Data Scientists | 15-2051.00 | Used as a close data-related occupation because O*NET search maps data analyst-related work to data science and business intelligence roles. |
| Software Developer | Software Developers | 15-1252.00 | Direct match with O*NET occupation title. |
| Cybersecurity Analyst | Information Security Analysts | 15-1212.00 | Used as the closest official O*NET occupation title for cybersecurity-related analysis work. |
| AI Engineer | Computer and Information Research Scientists | 15-1221.00 | Used as the closest occupation because O*NET does not list AI Engineer as a direct main occupation title. |

This mapping is stored directly in the XML using fields such as `sourceOccupationCode`, `sourceOccupationTitle`, and `sourceNote`.

## 7. Current XML Dataset Design

The XML file is named:

```text
career_skill_data.xml
```

It contains the following main sections:

### 7.1 dataSources

Stores information about the source used to prepare the prototype dataset.

### 7.2 skills

Stores the standard skill names, skill categories, and aliases. Aliases are included to support user input normalisation. For example, `py`, `python programming`, and `pyhton` can be mapped to the standard skill name `Python`.

### 7.3 careers

Stores the project career paths, their mapped O*NET occupation titles and codes, career level, source note, and required skills. Each required skill uses a skill ID reference and priority level.

### 7.4 courses

Stores recommended courses and the skills they teach. Some courses also include prerequisite skills to support learning path sequencing.

### 7.5 students

Stores a sample student profile for testing. This section can be used to test whether the system can compare a student's current skills with the selected target career.

## 8. Input Handling Plan

The system will include an input pre-processing layer to reduce matching problems caused by strict semantic resource names.

The planned input handling flow is:

```text
Input Layer:
- Accept comma-separated skills from user

Pre-processing Layer:
- Convert input to lowercase
- Remove extra spaces
- Match aliases, e.g. "ml" → "Machine Learning"
- Use fuzzy matching for typos, e.g. "pyhton" → "Python"
- Ask user to confirm correction

Semantic Layer:
- Convert confirmed skills to RDF resource names
- Run SPARQL queries using standardised skill names

Output Layer:
- Show matched skills
- Show missing skills
- Show readiness score
- Show recommended courses
- Show alternative careers
```

This design is important because SPARQL and RDF resource matching are strict. The input normalisation layer helps ensure that casual user input can still be matched to standardised skill names.

## 9. Expected System Output

A sample terminal output may look like this:

```text
===== Semantic Career Path / Skill Gap Analyzer =====

Available Careers:
1. Data Analyst
2. Software Developer
3. Cybersecurity Analyst
4. AI Engineer

Select your target career: AI Engineer

Enter your current skills:
pyhton, sql, ml

Input Validation:
- "pyhton" was corrected to "Python"
- "sql" matched to "SQL"
- "ml" matched to "Machine Learning"

Target Career: AI Engineer

Matched Skills:
- Python
- Machine Learning

Missing Skills by Priority:
[HIGH]
- Statistics

[MEDIUM]
- Data Visualization
- Problem Solving

Career Readiness Score: 40%

Recommended Learning Path:
1. Statistics for Data Analytics
2. Data Visualization Fundamentals
3. Problem Solving for Computing

Alternative Career Suggestions:
1. Software Developer - 60% match
2. Data Analyst - 40% match
3. Cybersecurity Analyst - 25% match
```

## 10. Why This Solution Has Novelty

The novelty of Solution 2 is that it does not only list missing skills. It adds a semantic and explainable skill gap analysis process.

The system includes:

- Real-world occupation mapping using O*NET.
- XML-based structured dataset.
- XSD-based data validation.
- Skill alias and typo handling before semantic matching.
- RDF/RDFS conversion for semantic relationships.
- SPARQL-based retrieval of career, skill, and course relationships.
- Career readiness score.
- Missing skill priority ranking.
- Recommended courses for missing skills.
- Alternative career suggestions based on skill match percentage.

## 11. Planned Functional Testing

Planned test cases include:

| Test Case ID | Test Description | Expected Result |
|---|---|---|
| S2-TC01 | Validate correct XML against XSD | XML validation successful |
| S2-TC02 | Enter invalid priority value in XML | XSD validation fails |
| S2-TC03 | Enter skill alias such as `ml` | System maps it to `Machine Learning` |
| S2-TC04 | Enter typo such as `pyhton` | System suggests or corrects to `Python` |
| S2-TC05 | Select AI Engineer with Python and SQL only | System shows matched and missing skills correctly |
| S2-TC06 | Missing skill has related course | System recommends the correct course |
| S2-TC07 | Student already has all required skills | Career readiness score becomes 100% |
| S2-TC08 | Unknown skill entered | System asks user to confirm or ignore the skill |

## 12. Future Improvements

Possible future improvements include:

- Integrating live data from O*NET or other career-skill APIs.
- Expanding the number of careers, skills, and courses.
- Aligning the system with ESCO for broader occupation-skill interoperability.
- Adding OWL inference to infer related or equivalent skills.
- Building a web-based user interface.
- Adding student login and saved skill profiles.
- Connecting Solution 2 with Solution 1 course recommendation.
- Using real university course data and programme structures.

## 13. Files in This Solution

The planned files are:

```text
solution2/
│
├── career_skill_data.xml
├── career_skill_schema.xsd
├── validate_xml.py
├── xml_to_rdf.py
├── career_skill_graph.ttl
├── main.py
└── README.md
```

## 14. Summary

Solution 2 is a semantic web-based Career Path / Skill Gap Analysis prototype. It uses a small O*NET-based dataset prepared in XML format and validated with XSD. The validated XML data will be parsed by Python and converted into RDF/RDFS triples. SPARQL will then be used to query the semantic relationships between careers, skills, and courses. The final result will be displayed through a terminal-based interface that provides students with matched skills, missing skills, readiness scores, recommended courses, and alternative career paths.
