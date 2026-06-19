import re
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
# re                          - Used to clean text when creating safe RDF resource names.
# xml.etree.ElementTree as ET - Used to read and parse the XML file.
# rdflib                      - Used to create and manipulate the RDF graph.
# Graph                       - Creates the RDF graph.
# Namespace                   - Creates the project RDF namespace.
# RDF                         - Used for RDF vocabulary, such as rdf:type.
# RDFS                        - Used for RDFS vocabulary, such as rdfs:Class and rdfs:label.
# Literal                     - Used for text values in RDF triples.
# URIRef                      - Used for RDF URI references, but in the current code it is imported (EX[make_uri_name(skill_name)]) and not really used.

# ------------------------------------------------------------
# Purpose:
# This file converts career_skill_data.xml into RDF/RDFS triples.
#
# Why this is important:
# XML stores structured data, but RDF represents the data as
# semantic relationships that can be queried using SPARQL.
#
# Example RDF meaning:
# AIEngineer requiresSkill Python
# MachineLearningFundamentals teachesSkill MachineLearning
# SampleStudent targetsCareer AIEngineer
# ------------------------------------------------------------


XML_FILE        = "career_skill_data.xml"
OUTPUT_TTL_FILE = "career_skill_graph.ttl"

# XML namespace used in career_skill_data.xml
# - Use the XML namespace when searching XML tags
XML_NS          = {"cs": "https://tsw6223.example.edu/career-skill"}

# RDF namespace for our project resources
# - Use ex: as the RDF namespace for project resources
# Example:
# http://example.org/career-skill#Python
# http://example.org/career-skill#AIEngineer
EX              = Namespace("http://example.org/career-skill#")


def get_text(parent, tag_name):
    """
    Safely get text from a child XML element. 
    (Helper Function to avoid repetitive code when extracting text from XML elements.)
    """
    element = parent.find(f"cs:{tag_name}", XML_NS)

    # Return the stripped text if the element exists and has text, otherwise return an empty string.
    if element is not None and element.text is not None:
        return element.text.strip()

    return ""


def make_uri_name(text):
    """
    Convert normal text into a safe RDF resource name, using python built-in functions.
    (Helper Function to create valid RDF resource names from text.)

    Example:
    "AI Engineer" -> "AIEngineer"
    "Machine Learning Fundamentals" -> "MachineLearningFundamentals"

    RDF resource names should not contain spaces or special symbols.
    """
    # Delete anything that is NOT a letter, digit, or space.
    cleaned_text = re.sub(r"[^A-Za-z0-9 ]", "", text) 

    # Remove spaces to create a single word for the RDF resource name.
    parts = cleaned_text.split()

    # Join the parts together to form a single string without spaces.
    return "".join(parts)


def create_graph():
    """
    Create an empty RDF graph and bind namespace prefixes.
    """
    g = Graph()

    # Bind prefixes to make the Turtle output easier to read.
    # Instead of writing full URI every time, Turtle can use ex:Python.
    g.bind("ex", EX)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)

    return g


