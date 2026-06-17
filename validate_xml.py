from lxml import etree


def validate_xml(xml_file, xsd_file):
    try:
        xml_doc = etree.parse(xml_file)
        xsd_doc = etree.parse(xsd_file)

        schema = etree.XMLSchema(xsd_doc)

        if schema.validate(xml_doc):
            print("XML validation successful.")
            print(f"{xml_file} follows the structure defined in {xsd_file}.")
        else:
            print("XML validation failed.")
            for error in schema.error_log:
                print(f"Line {error.line}: {error.message}")

    except etree.XMLSyntaxError as e:
        print("XML syntax error:")
        print(e)

    except etree.XMLSchemaParseError as e:
        print("XSD schema error:")
        print(e)

    except OSError as e:
        print("File error:")
        print(e)


validate_xml("career_skill_data.xml", "career_skill_schema.xsd")