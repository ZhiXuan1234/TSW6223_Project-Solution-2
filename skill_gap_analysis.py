import xml.etree.ElementTree as ET
from difflib import get_close_matches


# ------------------------------------------------------------
# Purpose:
# This file performs the main skill gap analysis for Solution 2.
#
# It combines:
# 1. XML parsing
# 2. User skill normalisation
# 3. Career requirement comparison
# 4. Missing skill detection
# 5. Readiness score calculation
# 6. Course recommendation
# 7. Alternative career suggestion
#
# Later, we will improve this by converting XML data into RDF/RDFS
# and retrieving the data using SPARQL.
# ------------------------------------------------------------


XML_FILE = "career_skill_data.xml"

# Namespace used in career_skill_data.xml
NS = {"cs": "https://tsw6223.example.edu/career-skill"}


def get_text(parent, tag_name):
    """
    Safely get text from a child XML element.

    If the element is missing, return an empty string instead of crashing.
    """
    element = parent.find(f"cs:{tag_name}", NS)

    if element is not None and element.text is not None:
        return element.text.strip()

    return ""


def load_xml_root():
    """
    Load career_skill_data.xml and return the root XML element.
    """
    tree = ET.parse(XML_FILE)
    return tree.getroot()


def extract_skills(root):
    """
    Extract all skills and aliases from XML.

    Return:
    skills:
        {
            "SK001": {
                "name": "Python",
                "category": "Technical",
                "aliases": [...]
            }
        }

    alias_map:
        {
            "py": "Python",
            "pyhton": "Python",
            "ml": "Machine Learning"
        }
    """

    skills = {}
    alias_map = {}

    for skill in root.findall("cs:skills/cs:skill", NS):
        skill_id = skill.get("id")
        skill_name = get_text(skill, "skillName")
        skill_category = get_text(skill, "skillCategory")

        aliases = []

        # Map official skill name to itself
        alias_map[skill_name.lower()] = skill_name

        for alias in skill.findall("cs:aliases/cs:alias", NS):
            if alias.text:
                alias_text = alias.text.strip().lower()
                aliases.append(alias_text)
                alias_map[alias_text] = skill_name

        skills[skill_id] = {
            "name": skill_name,
            "category": skill_category,
            "aliases": aliases
        }

    return skills, alias_map


def extract_careers(root, skills):
    """
    Extract career information and required skills from XML.

    Each required skill contains:
    - skill ID
    - skill name
    - priority level
    - skill category
    """

    careers = {}

    for career in root.findall("cs:careers/cs:career", NS):
        career_id = career.get("id")

        career_name = get_text(career, "careerName")
        source_occupation_title = get_text(career, "sourceOccupationTitle")
        career_level = get_text(career, "careerLevel")
        source_occupation_code = career.get("sourceOccupationCode")

        required_skills = []

        for required_skill in career.findall("cs:requiredSkills/cs:requiredSkill", NS):
            skill_id = required_skill.get("ref")
            priority = required_skill.get("priority")

            skill_info = skills.get(skill_id, {})

            required_skills.append({
                "skill_id": skill_id,
                "skill_name": skill_info.get("name", "Unknown Skill"),
                "category": skill_info.get("category", "Unknown Category"),
                "priority": priority
            })

        careers[career_id] = {
            "name": career_name,
            "source_occupation_title": source_occupation_title,
            "source_occupation_code": source_occupation_code,
            "level": career_level,
            "required_skills": required_skills
        }

    return careers


def extract_courses(root, skills):
    """
    Extract course information from XML.

    Each course can teach one or more skills and may have prerequisites.
    """

    courses = {}

    for course in root.findall("cs:courses/cs:course", NS):
        course_id = course.get("id")
        course_name = get_text(course, "courseName")

        teaches_skills = []

        for teaches_skill in course.findall("cs:teachesSkill", NS):
            skill_id = teaches_skill.get("ref")
            skill_name = skills.get(skill_id, {}).get("name", "Unknown Skill")
            teaches_skills.append(skill_name)

        prerequisite_skills = []

        for prerequisite_skill in course.findall("cs:prerequisiteSkill", NS):
            skill_id = prerequisite_skill.get("ref")
            skill_name = skills.get(skill_id, {}).get("name", "Unknown Skill")
            prerequisite_skills.append(skill_name)

        courses[course_id] = {
            "name": course_name,
            "teaches_skills": teaches_skills,
            "prerequisite_skills": prerequisite_skills
        }

    return courses


