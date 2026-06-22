# TSW6223 Solution 2: Semantic Career Path / Skill Gap Analysis

## 1. Solution Overview

Solution 2 focuses on the education domain, specifically the subdomain of **Career Path / Skill Gap Analysis**. The purpose of this solution is to help students understand how close their current skills are to a selected career path and what skills they still need to learn.

The system is implemented as a semantic web-based prototype using:

* **XML** as the structured data layer
* **XSD** as the XML validation layer
* **RDF/RDFS** as the semantic representation layer
* **SPARQL** as the semantic query layer
* **Python** as the implementation language
* **Flask** as the modern web dashboard framework
* **Tkinter** as the legacy popup GUI framework

A student selects a target career and enters their current skills. The system then analyses the student’s skills against the required skills of the selected career. The output includes matched skills, missing skills, missing skill priority, career readiness score, recommended courses, prerequisite skills, and alternative career suggestions.

The project includes three versions of the Skill Gap Analyzer interface. These versions use the same main semantic analysis concept, but they present the output in different ways.

1. **Modern Web Dashboard** (`py web_app.py`)
   A responsive Flask-based web interface with interactive skill tags, animated readiness scores, priority-grouped missing skills, recommended learning paths, and alternative career cards. It is accessed through a browser at `http://localhost:5000`.

2. **Legacy GUI Application** (`py main.py`)
   The original Tkinter popup window version. When `py main.py` is executed, the system validates the XML file, regenerates the RDF/RDFS Turtle file, runs SPARQL test queries, and then launches `gui_app.py`.

3. **Terminal-Based Analyzer** (`py skill_gap_analysis.py`)
   A command-line version of the same SPARQL-powered skill gap analyzer. This version is kept as a backup and testing-friendly interface.

Although these three versions use different interfaces, they perform the same core analysis purpose. They retrieve career and skill relationships from the RDF graph using SPARQL, normalise user skill input using XML aliases, compare the user’s skills with selected career requirements, calculate a readiness score, recommend courses for missing skills, and suggest alternative career paths.

---

## 2. Problem Addressed

Students often struggle to choose suitable courses and career paths because they may not clearly understand the relationship between their current skills, course learning outcomes, and career requirements. A normal career or course list does not clearly show which skills are needed for a particular career, which skills the student already has, which skills are missing, or which courses can help close the skill gap.

This solution addresses the problem by structuring career, skill, and course data in a machine-readable format and using semantic web technologies to represent and query the relationships between them.

The system supports skill-based career guidance by:

* comparing student skills with selected career requirements
* identifying matched and missing skills
* grouping missing skills by priority
* calculating a career readiness score
* recommending courses for missing skills
* showing prerequisite skills for recommended courses
* suggesting alternative careers based on the student’s current skills

---

## 3. Implemented System Architecture

The implemented architecture for Solution 2 is:

```text
Real-world occupation and skill reference
        ↓
Selected prototype dataset
        ↓
career_skill_data.xml
        ↓ validated by
career_skill_schema.xsd
        ↓ processed by Python
XML validation + input normalisation
        ↓
Convert XML to RDF/RDFS triples
        ↓
career_skill_graph.ttl
        ↓
SPARQL queries over RDF graph
        ↓
Terminal output OR Tkinter GUI output OR Web dashboard output
```

The system has three interaction options.

### Option A: Modern Web Dashboard

```text
py web_app.py
   ↓
Starts Flask server on http://localhost:5000
   ↓
User accesses responsive web dashboard
   ↓
User selects target career and enters skills through interactive tags
   ↓
System normalises input using aliases and typo handling through API
   ↓
System retrieves required skills and courses using SPARQL
   ↓
System displays readiness score, skill gaps, courses, and alternative careers
```

### Option B: Legacy GUI Application

