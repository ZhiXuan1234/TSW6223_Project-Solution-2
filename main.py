from lxml import etree
import subprocess
import sys


# ------------------------------------------------------------
# TSW6223 Solution 2 Main Application
#
# Purpose:
# This file acts as the main launcher for the Career Path /
# Skill Gap Analysis system.
#
# It performs the complete flow:
# 1. Validate XML using XSD
# 2. Convert XML data into RDF/RDFS Turtle format
# 3. Run the terminal-based skill gap analysis application
#
# This allows the project demo to be executed using:
# py main.py
# ------------------------------------------------------------


XML_FILE = "career_skill_data.xml"
XSD_FILE = "career_skill_schema.xsd"


def validate_xml(xml_file, xsd_file):
    """
    Validate the XML dataset against the XSD schema.

    This ensures that the XML file follows the required structure
    before it is converted into RDF or used for skill gap analysis.
    """

    print("\n===== Step 1: XML Validation =====")

    try:
        # Read the XML file
        xml_doc = etree.parse(xml_file)

        # Read the XSD schema file
        xsd_doc = etree.parse(xsd_file)

        # Create schema object from XSD
        schema = etree.XMLSchema(xsd_doc)

        # Validate XML against XSD
        if schema.validate(xml_doc):
            print("XML validation successful.")
            print(f"{xml_file} follows the structure defined in {xsd_file}.")
            return True

        print("XML validation failed.")

        # Print detailed validation errors
        for error in schema.error_log:
            print(f"Line {error.line}: {error.message}")

        return False

    except Exception as e:
        print("An error occurred during XML validation:")
        print(e)
        return False


def run_python_file(file_name):
    """
    Run another Python file from this main program.

    Example:
    run_python_file("xml_to_rdf.py")

    This keeps main.py simple while still allowing us to reuse
    existing modules that are already working.
    """

    try:
        result = subprocess.run(
            [sys.executable, file_name],
            check=True
        )

        return result.returncode == 0

    except subprocess.CalledProcessError:
        print(f"Error: {file_name} did not run successfully.")
        return False

    except FileNotFoundError:
        print(f"Error: {file_name} was not found.")
        return False


def main():
    """
    Main flow of the complete Solution 2 application.
    """

    print("==============================================")
    print(" TSW6223 Solution 2")
    print(" Semantic Career Path / Skill Gap Analyzer")
    print("==============================================")

    # Step 1: Validate XML before processing
    is_valid = validate_xml(XML_FILE, XSD_FILE)

    if not is_valid:
        print("\nProgram stopped because XML validation failed.")
        return

    # Step 2: Convert XML into RDF/RDFS Turtle file
    print("\n===== Step 2: XML to RDF/RDFS Conversion =====")
    print("Generating career_skill_graph.ttl...")

    rdf_success = run_python_file("xml_to_rdf.py")

    if not rdf_success:
        print("\nProgram stopped because RDF conversion failed.")
        return

    # Step 3: Launch final skill gap analyzer
    print("\n===== Step 3: Launch Skill Gap Analyzer =====")

    analysis_success = run_python_file("skill_gap_analysis.py")

    if not analysis_success:
        print("\nSkill gap analysis did not complete successfully.")
        return

    print("\nProgram completed successfully.")


if __name__ == "__main__":
    main()