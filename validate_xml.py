from lxml import etree


def validate_xml(xml_file, xsd_file):
    """
    Validate an XML file against an XSD schema file.

    xml_file: The XML dataset file, e.g. career_skill_data.xml
    xsd_file: The XML Schema file, e.g. career_skill_schema.xsd
    """

    try:
        # Step 1: Read and parse the XML file
        xml_doc = etree.parse(xml_file)

        # Step 2: Read and parse the XSD schema file
        xsd_doc = etree.parse(xsd_file)

        # Step 3: Create an XMLSchema object from the XSD file
        schema = etree.XMLSchema(xsd_doc)

        # Step 4: Validate the XML file using the XSD schema
        if schema.validate(xml_doc):
            print("XML validation successful.")
            print(f"{xml_file} follows the structure defined in {xsd_file}.")
        else:
            print("XML validation failed.")

            # Print detailed error messages if validation fails
            for error in schema.error_log:
                print(f"Line {error.line}: {error.message}")

    except etree.XMLSyntaxError as e:
        # This catches basic XML syntax errors, such as missing closing tags
        print("XML syntax error:")
        print(e)

    except etree.XMLSchemaParseError as e:
        # This catches problems inside the XSD file itself
        print("XSD schema error:")
        print(e)

    except OSError as e:
        # This catches file-related errors, such as wrong filename or missing file
        print("File error:")
        print(e)


# Run validation using our Solution 2 XML and XSD files
validate_xml("career_skill_data.xml", "career_skill_schema.xsd")

# =============================================================================================================================
# Command for testing: py validate_xml.py
# - Expected output: XML validation successful. career_skill_data.xml follows the structure defined in career_skill_schema.xsd.
# - Test in the terminal to confirm that the XML file is valid against the XSD schema.
# =============================================================================================================================