```text
py main.py
   ↓
Validate XML using XSD
   ↓
Generate or update RDF/RDFS Turtle file
   ↓
Run SPARQL test queries in terminal
   ↓
Launch Tkinter GUI Skill Gap Analyzer
   ↓
User selects target career and enters skills
   ↓
System normalises input using aliases and typo handling
   ↓
System retrieves required skills and courses using SPARQL
   ↓
System displays skill gap analysis result in popup window
```

### Option C: Terminal-Based Analyzer

```text
py skill_gap_analysis.py
   ↓
Load RDF/RDFS Turtle graph
   ↓
Display available careers in terminal
   ↓
User selects target career and enters skills
   ↓
System normalises input using aliases and typo handling
   ↓
System retrieves required skills and courses using SPARQL
   ↓
System prints skill gap analysis result in terminal
```

---

## 4. Semantic Web Technologies Used

### 4.1 XML

XML is used as the main structured data format. It stores data about sources, skills, careers, courses, and sample student profiles. XML is suitable because it allows the data to be organised in a clear hierarchical structure before being transformed into semantic triples.

The XML file used in this solution is:

```text
career_skill_data.xml
```

The XML file stores:

* data sources
* skill names
* skill categories
* skill aliases
* career paths
* required skills for each career
* priority level of each required skill
* courses
* prerequisite skills
* sample student profile

### 4.2 XSD

XSD is used to validate the XML file. It ensures that the XML follows the correct structure and that important values are controlled before the data is processed.

For example, the XSD checks that:

* skill priority can only be `High`, `Medium`, or `Low`
* career level can only be `Beginner`, `Intermediate`, or `Advanced`
* skill category can only be `Technical` or `Essential`
* referenced skills, careers, and sources must exist in the XML file

The XSD file used in this solution is:

```text
career_skill_schema.xsd
```

### 4.3 RDF/RDFS

RDF/RDFS is used to convert the validated XML data into semantic triples. The generated RDF graph represents meaningful relationships such as:

```text
AI Engineer requiresSkill Machine Learning
Machine Learning Fundamentals teachesSkill Machine Learning
Data Visualization Fundamentals prerequisiteSkill Statistics
Sample Student hasSkill Python
Software Developer usesSource O*NET OnLine
```

RDFS is used to define semantic classes and properties, including:

```text
Classes:
- Source
- Skill
- Career
- Course
- Student
- SkillRequirement

Object Properties:
- requiresSkill
- teachesSkill
- prerequisiteSkill
- targetsCareer
- hasSkill
- usesSource
- hasRequirement
- requirementForCareer

Data Properties:
- skillName
- skillCategory
- alias
- careerName
- careerLevel
- sourceOccupationTitle
- sourceOccupationCode
- sourceNote
- courseName
- studentName
- priority
- sourceName
- sourceUrl
- description
```

The generated RDF/RDFS Turtle file is:

```text
career_skill_graph.ttl
```

This file can be regenerated by running:

```bash
py xml_to_rdf.py
```

or by running the legacy launcher:

```bash
py main.py
```

### 4.4 SPARQL

SPARQL is used to query the RDF graph. In the current implementation, SPARQL is used in the final application logic, not only for testing.

SPARQL is used to retrieve:

* available career options
* required skills for the selected career
* skill priority and skill category
* courses that teach missing skills
* prerequisite skills for recommended courses
* alternative career suggestions based on skill match percentage

This strengthens the solution because the final skill gap analysis retrieves semantic relationships from the RDF graph instead of relying only on static Python lists.

The SPARQL implementation can be seen in:

```text
skill_gap_analysis.py
gui_app.py
web_app.py
xml_to_rdf.py
```

The file `skill_gap_analysis.py` provides a terminal-based version of the analyzer. The file `gui_app.py` provides the Tkinter popup version. The file `web_app.py` provides the modern Flask web dashboard version. All three analyzer interfaces query the RDF graph using SPARQL to retrieve career options, required skills, course recommendations, prerequisite skills, and alternative career suggestions.

The file `xml_to_rdf.py` also runs SPARQL test queries after converting XML data into RDF/RDFS triples. These test queries are used to prove that the RDF graph can be queried successfully.

