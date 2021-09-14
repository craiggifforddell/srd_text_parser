import sys

def text_parser():
    file = open(sys.path[0] + "/../biosoptions.txt", "r")

    # Define our Variables
    nested_dict = {}
    sub_dict = {}
    sub_possible_value_dict = {}
    attribute = "N/A"
    FQDD = "N/A"
    current_value = "N/A"
    possible_value = "N/A"
    iter_num = 0

    # Loop through the lines of the text file.
    for line in file:
        # Identify/Create new attribute if line begins with 'Attribute'
        if "Attribute" in line:
            attribute = line.partition("[")[2].partition("]")[0].replace(" ", "")
            print(f"Attribute = " + attribute)
        # Push the FQDD into the sub directory
        elif "FQDDString" in line:
            FQDD = line.partition("=")[2].replace(" ", "")
            print(f"FQDD = " + FQDD)
            sub_dict['FQDD'] = FQDD
        # Push the current value into the sub directory
        elif "Current value" in line:
            current_value = line.partition("[")[2].partition("]")[0].replace(" ", "")
            sub_dict['current_value'] = current_value
        # Push the possible values into the sub directory
        elif "Possible value" in line:
            possible_value = line.partition("[")[2].partition("]")[0].replace(" ", "")
            print(f"Possible Value = " + possible_value)
            iter_num = iter_num + 1
            possible_value_iter = "possible_value_" + str(iter_num)
            sub_possible_value_dict[possible_value_iter] = possible_value
        elif attribute != "":
            sub_dict['possible_values'] = sub_possible_value_dict
            nested_dict[attribute] = sub_dict
            print("ELSE")
            attribute = ""
            FQDD = ""
            current_value = ""
            possible_value = ""
            iter_num = 0
            # reset the sub dictionaries
            sub_dict = {}
            sub_possible_value_dict = {}

    print("HERE IS THE END")
    print(nested_dict)

    file.close()
    return nested_dict

if __name__ == "__main__":
    text_parser()