def clean_user_input(user_input):
    """
    Clean comma-separated user input.

    Example:
    Input:  " pyhton, SQL, ml "
    Output: ["pyhton", "sql", "ml"]
    """

    cleaned_items = []

    for item in user_input.split(","):
        cleaned = item.strip().lower()

        if cleaned:
            cleaned_items.append(cleaned)

    return cleaned_items


def normalise_skills(user_input, skills, alias_map):
    """
    Convert user input into official skill names.

    This function supports:
    1. Alias matching
    2. Typo correction using fuzzy matching
    3. User confirmation for suggested corrections
    """

    cleaned_inputs = clean_user_input(user_input)

    confirmed_skills = []
    unknown_skills = []

    official_skill_names = [skill["name"] for skill in skills.values()]
    official_skill_lookup = {name.lower(): name for name in official_skill_names}
    official_skill_lowercase = list(official_skill_lookup.keys())

    print("\n===== Input Validation =====")

    for item in cleaned_inputs:

        # First, try exact alias matching
        if item in alias_map:
            official_skill = alias_map[item]
            print(f'- "{item}" matched to "{official_skill}"')

            if official_skill not in confirmed_skills:
                confirmed_skills.append(official_skill)

        else:
            # If no alias match, try fuzzy matching for spelling mistakes
            possible_matches = get_close_matches(
                item,
                official_skill_lowercase,
                n=1,
                cutoff=0.7
            )

            if possible_matches:
                suggested_skill = official_skill_lookup[possible_matches[0]]

                print(f'- "{item}" was not found. Did you mean "{suggested_skill}"?')
                user_confirm = input("  Enter Y to accept, or N to reject: ").strip().lower()

                if user_confirm == "y":
                    if suggested_skill not in confirmed_skills:
                        confirmed_skills.append(suggested_skill)

                    print(f'  Accepted: "{item}" -> "{suggested_skill}"')
                else:
                    unknown_skills.append(item)
                    print(f'  Rejected: "{item}" was marked as unknown.')

            else:
                unknown_skills.append(item)
                print(f'- "{item}" could not be matched to any known skill.')

    return confirmed_skills, unknown_skills


def display_available_careers(careers):
    """
    Display career options for user selection.
    """

    print("\n===== Available Careers =====")

    career_ids = list(careers.keys())

    for index, career_id in enumerate(career_ids, start=1):
        career = careers[career_id]
        print(f"{index}. {career['name']}")

    return career_ids