### 4.5 Python, Flask, and Tkinter

Python is used to implement the application logic. Python handles:

* XML validation using XSD
* XML parsing
* XML-to-RDF/RDFS conversion
* SPARQL query execution using RDFLib
* user input normalisation
* alias matching
* fuzzy typo correction
* readiness score calculation
* result display through terminal, GUI, or web dashboard

The project provides three user interaction methods:

| Interface           | File                    | Description                                                |
| ------------------- | ----------------------- | ---------------------------------------------------------- |
| Terminal Analyzer   | `skill_gap_analysis.py` | Runs the analyzer inside the command-line terminal.        |
| Tkinter GUI         | `gui_app.py`            | Opens a simple Python popup window for user interaction.   |
| Flask Web Dashboard | `web_app.py`            | Runs a browser-based dashboard at `http://localhost:5000`. |

---

## 5. Dataset Preparation and Source Usage

The dataset is prepared as a small prototype dataset based on selected real-world occupation information from **O*NET OnLine**. O*NET is used because it provides occupation profiles, worker requirements, software skills, essential skills, and occupation-related information.

The system does **not** directly scrape or fetch live data from O*NET during runtime. Instead, selected occupation information was manually reviewed and transformed into XML. This makes the prototype more stable for development, testing, and demonstration.

The dataset currently uses one source:

| Source ID | Source Name  | Source URL                  | Usage                                                                                                                                                 |
| --------- | ------------ | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| SRC001    | O*NET OnLine | https://www.onetonline.org/ | Used as the real-world reference for occupation descriptions, worker requirements, software skills, essential skills, and career-skill relationships. |

---

## 6. Career Mapping Used in the Dataset

Some modern job titles are not always available as exact O*NET occupation titles. Therefore, the project career names are mapped to the closest available O*NET occupation profiles.

| Project Career Name   | O*NET Occupation Title Used                  | O*NET Code | Reason for Mapping                                                                                                                           |
| --------------------- | -------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Data Analyst          | Data Scientists                              | 15-2051.00 | Used as a close data-related occupation because O*NET search maps data analyst-related work to data science and business intelligence roles. |
| Software Developer    | Software Developers                          | 15-1252.00 | Direct match with O*NET occupation title.                                                                                                    |
| Cybersecurity Analyst | Information Security Analysts                | 15-1212.00 | Used as the closest official O*NET occupation title for cybersecurity-related analysis work.                                                 |
| AI Engineer           | Computer and Information Research Scientists | 15-1221.00 | Used as the closest occupation because O*NET does not list AI Engineer as a direct main occupation title.                                    |
| Cloud Architect       | Computer Systems Analysts                    | 15-1211.00 | Used as a close occupation for analysing cloud-related system planning and architecture skills.                                              |
| Full Stack Developer  | Software Developers                          | 15-1252.00 | Mapped under software development because the role requires both frontend and backend software skills.                                       |
| Mobile Developer      | Software Developers                          | 15-1252.00 | Mapped under software development because mobile application development is part of software development work.                               |
| Systems Engineer      | Software Developers                          | 15-1252.00 | Mapped under software development because the prototype focuses on system-level programming and software-related skills.                     |

This mapping is stored directly in the XML using fields such as:

```text
sourceOccupationCode
sourceOccupationTitle
sourceNote
```

---

## 7. XML Dataset Design

The XML file is named:

```text
career_skill_data.xml
```

It contains the following main sections.

### 7.1 dataSources

The `dataSources` section stores information about the source used to prepare the prototype dataset.

Example:

```text
SRC001 → O*NET OnLine
```

### 7.2 skills

The `skills` section stores standard skill names, skill categories, and aliases. Aliases are included to support user input normalisation.

Examples:

```text
py → Python
python programming → Python
pyhton → Python
ml → Machine Learning
machien learning → Machine Learning
aws → Cloud Computing
github → Git
```

### 7.3 careers