def add_rdfs_schema(g):
    """
    Add and define RDFS classes and properties.

    This is the RDFS part of Category 2.
    It defines the meaning of the main classes and relationships.
    """

    # -------------------------
    # Define main classes
    # -------------------------
    classes = [
        "Source",
        "Skill",
        "Career",
        "Course",
        "Student",
        "SkillRequirement"
    ]

    for class_name in classes:
        # g.add(...)     - RDFLib method to add a triple
        # EX[class_name] - Creates project resource URI
        # RDF.type       - RDF vocabulary for “is a type of”
        # RDFS.Class     - RDFS vocabulary for class
        g.add((EX[class_name], RDF.type, RDFS.Class))
        # Example: ex:Skill rdf:type rdfs:Class

    # -------------------------
    # Define object properties
    # Object properties connect one resource to another resource.
    # Example: AIEngineer requiresSkill Python
    # -------------------------
    object_properties = {
        "requiresSkill": "Career requires a skill",             # eg. ex:AIEngineer  ex:requiresSkill  ex:Python
        "teachesSkill": "Course teaches a skill",               # eg. ex:PythonCourse  ex:teachesSkill  ex:Python
        "prerequisiteSkill": "Course has a prerequisite skill", # eg. ex:PythonCourse  ex:prerequisiteSkill  ex:Statistics
        
        # Used for sample XML student data. GUI user input is processed directly
        # by Python and is not currently saved as a new RDF Student resource.
        "targetsCareer": "Student targets a career",            # eg. ex:Student1  ex:targetsCareer  ex:AIEngineer
        "hasSkill": "Student has a skill",                      # eg. ex:Student1  ex:hasSkill  ex:Python
        
        "usesSource": "Career uses a data source",              # eg. ex:AIEngineer  ex:usesSource  ex:SRC001

        # These two properties make it easier for SPARQL
        # to retrieve the priority of each career-skill requirement.
        "hasRequirement": "Career has a skill requirement record",
        "requirementForCareer": "Skill requirement belongs to a career"
    }

    for property_name, label in object_properties.items():
        g.add((EX[property_name], RDF.type, RDF.Property))
        g.add((EX[property_name], RDFS.label, Literal(label)))

    # -------------------------
    # Define data properties
    # Data properties connect a resource to a text/value.
    # Example: Python skillCategory "Technical"
    # -------------------------
    data_properties = {
        "skillName": "Skill name",                         # eg. ex:Python  ex:skillName  "Python"
        "skillCategory": "Skill category",                 # eg. ex:Python  ex:skillCategory  "Technical"
        "alias": "Skill alias",                            # eg. ex:Python  ex:alias  "py"
        "careerName": "Career name",                       # eg. ex:AIEngineer  ex:careerName  "AI Engineer"
        "careerLevel": "Career level",                     # eg. ex:AIEngineer  ex:careerLevel  "Advanced"
        "sourceOccupationTitle": "O*NET occupation title", # eg. ex:AIEngineer  ex:sourceOccupationTitle  "Computer and Information Research Scientists"
        "sourceOccupationCode": "O*NET occupation code",   # eg. ex:AIEngineer  ex:sourceOccupationCode  "15-1221.00"
        "sourceNote": "Source mapping note",               # eg. ex:AIEngineer  ex:sourceNote  "Mapped from O*NET occupation title"
        "courseName": "Course name",                       # eg. ex:PythonCourse  ex:courseName  "Introduction to Python"
        "studentName": "Student name",                     # eg. ex:Student1  ex:studentName  "Alice"
        "priority": "Skill priority",                      # eg. ex:AIEngineer_Python_Requirement  ex:priority  "High"
        "sourceName": "Source name",                       # eg. ex:AIEngineer  ex:sourceName  "O*NET OnLine"
        "sourceUrl": "Source URL",                         # eg. ex:SRC001  ex:sourceUrl  "https://www.onetonline.org/"
        "description": "Description"                       # eg. ex:SRC001  ex:description  "Used as a real-world reference..."
    }

    for property_name, label in data_properties.items():
        g.add((EX[property_name], RDF.type, RDF.Property))
        g.add((EX[property_name], RDFS.label, Literal(label)))


def convert_sources(root, g):
    """
    Take the <dataSources> section from the XML and convert each <source> into RDF triples.
    """

    source_uri_map = {}

    for source in root.findall("cs:dataSources/cs:source", XML_NS):
        source_id = source.get("id")
        source_name = get_text(source, "sourceName")
        source_url = get_text(source, "sourceUrl")
        description = get_text(source, "description")

        source_uri = EX[make_uri_name(source_id)]

        g.add((source_uri, RDF.type, EX.Source))
        g.add((source_uri, EX.sourceName, Literal(source_name)))
        g.add((source_uri, EX.sourceUrl, Literal(source_url)))
        g.add((source_uri, EX.description, Literal(description)))

        source_uri_map[source_id] = source_uri

    return source_uri_map


