from datetime import date, time
import xlsxwriter
from numpy import *
import array

def excel_generation(parsed_dict):
    boot_mode = "Uefi"
    print(parsed_dict)
    # Initialize Workbook
    workbook = xlsxwriter.Workbook("./excel_output/output_roblox.xlsx")

    # Create BIOS Worksheet
    worksheet_bios = workbook.add_worksheet("BIOS")

    full_dict_array = parsed_dict

    # full_dict_array = parsed_dict
    # print("full dict array is...")
    # print(full_dict_array)

    # Increase the cell size of the merged cells to highlight the formatting.
    worksheet_bios.set_column('B:D', 12)

    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#0078d4'})

    # Add a format for the header cells.
    header_format = workbook.add_format({
        'border': 1,
        'bg_color': '#C6EFCE',
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })

    header_format_2 = workbook.add_format({
        'border': 1,
        'bg_color': '#0f94fa',
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })

    worksheet_bios.merge_range('A5:D6', 'BIOS Settings', merge_format)

    # Set up layout of the worksheet.
    worksheet_bios.set_column('A:A', 30)
    worksheet_bios.set_column('B:B', 30)
    worksheet_bios.set_column('C:C', 30)
    worksheet_bios.set_column('D:D', 30)
    worksheet_bios.set_row(0, 36)

    # Write the header cells and some data that will be used in the examples.
    heading1 = 'Setting'
    heading2 = 'Option'
    heading3 = 'Customer Selection'

    worksheet_bios.write('B3', heading1, header_format)
    worksheet_bios.write('C3', heading2, header_format)
    worksheet_bios.write('D3', heading3, header_format_2)

    worksheet_bios.freeze_panes(3, 0)

    row = 7
    # for title_group in full_dict_array:
    #     print(title_group)
    for bios_section in full_dict_array:
        bios_section_title = bios_section["Title"]
        bios_section_config_items = bios_section["Config Items"]

        if len(bios_section_config_items) == 0:
            continue

        fail_count = 0

        for i, config_item in enumerate(bios_section_config_items):

            x = i + 1 - fail_count
            try:
                display_name = config_item["DisplayName"]
                current_value = config_item["Current Value"]
                potential_values_raw = config_item["Potential Values"]
                dependencies = config_item["Dependencies"]

                if current_value == "NO VALUE":
                    continue

                potential_values_clean = []
                if x == 1:
                    row = row + 1
                header_row = row - x

                if len(dependencies) != 0:
                    isSuppressed = False
                    for j, dependency in enumerate(dependencies):
                        dependency_tag = dependency["Tag"]
                        dependency_text = dependency["Text"]
                        if dependency_tag == "SuppressIf" and dependency_text == boot_mode:
                            isSuppressed = True

                    if isSuppressed:
                        continue

                for potential_value in potential_values_raw:
                    potential_values_clean.append(potential_value["Value"])

                worksheet_bios.write(f'B{row}', display_name)
                # print(f"Display Name is {display_name}")
                worksheet_bios.write(f'C{row}', current_value)
                # print(f"Current Value is {current_value}")
                worksheet_bios.data_validation(f'D{row}', {'validate': 'list',
                                                  'source': potential_values_clean})

                if x == 1:
                    worksheet_bios.merge_range(f'B{header_row}:D{header_row}', bios_section_title, merge_format)

                row = row + 1

            except:
                fail_count = fail_count + 1
                continue
        # row = row + 2

    workbook.close()

if __name__ == "__main__":
    full_dict_array = [
        {
            "Title": "System BIOS Settings",
            "Config Items": [
                {
                    "Name": "SysInformationRef",
                    "BiosMapping": "2796",
                    "CommitIndex": "0",
                    "Dependencies": [],
                    "ValueStruct": []
                },
                {
                    "Name": "MemSettingsRef",
                    "BiosMapping": "2809",
                    "CommitIndex": "0",
                    "Dependencies": [],
                    "ValueStruct": []
                }
            ]
        }
    ]

    excel_generation(full_dict_array)