The `careers` section stores the project career paths, mapped O*NET occupation titles and codes, career level, source note, and required skills. Each required skill uses a skill ID reference and priority level.

Example:

```text
AI Engineer requires Python, Machine Learning, Statistics, TensorFlow, Critical Thinking, and other related skills.
```

### 7.4 courses

The `courses` section stores recommended courses and the skills they teach. Some courses also include prerequisite skills to support learning path sequencing.

Example:

```text
Machine Learning Fundamentals teaches Machine Learning and TensorFlow.
Prerequisite skills: Python and Statistics.
```

### 7.5 students

The `students` section stores a sample student profile for testing. The actual application allows users to enter their own skills through the terminal, GUI, or web dashboard.

---

## 8. Input Handling Design

The system includes an input pre-processing layer to reduce matching problems caused by strict semantic resource names.

The input handling flow is:

```text
Input Layer:
- Accept skills from the user through terminal, GUI, or web dashboard

Pre-processing Layer:
- Convert input to lowercase
- Remove extra spaces
- Match aliases, e.g. "ml" → "Machine Learning"
- Use fuzzy matching for typos, e.g. "pythn" → "Python"
- Confirm or display suggested corrections depending on the interface

Semantic Layer:
- Use confirmed standardised skill names
- Retrieve career and course data from RDF graph using SPARQL

Output Layer:
- Show matched skills
- Show missing skills
- Show missing skills by priority
- Show readiness score
- Show recommended courses
- Show prerequisite skills
- Show alternative careers
```

This design is important because RDF and SPARQL matching are strict. The input normalisation layer helps ensure that casual user input can still be matched to standardised skill names.

Different interfaces handle fuzzy matching slightly differently:

| Interface         | Input Handling Behaviour                                                                       |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| Terminal Analyzer | Asks the user to enter `Y` or `N` when a fuzzy suggestion is found.                            |
| Tkinter GUI       | Shows a popup confirmation box when a fuzzy suggestion is found.                               |
| Web Dashboard     | Automatically accepts fuzzy corrections and displays the correction in the dashboard response. |

---

## 9. How to Run the Application in Visual Studio Code

This section explains how to run the project using **Visual Studio Code**.

### 9.1 Open the Project Folder in Visual Studio Code

1. Open **Visual Studio Code**.
2. Click **File** from the top menu.
3. Click **Open Folder**.
4. Select the project folder:

```text
TSW6223_Project-Solution-2
```

5. Click **Select Folder** or **Open**.
6. After opening the folder, make sure the Explorer panel shows the project files, such as:

```text
career_skill_data.xml
career_skill_schema.xsd
career_skill_graph.ttl
xml_to_rdf.py
skill_gap_analysis.py
gui_app.py
web_app.py
main.py
README.md
static/
templates/
testing/
```

### 9.2 Open a New Terminal in Visual Studio Code

After opening the project folder, open a new terminal from the top menu:

```text
Terminal → New Terminal
```

A terminal window will appear at the bottom of Visual Studio Code.

Make sure the terminal is opened in the main project folder. The terminal path should end with something similar to:

```text
TSW6223_Project-Solution-2>
```

If the terminal is not in the correct folder, close it and open **Terminal → New Terminal** again after selecting the project folder in VS Code.

### 9.3 Install the Required Python Libraries

In the Visual Studio Code terminal, install the required libraries by running:

```bash
py -m pip install lxml rdflib flask
```

The required libraries are:

| Library  | Purpose                                                 |
| -------- | ------------------------------------------------------- |
| `lxml`   | Used to validate the XML file against the XSD schema.   |
| `rdflib` | Used to create RDF/RDFS triples and run SPARQL queries. |
| `flask`  | Used to run the modern web-based dashboard.             |

Tkinter is used for the legacy GUI popup window. It is normally included with standard Python installations on Windows, so no extra installation is usually needed.

---

## 10. Running the Different Interfaces

### 10.1 Run the Modern Web Interface