def convert_skills(root, g):
    """
    Convert <skills> XML data into RDF triples.

    Return:
    skill_uri_map:
        {
            "SK001": ex:Python,
            "SK002": ex:SQL
        }
    - skill_uri_map is used before SPARQL, during XML-to-RDF conversion.
    - SPARQL later queries the RDF triples that have already been created.
    - XML stores references using IDs like SK001.
    - Python first creates ex:Python from the skill record.
    - Then Python maps SK001 to ex:Python.
    - Later, careers/courses/students use SK001 references (eg. ref = SK001, which is used as the attribute inside the element)
      , and Python uses the map to create correct RDF relationships.
    """

    skill_uri_map = {}

    for skill in root.findall("cs:skills/cs:skill", XML_NS):
        skill_id = skill.get("id")
        skill_name = get_text(skill, "skillName")
        skill_category = get_text(skill, "skillCategory")

        skill_uri = EX[make_uri_name(skill_name)]

        g.add((skill_uri, RDF.type, EX.Skill))
        g.add((skill_uri, EX.skillName, Literal(skill_name)))
        g.add((skill_uri, EX.skillCategory, Literal(skill_category)))

        # Add aliases as literal values
        for alias in skill.findall("cs:aliases/cs:alias", XML_NS):
            if alias.text:
                g.add((skill_uri, EX.alias, Literal(alias.text.strip())))

        skill_uri_map[skill_id] = skill_uri

    return skill_uri_map


def convert_careers(root, g, skill_uri_map, source_uri_map):
    """
    Convert <careers> XML data into RDF triples.
    - Notes: convert_careers() links careers to required skills and stores priority.

    Example triples:
    ex:AIEngineer rdf:type ex:Career
    ex:AIEngineer ex:requiresSkill ex:Python
    ex:AIEngineer ex:priority "High"
    """

    career_uri_map = {}

    for career in root.findall("cs:careers/cs:career", XML_NS):
        career_id = career.get("id")
        source_ref = career.get("sourceRef")
        source_occupation_code = career.get("sourceOccupationCode")

        career_name = get_text(career, "careerName")
        source_occupation_title = get_text(career, "sourceOccupationTitle")
        career_level = get_text(career, "careerLevel")
        source_note = get_text(career, "sourceNote")

        career_uri = EX[make_uri_name(career_name)]

        g.add((career_uri, RDF.type, EX.Career))
        g.add((career_uri, EX.careerName, Literal(career_name)))
        g.add((career_uri, EX.sourceOccupationTitle, Literal(source_occupation_title)))
        g.add((career_uri, EX.sourceOccupationCode, Literal(source_occupation_code)))
        g.add((career_uri, EX.careerLevel, Literal(career_level)))
        g.add((career_uri, EX.sourceNote, Literal(source_note)))

        # Link career to source, such as O*NET
        if source_ref in source_uri_map:
            g.add((career_uri, EX.usesSource, source_uri_map[source_ref]))

        # Link career to required skills
        for required_skill in career.findall("cs:requiredSkills/cs:requiredSkill", XML_NS):
            skill_ref = required_skill.get("ref")
            priority = required_skill.get("priority")

            if skill_ref in skill_uri_map:
                skill_uri = skill_uri_map[skill_ref]

                # Main semantic relationship:
                # Career requires Skill
                g.add((career_uri, EX.requiresSkill, skill_uri))

                # Store priority using a reified-like simple node.
                # This lets us keep priority for each career-skill relationship.
                #
                # Example:
                # AIEngineer_Python_Requirement priority High
                requirement_uri = EX[
                    make_uri_name(career_name)
                    + "_"
                    + make_uri_name(str(skill_uri).split("#")[-1])
                    + "_Requirement"
                ]

                # This requirement node stores extra information about the
                # relationship between one career and one required skill.
                #
                # Example:
                # AI Engineer requires Machine Learning with High priority.
                g.add((requirement_uri, RDF.type, EX.SkillRequirement))

                # Link the career to the requirement node.
                g.add((career_uri, EX.hasRequirement, requirement_uri))

                # Link the requirement node back to the career.
                g.add((requirement_uri, EX.requirementForCareer, career_uri))

                # Link the requirement node to the required skill.
                g.add((requirement_uri, EX.requiresSkill, skill_uri))

                # Store the priority of this required skill for this career.
                g.add((requirement_uri, EX.priority, Literal(priority)))

        career_uri_map[career_id] = career_uri

    return career_uri_map


