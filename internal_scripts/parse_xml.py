import xml.etree.ElementTree as ET
import json
import sys

def xml_parser(file_location):
    # Use Element Tree to parse xml document
    tree = ET.parse(file_location)
    # tree = ET.parse(file_name)
    root = tree.getroot()
    possible_values = root[0]
    current_values = root[1]

    possible_values_formsets = possible_values.find('FormSet').findall('Form')
    current_values_formsets = current_values.find('FormSet').findall('Form')
    possible_values_array = []
    current_values_array = []

    for form in possible_values_formsets:
        form_display_title = form.find('DisplayTitle').text
        config_items = form.findall('ConfigItem')
        config_array = []
        possible_values_object = {}
        possible_values_object['Title'] = form_display_title
        for config in config_items:
            config_object = {}
            config_item_name = config.find('Name').text
            config_object['Name'] = config_item_name
            config_item_ref_form_id = config.find('RefFormId').text
            config_object['RefFormId'] = config_item_ref_form_id
            config_item_display_name = config.find('DisplayName').text
            # print(f"display name is {config_item_display_name}")
            config_object['DisplayName'] = config_item_display_name
            config_item_bios_mapping = config.find('BiosMapping').text
            config_object['BiosMapping'] = config_item_bios_mapping
            config_item_display_index = config.find('DisplayIndex').text
            config_object['DisplayIndex'] = config_item_display_index
            config_object['Current Value'] = "NO VALUE"
            try:
                values = config.findall('ValueStruct')
                potential_value_array = []
                # print("values follow")
                # print(values)
                for item in values:
                    item.attrib['Value'] = item.find('DisplayValue').text
                    potential_value_array.append(item.attrib)
                    try:
                        if item.find('DefaultId').text == '0000':
                            print('in the if statment...')
                            config_object['Current Value'] = item.find('DisplayValue').text
                    except:
                        pass
            except:
                pass
            config_object['Potential Values'] = potential_value_array
            try:
                config_item_help = config.find('Help').text
                config_object['Help'] = config_item_help
            except:
                pass
            try:
                modifiers = config.findall('Modifier')
                modifier_array = []
                for modify in modifiers:
                    modify.attrib['Value'] = modify.text
                    modifier_array.append(modify.attrib)
            except:
                pass
            config_object['Modifiers'] = modifier_array
            try:
                dependencies = config.find('Dependencies')
                dependency_array = []
                for item in dependencies:
                    item.attrib['Tag'] = item.tag
                    item.attrib['Text'] = item.text
                    dependency_array.append(item.attrib)
            except:
                pass
            config_object['Dependencies'] = dependency_array
            config_array.append(config_object)

        possible_values_object['Config Items'] = config_array
        possible_values_array.append(possible_values_object)

    for form in current_values_formsets:
        form_display_title = form.find('DisplayTitle').text
        config_items = form.findall('ConfigItem')
        config_array = []
        current_values_object = {}
        current_values_object['Title'] = form_display_title
        for config in config_items:
            config_object = {}
            config_item_name = config.find('Name').text
            config_object['Name'] = config_item_name
            config_item_bios_mapping = config.find('BiosMapping').text
            config_object['BiosMapping'] = config_item_bios_mapping
            config_item_display_index = config.find('CommitIndex').text
            config_object['CommitIndex'] = config_item_display_index
            try:
                value_struct = config.find('ValueStruct')
                value_array = []
                for item in dependencies:
                    try:
                        item['Value'] = item.find('Value').text
                    except:
                        pass
                    try:
                        item['BiosMapping'] = item.find('BiosMapping').text
                    except:
                        pass
                    value_array.append(item)
            except:
                pass
            config_object['Dependencies'] = dependency_array
            config_object['ValueStruct'] = value_array
            config_array.append(config_object)

        current_values_object['Config Items'] = config_array
        current_values_array.append(current_values_object)

    f = open("generated_dictionary.txt", "a")
    f.write(json.dumps(possible_values_array, indent=1))
    f.close()
    return possible_values_array

if __name__ == "__main__":
    xml_parser(sys.path[0] + '/../BIOSSetup11_roblox.xml')