To launch the modern Flask-based web dashboard:

```bash
py web_app.py
```

Then open your browser and go to:

```text
http://localhost:5000
```

The web dashboard allows the user to:

* select a target career
* enter skills using interactive tags
* receive alias and typo handling
* view an animated readiness score
* view confirmed skills and missing skills
* view missing skills by priority
* view recommended courses
* view prerequisite skills
* view alternative career suggestions
* switch between dark and light themes

Important note:

```text
web_app.py does not run through main.py by default. It is run separately because it starts a Flask web server.
```

### 10.2 Run the Legacy GUI Application

To run the full end-to-end backend pipeline and launch the Tkinter popup GUI:

```bash
py main.py
```

The application will automatically perform the following steps:

```text
1. Validate career_skill_data.xml using career_skill_schema.xsd
2. Generate or update career_skill_graph.ttl using xml_to_rdf.py
3. Run SPARQL test queries in the terminal
4. Launch the GUI Skill Gap Analyzer popup window using gui_app.py
```

After Step 3, a popup window will appear where the user can select a career, enter skills, and view the result in the output box.

By default, `main.py` launches:

```text
gui_app.py
```

The terminal-based analyzer is available as a backup option inside `main.py` through a commented line:

```text
analysis_success = run_python_file("skill_gap_analysis.py")
```

To use the terminal analyzer through `main.py`, the developer may change the default launcher line from `gui_app.py` to `skill_gap_analysis.py`.

### 10.3 Run the Terminal-Based Analyzer

To run the terminal-based backup version directly:

```bash
py skill_gap_analysis.py
```

This version runs fully inside the terminal. The user selects a target career by number, enters their current skills, and receives the skill gap analysis result as terminal text.

Before running `skill_gap_analysis.py`, make sure the RDF graph has already been generated by running either:

```bash
py xml_to_rdf.py
```

or:

```bash
py main.py
```

### 10.4 Run XML to RDF/RDFS Conversion Only

To regenerate the RDF/RDFS Turtle graph only:

```bash
py xml_to_rdf.py
```

This command reads `career_skill_data.xml`, converts it into RDF/RDFS triples, saves the output as `career_skill_graph.ttl`, and runs SPARQL test queries.

### 10.5 Run Validation or Testing Files

The same Visual Studio Code terminal can also be used to run the validation and testing files.

To run XML validation only:

```bash
py testing/validate_xml.py
```

To test XML parsing:

```bash
py testing/parse_xml.py
```

To test skill input normalisation:

```bash
py testing/skill_normalizer.py
```

Important:

```text
Run these commands from the main project folder, not from inside the testing folder.
```

---

## 11. Example System Output

### 11.1 Backend Processing Output

When running `py main.py`, the terminal first shows the backend semantic processing:

```text
===== Step 1: XML Validation =====
XML validation successful.
career_skill_data.xml follows the structure defined in career_skill_schema.xsd.

===== Step 2: XML to RDF/RDFS Conversion =====
Generating or updating career_skill_graph.ttl...
Reading XML file...
Creating RDF graph...
Adding RDFS schema...
Converting XML data into RDF triples...
Saving RDF graph to career_skill_graph.ttl...
RDF conversion completed successfully.

===== SPARQL Test 1: Careers and Required Skills =====
AI Engineer requires Machine Learning
Software Developer requires Python

===== SPARQL Test 2: Courses and Skills They Teach =====
Machine Learning Fundamentals teaches Machine Learning
Python Programming teaches Python

===== Step 3: Launch Skill Gap Analyzer =====
A popup window will open for user interaction.
```

### 11.2 Sample Analyzer Output

A sample analyzer result may include:

```text
Target Career: AI Engineer
O*NET Source Title: Computer and Information Research Scientists
O*NET Code: 15-1221.00
Career Level: Advanced

Confirmed Current Skills:
- Python
- Machine Learning

Required Skills Retrieved Using SPARQL:
- Python
- Machine Learning
- Statistics
- Data Visualization
- Problem Solving

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

Recommended Learning Path Retrieved Using SPARQL:
1. Statistics for Data Analytics
2. Data Visualization Fundamentals
3. Problem Solving for Computing

Alternative Career Suggestions Retrieved Using SPARQL:
1. Data Analyst - 40% match
2. Full Stack Developer - 40% match
3. Software Developer - 40% match
```

The exact result may differ depending on the selected career, the current XML dataset, and the skills entered by the user.

---

## 12. Functional Testing

Recommended test cases include:

| Test Case ID | Test Description                                                 | Expected Result                                                                |
| ------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| S2-TC01      | Validate correct XML against XSD                                 | XML validation successful                                                      |
| S2-TC02      | Enter invalid priority value in XML                              | XSD validation fails                                                           |
| S2-TC03      | Enter skill alias such as `ml`                                   | System maps it to `Machine Learning`                                           |
| S2-TC04      | Enter typo such as `pyhton` or `pythn`                           | System maps or suggests correction to `Python`                                 |
| S2-TC05      | Select Software Developer with Python only                       | System shows Python as matched and other required skills as missing            |
| S2-TC06      | Missing skill has related course                                 | System recommends the correct course using SPARQL                              |
| S2-TC07      | Student already has all required skills                          | Career readiness score becomes 100%                                            |
| S2-TC08      | Unknown skill entered                                            | System marks it as unknown or asks user to confirm correction                  |
| S2-TC09      | Run `py main.py`                                                 | XML validation, RDF generation, SPARQL test, and GUI analyzer run successfully |
| S2-TC10      | Delete or rename `career_skill_graph.ttl`, then run `py main.py` | TTL file is regenerated automatically                                          |
| S2-TC11      | Enter `pythn` in the GUI                                         | Popup asks whether the user meant `Python`                                     |
| S2-TC12      | Run `py web_app.py`                                              | Flask server starts and the dashboard is accessible at `http://localhost:5000` |
| S2-TC13      | Enter skills in the web dashboard                                | System validates skills and returns analysis through the dashboard             |
| S2-TC14      | Run `py skill_gap_analysis.py`                                   | Terminal-based analyzer runs and displays skill gap results                    |

---

## 13. Files in This Solution

```text
TSW6223_Project-Solution-2/
│
├── career_skill_data.xml
├── career_skill_schema.xsd
├── career_skill_graph.ttl
├── xml_to_rdf.py
├── skill_gap_analysis.py
├── gui_app.py
├── web_app.py
├── main.py
├── README.md
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
└── testing/
    ├── validate_xml.py
    ├── parse_xml.py
    └── skill_normalizer.py
```

### 13.1 Main Files

| File                      | Purpose                                                                                                                                                                                                                                      |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `career_skill_data.xml`   | Stores the structured career, skill, course, source, alias, and sample student data.                                                                                                                                                         |
| `career_skill_schema.xsd` | Validates the XML structure, controlled values, and ID references.                                                                                                                                                                           |
| `career_skill_graph.ttl`  | Generated RDF/RDFS Turtle graph created from the XML data.                                                                                                                                                                                   |
| `xml_to_rdf.py`           | Converts XML data into RDF/RDFS triples and runs SPARQL test queries.                                                                                                                                                                        |
| `skill_gap_analysis.py`   | Terminal-based SPARQL-powered skill gap analyzer. It performs the same core analysis but displays the result in the command-line terminal.                                                                                                   |
| `gui_app.py`              | Tkinter popup version of the SPARQL-powered skill gap analyzer. This is the default interface launched by `main.py`.                                                                                                                         |
| `web_app.py`              | Flask web dashboard version of the SPARQL-powered skill gap analyzer. It performs the same core analysis but displays the result through a browser-based interface.                                                                          |
| `main.py`                 | Legacy launcher that validates XML, regenerates RDF/RDFS, runs SPARQL test queries through `xml_to_rdf.py`, and starts `gui_app.py` by default. The terminal version can be used by switching the commented line to `skill_gap_analysis.py`. |
| `README.md`               | Project explanation, architecture summary, file description, and running instructions.                                                                                                                                                       |