def convert_courses(root, g, skill_uri_map):
    """
    Convert <courses> XML data into RDF triples.
    - Notes: convert_courses() links courses to taught skills and prerequisite skills.

    Example triples:
    ex:MachineLearningFundamentals rdf:type ex:Course
    ex:MachineLearningFundamentals ex:teachesSkill ex:MachineLearning
    ex:MachineLearningFundamentals ex:prerequisiteSkill ex:Statistics
    """

    course_uri_map = {}

    for course in root.findall("cs:courses/cs:course", XML_NS):
        course_id = course.get("id")
        course_name = get_text(course, "courseName")

        course_uri = EX[make_uri_name(course_name)]

        g.add((course_uri, RDF.type, EX.Course))
        g.add((course_uri, EX.courseName, Literal(course_name)))

        for teaches_skill in course.findall("cs:teachesSkill", XML_NS):
            skill_ref = teaches_skill.get("ref")

            if skill_ref in skill_uri_map:
                g.add((course_uri, EX.teachesSkill, skill_uri_map[skill_ref]))

        for prerequisite_skill in course.findall("cs:prerequisiteSkill", XML_NS):
            skill_ref = prerequisite_skill.get("ref")

            if skill_ref in skill_uri_map:
                g.add((course_uri, EX.prerequisiteSkill, skill_uri_map[skill_ref]))

        course_uri_map[course_id] = course_uri

    return course_uri_map


def convert_students(root, g, skill_uri_map, career_uri_map):
    """
    Convert optional <students> XML data into RDF triples.
    Notes: The student conversion here is mainly for the sample student record in the XML and future support for saved student profiles.
    """

    for student in root.findall("cs:students/cs:student", XML_NS):
        student_id = student.get("id")
        student_name = get_text(student, "studentName")

        student_uri = EX[make_uri_name(student_id)]

        g.add((student_uri, RDF.type, EX.Student))
        g.add((student_uri, EX.studentName, Literal(student_name)))

        target_career = student.find("cs:targetCareer", XML_NS)

        if target_career is not None:
            career_ref = target_career.get("ref")

            if career_ref in career_uri_map:
                g.add((student_uri, EX.targetsCareer, career_uri_map[career_ref]))

        for current_skill in student.findall("cs:currentSkills/cs:currentSkill", XML_NS):
            skill_ref = current_skill.get("ref")

            if skill_ref in skill_uri_map:
                g.add((student_uri, EX.hasSkill, skill_uri_map[skill_ref]))


def run_sparql_tests(g):
    """
    Run simple SPARQL queries to prove that the RDF graph works.
    """

    print("\n===== SPARQL Test 1: Careers and Required Skills =====")

    query_required_skills = """
    PREFIX ex: <http://example.org/career-skill#>

    SELECT ?careerName ?skillName
    WHERE {
        ?career a ex:Career .
        ?career ex:careerName ?careerName .
        ?career ex:requiresSkill ?skill .
        ?skill ex:skillName ?skillName .
    }
    ORDER BY ?careerName ?skillName
    """

    for row in g.query(query_required_skills):
        print(f"{row.careerName} requires {row.skillName}")

    print("\n===== SPARQL Test 2: Courses and Skills They Teach =====")

    query_courses = """
    PREFIX ex: <http://example.org/career-skill#>

    SELECT ?courseName ?skillName
    WHERE {
        ?course a ex:Course .
        ?course ex:courseName ?courseName .
        ?course ex:teachesSkill ?skill .
        ?skill ex:skillName ?skillName .
    }
    ORDER BY ?courseName ?skillName
    """

    for row in g.query(query_courses):
        print(f"{row.courseName} teaches {row.skillName}")


def main():
    """
    Main conversion process.
    """

    print("Reading XML file...")
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    print("Creating RDF graph...")
    g = create_graph()

    print("Adding RDFS schema...")
    add_rdfs_schema(g)

    print("Converting XML data into RDF triples...")
    source_uri_map = convert_sources(root, g)
    skill_uri_map = convert_skills(root, g)
    career_uri_map = convert_careers(root, g, skill_uri_map, source_uri_map)
    convert_courses(root, g, skill_uri_map)
    convert_students(root, g, skill_uri_map, career_uri_map)

    print(f"Saving RDF graph to {OUTPUT_TTL_FILE}...")
    g.serialize(destination=OUTPUT_TTL_FILE, format="turtle")

    print("RDF conversion completed successfully.")
    print(f"Total RDF triples generated: {len(g)}")

    run_sparql_tests(g)

# If this file is run directly, then execute main().
if __name__ == "__main__":
    main()