def select_target_career(careers):
    """
    Let the user select a target career by number.

    Return:
    selected career ID, e.g. C004
    """

    career_ids = display_available_careers(careers)

    while True:
        try:
            choice = int(input("\nSelect your target career number: "))

            if 1 <= choice <= len(career_ids):
                return career_ids[choice - 1]

            print("Invalid choice. Please select a valid career number.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def analyse_skill_gap(target_career, confirmed_skills):
    """
    Compare user's confirmed skills with target career required skills.

    Return:
    matched_skills, missing_skills, readiness_score
    """

    required_skills = target_career["required_skills"]

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:
        skill_name = required_skill["skill_name"]

        if skill_name in confirmed_skills:
            matched_skills.append(required_skill)
        else:
            missing_skills.append(required_skill)

    total_required = len(required_skills)
    total_matched = len(matched_skills)

    if total_required > 0:
        readiness_score = round((total_matched / total_required) * 100)
    else:
        readiness_score = 0

    return matched_skills, missing_skills, readiness_score


def group_missing_skills_by_priority(missing_skills):
    """
    Group missing skills by High, Medium, and Low priority.
    """

    grouped = {
        "High": [],
        "Medium": [],
        "Low": []
    }

    for skill in missing_skills:
        priority = skill["priority"]
        grouped[priority].append(skill)

    return grouped


def recommend_courses(missing_skills, courses):
    """
    Recommend courses based on missing skills.

    If a course teaches any missing skill, it will be recommended.
    """

    missing_skill_names = [skill["skill_name"] for skill in missing_skills]

    recommended_courses = []

    for course_id, course in courses.items():
        matched_missing_skills = []

        for taught_skill in course["teaches_skills"]:
            if taught_skill in missing_skill_names:
                matched_missing_skills.append(taught_skill)

        if matched_missing_skills:
            recommended_courses.append({
                "course_id": course_id,
                "course_name": course["name"],
                "teaches_missing_skills": matched_missing_skills,
                "prerequisite_skills": course["prerequisite_skills"]
            })

    return recommended_courses


def suggest_alternative_careers(careers, selected_career_id, confirmed_skills):
    """
    Suggest alternative careers based on the user's existing skills.

    The selected target career is excluded from the alternative list.
    """

    alternatives = []

    for career_id, career in careers.items():

        # Do not compare the selected career with itself
        if career_id == selected_career_id:
            continue

        required_skills = career["required_skills"]
        matched_count = 0

        for required_skill in required_skills:
            if required_skill["skill_name"] in confirmed_skills:
                matched_count += 1

        total_required = len(required_skills)

        if total_required > 0:
            match_score = round((matched_count / total_required) * 100)
        else:
            match_score = 0

        alternatives.append({
            "career_name": career["name"],
            "match_score": match_score
        })

    # Sort careers by highest match score first
    alternatives.sort(key=lambda item: item["match_score"], reverse=True)

    return alternatives


def print_analysis_result(
    target_career,
    confirmed_skills,
    unknown_skills,
    matched_skills,
    missing_skills,
    readiness_score,
    recommended_courses,
    alternative_careers
):
    """
    Print final skill gap analysis result in terminal.
    """

    print("\n\n===== Semantic Career Path / Skill Gap Analyzer =====")

    print(f"\nTarget Career: {target_career['name']}")
    print(f"O*NET Source Title: {target_career['source_occupation_title']}")
    print(f"O*NET Code: {target_career['source_occupation_code']}")
    print(f"Career Level: {target_career['level']}")

    print("\nConfirmed Current Skills:")
    if confirmed_skills:
        for skill in confirmed_skills:
            print(f"- {skill}")
    else:
        print("- None")

    if unknown_skills:
        print("\nUnknown / Unmatched Inputs:")
        for skill in unknown_skills:
            print(f"- {skill}")

    print("\nRequired Skills:")
    for required_skill in target_career["required_skills"]:
        print(
            f"- {required_skill['skill_name']} "
            f"({required_skill['priority']}, {required_skill['category']})"
        )

    print("\nMatched Skills:")
    if matched_skills:
        for skill in matched_skills:
            print(f"- {skill['skill_name']}")
    else:
        print("- None")

    print("\nMissing Skills by Priority:")
    grouped_missing_skills = group_missing_skills_by_priority(missing_skills)

    has_missing = False

    for priority in ["High", "Medium", "Low"]:
        if grouped_missing_skills[priority]:
            has_missing = True
            print(f"\n[{priority.upper()}]")
            for skill in grouped_missing_skills[priority]:
                print(f"- {skill['skill_name']} ({skill['category']})")

    if not has_missing:
        print("- No missing skills. You meet all listed requirements.")

    print(f"\nCareer Readiness Score: {readiness_score}%")

    print("\nRecommended Learning Path:")
    if recommended_courses:
        for index, course in enumerate(recommended_courses, start=1):
            taught_skills = ", ".join(course["teaches_missing_skills"])

            print(f"{index}. {course['course_name']}")
            print(f"   Reason: This course teaches missing skill(s): {taught_skills}.")

            if course["prerequisite_skills"]:
                prerequisites = ", ".join(course["prerequisite_skills"])
                print(f"   Prerequisite skill(s): {prerequisites}.")
            else:
                print("   Prerequisite skill(s): None.")
    else:
        print("- No course recommendation needed.")

    print("\nAlternative Career Suggestions:")
    if alternative_careers:
        for index, career in enumerate(alternative_careers, start=1):
            print(f"{index}. {career['career_name']} - {career['match_score']}% match")
    else:
        print("- No alternative careers available.")


def main():
    """
    Main program flow.
    """

    root = load_xml_root()

    skills, alias_map = extract_skills(root)
    careers = extract_careers(root, skills)
    courses = extract_courses(root, skills)

    selected_career_id = select_target_career(careers)
    target_career = careers[selected_career_id]

    print("\nEnter your current skills separated by comma.")
    print("Example: pyhton, sql, ml")
    user_input = input("Your skills: ")

    confirmed_skills, unknown_skills = normalise_skills(
        user_input,
        skills,
        alias_map
    )

    matched_skills, missing_skills, readiness_score = analyse_skill_gap(
        target_career,
        confirmed_skills
    )

    recommended_courses = recommend_courses(missing_skills, courses)

    alternative_careers = suggest_alternative_careers(
        careers,
        selected_career_id,
        confirmed_skills
    )

    print_analysis_result(
        target_career,
        confirmed_skills,
        unknown_skills,
        matched_skills,
        missing_skills,
        readiness_score,
        recommended_courses,
        alternative_careers
    )


if __name__ == "__main__":
    main()