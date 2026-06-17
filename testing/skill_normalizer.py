import xml.etree.ElementTree as ET
from difflib import get_close_matches


# ------------------------------------------------------------
# Purpose:
# This file normalises user-entered skills.
#
# Example:
# User types: pyhton, sql, ml
#
# System converts to:
# Python, SQL, Machine Learning
#
# This is important because SPARQL/RDF matching is strict.
# If the RDF graph uses "Python", but the user types "pyhton",
# the system may fail to match unless we clean the input first.
#
# Test Command: py testing/skill_normalizer.py 
# ------------------------------------------------------------


XML_FILE = "career_skill_data.xml"

# XML namespace used in career_skill_data.xml
NS = {"cs": "https://tsw6223.example.edu/career-skill"}


def get_text(parent, tag_name):
    """
    Safely get text from a child XML element.

    Example:
    get_text(skill, "skillName") returns "Python".
    """
    element = parent.find(f"cs:{tag_name}", NS)

    if element is not None and element.text is not None:
        return element.text.strip()

    return ""


def load_skills_from_xml():
    """
    Read skills and aliases from career_skill_data.xml.

    Return:
    1. skill_names:
       List of official skill names, e.g. ["Python", "SQL"]

    2. alias_map:
       Dictionary mapping aliases to official skill names.
       Example:
       {
           "py": "Python",
           "pyhton": "Python",
           "ml": "Machine Learning"
       }
    """

    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    skill_names = []
    alias_map = {}

    for skill in root.findall("cs:skills/cs:skill", NS):
        skill_name = get_text(skill, "skillName")

        # Store official skill name
        skill_names.append(skill_name)

        # Also map the lowercase official skill name to itself
        # Example: "python" -> "Python"
        alias_map[skill_name.lower()] = skill_name

        # Store all aliases from XML
        for alias in skill.findall("cs:aliases/cs:alias", NS):
            if alias.text:
                alias_text = alias.text.strip().lower()
                alias_map[alias_text] = skill_name

    return skill_names, alias_map


def clean_user_input(user_input):
    """
    Clean raw user input.

    Example:
    Input:  "  pyhton, SQL,   ml "
    Output: ["pyhton", "sql", "ml"]
    """

    # Split by comma
    raw_items = user_input.split(",")

    cleaned_items = []

    for item in raw_items:
        # Remove leading/trailing spaces and convert to lowercase
        cleaned = item.strip().lower()

        # Ignore empty values caused by extra commas
        if cleaned:
            cleaned_items.append(cleaned)

    return cleaned_items


def normalise_skills(user_input, skill_names, alias_map):
    """
    Convert user-entered skills into official skill names.

    This function uses:
    1. Exact alias matching
    2. Fuzzy matching for spelling mistakes
    3. User confirmation for fuzzy suggestions

    Return:
    confirmed_skills = list of official skill names accepted by user
    unknown_skills = list of inputs that could not be matched
    """

    cleaned_inputs = clean_user_input(user_input)

    confirmed_skills = []
    unknown_skills = []

    # Prepare lowercase official skill names for fuzzy matching
    official_skill_lookup = {name.lower(): name for name in skill_names}
    official_skill_lowercase = list(official_skill_lookup.keys())

    print("\n===== Input Validation =====")

    for item in cleaned_inputs:

        # ----------------------------------------------------
        # Step 1: Exact alias matching
        # Example:
        # "ml" -> "Machine Learning"
        # "py" -> "Python"
        # ----------------------------------------------------
        if item in alias_map:
            official_skill = alias_map[item]

            print(f'- "{item}" matched to "{official_skill}"')

            if official_skill not in confirmed_skills:
                confirmed_skills.append(official_skill)

        else:
            # ------------------------------------------------
            # Step 2: Fuzzy matching for typo handling
            # Example:
            # "pythn" may suggest "python"
            # ------------------------------------------------
            possible_matches = get_close_matches(
                item,
                official_skill_lowercase,
                n=1,
                cutoff=0.7
            )

            if possible_matches:
                suggested_lowercase = possible_matches[0]
                suggested_skill = official_skill_lookup[suggested_lowercase]

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
                # No exact match and no fuzzy match
                unknown_skills.append(item)
                print(f'- "{item}" could not be matched to any known skill.')

    return confirmed_skills, unknown_skills


def main():
    """
    Main testing function for skill normalisation.
    """

    skill_names, alias_map = load_skills_from_xml()

    print("===== Skill Input Normalisation Test =====")
    print("Enter your current skills separated by comma.")
    print("Example: pyhton, sql, ml")
    print()

    user_input = input("Enter your current skills: ")

    confirmed_skills, unknown_skills = normalise_skills(
        user_input,
        skill_names,
        alias_map
    )

    print("\n===== Confirmed Skills =====")

    if confirmed_skills:
        for skill in confirmed_skills:
            print(f"- {skill}")
    else:
        print("No confirmed skills.")

    print("\n===== Unknown Skills =====")

    if unknown_skills:
        for skill in unknown_skills:
            print(f"- {skill}")
    else:
        print("No unknown skills.")

    print("\nSkill normalisation completed.")


if __name__ == "__main__":
    main()