### 13.2 Web Interface Files

| File                   | Purpose                                                                             |
| ---------------------- | ----------------------------------------------------------------------------------- |
| `static/css/style.css` | Design system with dark/light themes, animations, and responsive layout.            |
| `static/js/app.js`     | Frontend logic for skill tag input, API calls, and dashboard rendering.             |
| `templates/index.html` | HTML template for the two-state web interface, from input view to result dashboard. |

### 13.3 Testing Files

| File                          | Purpose                                                         |
| ----------------------------- | --------------------------------------------------------------- |
| `testing/validate_xml.py`     | Tests XML validation against XSD.                               |
| `testing/parse_xml.py`        | Tests whether Python can correctly read and extract XML data.   |
| `testing/skill_normalizer.py` | Tests alias matching and typo handling for user-entered skills. |

---

## 14. Novelty of the Solution

The novelty of Solution 2 is that it does not only list missing skills. It provides a semantic and explainable skill gap analysis by combining XML, XSD, RDF/RDFS, SPARQL, Python, Flask, and a modern web dashboard.

The system includes:

* source-tracked career data based on O*NET occupation profiles
* XML validation using XSD
* RDF/RDFS semantic representation
* SPARQL-powered retrieval of careers, skills, courses, prerequisites, and alternatives
* skill alias matching and fuzzy typo correction
* missing skill priority ranking
* career readiness score calculation
* course recommendation with prerequisite display
* alternative career suggestions based on skill match percentage
* modern responsive web dashboard with dark/light theme support
* interactive skill tag input with real-time validation
* Tkinter GUI as an alternative popup interface
* terminal-based analyzer as a backup and testing interface

This makes the solution more meaningful than a simple static career list because the system can connect career requirements, user skills, courses, and learning paths through semantic relationships.

---

## 15. Future Improvements

Possible future improvements include:

* Integrating live data from O*NET or other career-skill APIs.
* Expanding the number of careers, skills, and courses.
* Aligning the system with ESCO for broader occupation-skill interoperability.
* Adding OWL inference to infer related or equivalent skills.
* Adding student login and saved skill profiles.
* Saving user analysis history for future comparison.
* Connecting Solution 2 with Solution 1 course recommendation.
* Using real university course data and programme structures.
* Adding more advanced scoring logic based on skill priority weight.
* Allowing users to export the analysis result as PDF.

---

## 16. Summary

Solution 2 is a semantic web-based Career Path / Skill Gap Analysis prototype. It uses a small O*NET-based dataset prepared in XML format and validated with XSD. The validated XML data is converted into RDF/RDFS triples and saved as a Turtle file. SPARQL is then used in the final application to query semantic relationships between careers, skills, and courses.

The system provides three ways to interact with the analyzer:

1. **Modern Web Dashboard**
   Run `py web_app.py` and open `http://localhost:5000` in a browser. This interface features interactive skill tags with validation, an animated readiness score, priority-grouped skill gaps, course recommendation timeline, alternative career cards, and dark/light theme support.

2. **Legacy GUI Application**
   Run `py main.py` to execute XML validation, RDF/RDFS conversion, and SPARQL test queries in the terminal, followed by a Tkinter popup window through `gui_app.py`.

3. **Terminal-Based Analyzer**
   Run `py skill_gap_analysis.py` to use the command-line version of the same SPARQL-powered skill gap analysis. This version is mainly kept as a backup and testing-friendly interface.

All three analyzer interfaces use the same semantic web foundation. They rely on XML/XSD for structured data and validation, RDF/RDFS for semantic representation, and SPARQL for retrieving career requirements, recommended courses, prerequisite skills, and alternative career suggestions.

The final output helps students understand their current career readiness, identify missing skills, follow a suitable learning path, and explore alternative careers based on their existing skills.
