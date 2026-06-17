import xml.etree.ElementTree as ET

# ------------------------------------------------------------
# Purpose:
# This file reads career_skill_data.xml and prints the data
# in a readable format.
#
# This step is important before RDF conversion because we need
# to confirm that Python can correctly read the XML structure.
#
# Test Command: py testing/parse_xml.py 
# ------------------------------------------------------------

# XML file name
XML_FILE = "career_skill_data.xml"

# Namespace used in career_skill_data.xml
# Because the XML uses xmlns="https://tsw6223.example.edu/career-skill",
# every XML tag is internally stored with this namespace.
NS = {"cs": "https://tsw6223.example.edu/career-skill"}


def get_text(parent, tag_name):
    """
    Helper function to safely get text from a child element.

    Example:
    get_text(skill, "skillName") will return "Python"

    If the tag is missing, it returns an empty string instead of crashing.
    """
    element = parent.find(f"cs:{tag_name}", NS)

    if element is not None and element.text is not None:
        return element.text.strip()

    return ""


def load_xml_root():
    """
    Load and parse the XML file.

    Return:
    root element of the XML document.
    """
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    return root


def extract_skills(root):
    """
    Extract all skills from the XML file.

    Return:
    A dictionary where:
    key   = skill ID, e.g. SK001
    value = skill details, e.g. Python, Technical, aliases
    """
    skills = {}

    for skill in root.findall("cs:skills/cs:skill", NS):
        skill_id = skill.get("id")
        skill_name = get_text(skill, "skillName")
        skill_category = get_text(skill, "skillCategory")

        aliases = []
        for alias in skill.findall("cs:aliases/cs:alias", NS):
            if alias.text:
                aliases.append(alias.text.strip())

        skills[skill_id] = {
            "name": skill_name,
            "category": skill_category,
            "aliases": aliases
        }

    return skills


def extract_careers(root, skills):
    """
    Extract all careers and their required skills.

    The required skills are stored as references, such as SK001.
    This function converts SK001 into the actual skill name, such as Python.
    """
    careers = {}

    for career in root.findall("cs:careers/cs:career", NS):
        career_id = career.get("id")
        source_ref = career.get("sourceRef")
        source_occupation_code = career.get("sourceOccupationCode")

        career_name = get_text(career, "careerName")
        source_occupation_title = get_text(career, "sourceOccupationTitle")
        career_level = get_text(career, "careerLevel")
        source_note = get_text(career, "sourceNote")

        required_skills = []

        for required_skill in career.findall("cs:requiredSkills/cs:requiredSkill", NS):
            skill_ref = required_skill.get("ref")
            priority = required_skill.get("priority")

            # Convert skill ID into readable skill name
            skill_name = skills.get(skill_ref, {}).get("name", "Unknown Skill")

            required_skills.append({
                "skill_id": skill_ref,
                "skill_name": skill_name,
                "priority": priority
            })

        careers[career_id] = {
            "name": career_name,
            "source_ref": source_ref,
            "source_occupation_code": source_occupation_code,
            "source_occupation_title": source_occupation_title,
            "level": career_level,
            "source_note": source_note,
            "required_skills": required_skills
        }

    return careers


def extract_courses(root, skills):
    """
    Extract all courses from the XML file.

    Each course can:
    - teach one or more skills
    - have zero or more prerequisite skills
    """
    courses = {}

    for course in root.findall("cs:courses/cs:course", NS):
        course_id = course.get("id")
        course_name = get_text(course, "courseName")

        teaches_skills = []
        for teaches_skill in course.findall("cs:teachesSkill", NS):
            skill_ref = teaches_skill.get("ref")
            skill_name = skills.get(skill_ref, {}).get("name", "Unknown Skill")

            teaches_skills.append({
                "skill_id": skill_ref,
                "skill_name": skill_name
            })

        prerequisite_skills = []
        for prerequisite_skill in course.findall("cs:prerequisiteSkill", NS):
            skill_ref = prerequisite_skill.get("ref")
            skill_name = skills.get(skill_ref, {}).get("name", "Unknown Skill")

            prerequisite_skills.append({
                "skill_id": skill_ref,
                "skill_name": skill_name
            })

        courses[course_id] = {
            "name": course_name,
            "teaches_skills": teaches_skills,
            "prerequisite_skills": prerequisite_skills
        }

    return courses


def extract_students(root, skills, careers):
    """
    Extract sample student profiles from the XML file.

    This is optional because later the terminal UI will allow the user
    to enter their own skills manually.
    """
    students = {}

    for student in root.findall("cs:students/cs:student", NS):
        student_id = student.get("id")
        student_name = get_text(student, "studentName")

        target_career_element = student.find("cs:targetCareer", NS)
        target_career_ref = target_career_element.get("ref") if target_career_element is not None else ""

        target_career_name = careers.get(target_career_ref, {}).get("name", "Unknown Career")

        current_skills = []
        for current_skill in student.findall("cs:currentSkills/cs:currentSkill", NS):
            skill_ref = current_skill.get("ref")
            skill_name = skills.get(skill_ref, {}).get("name", "Unknown Skill")

            current_skills.append({
                "skill_id": skill_ref,
                "skill_name": skill_name
            })

        students[student_id] = {
            "name": student_name,
            "target_career_id": target_career_ref,
            "target_career_name": target_career_name,
            "current_skills": current_skills
        }

    return students


def print_skills(skills):
    """
    Print all extracted skills.
    """
    print("\n===== Skills =====")

    for skill_id, skill in skills.items():
        print(f"{skill_id}: {skill['name']} ({skill['category']})")
        print(f"  Aliases: {', '.join(skill['aliases'])}")


def print_careers(careers):
    """
    Print all extracted careers and their required skills.
    """
    print("\n===== Careers =====")

    for career_id, career in careers.items():
        print(f"\n{career_id}: {career['name']}")
        print(f"  O*NET Title: {career['source_occupation_title']}")
        print(f"  O*NET Code: {career['source_occupation_code']}")
        print(f"  Level: {career['level']}")
        print("  Required Skills:")

        for required_skill in career["required_skills"]:
            print(
                f"    - {required_skill['skill_name']} "
                f"({required_skill['priority']})"
            )


def print_courses(courses):
    """
    Print all extracted courses and the skills they teach.
    """
    print("\n===== Courses =====")

    for course_id, course in courses.items():
        print(f"\n{course_id}: {course['name']}")

        teaches = [item["skill_name"] for item in course["teaches_skills"]]
        prerequisites = [item["skill_name"] for item in course["prerequisite_skills"]]

        print(f"  Teaches: {', '.join(teaches)}")

        if prerequisites:
            print(f"  Prerequisites: {', '.join(prerequisites)}")
        else:
            print("  Prerequisites: None")


def print_students(students):
    """
    Print sample student profiles.
    """
    print("\n===== Students =====")

    for student_id, student in students.items():
        print(f"\n{student_id}: {student['name']}")
        print(f"  Target Career: {student['target_career_name']}")

        current_skills = [item["skill_name"] for item in student["current_skills"]]
        print(f"  Current Skills: {', '.join(current_skills)}")


def main():
    """
    Main program flow for XML parsing.
    """
    print("Reading XML file...")

    root = load_xml_root()

    skills = extract_skills(root)
    careers = extract_careers(root, skills)
    courses = extract_courses(root, skills)
    students = extract_students(root, skills, careers)

    print_skills(skills)
    print_careers(careers)
    print_courses(courses)
    print_students(students)

    print("\nXML parsing completed successfully.")


if __name__ == "__main__":
    main()
