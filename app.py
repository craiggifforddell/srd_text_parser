import sys

from internal_scripts.parse_xml import xml_parser
from internal_scripts.generate_excel_file import excel_generation

def run_parser_and_excel_generator():
    print("running parser")
    parsed_dict = xml_parser('BIOSSetup11_roblox.xml')
    # print(parsed_dict)
    print("success")
    print("starting generator")
    excel_generation(parsed_dict)

# def run_excel_generator():
#     print("running excel generator")


if __name__ == "__main__":
    # execute only if run as a script
    run_parser_and_excel_generator()
    # run_excel_generator()