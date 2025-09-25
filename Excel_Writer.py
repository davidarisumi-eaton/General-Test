import GT_Excel_Interface
import os.path
from os import path


file_path = "Z:\\Arisumi\\SR2\\SR2 PXR20and25\\V1.3.14 (Batt Fix)\\Automation\\PXR20"

test_group = []
name_group = []
for root, dirs, files, in os.walk(file_path, topdown = True):
    for name in files:
        test_group.append(file_path + '/' + str(os.path.join(name)))
        name_group.append(name)

for name in name_group:
    print(name)


for check_file_name in test_group:

    config_file = GT_Excel_Interface.Test_File("Modify", check_file_name)

    config_file.write_cell(4, 2, 0, "Firmware Version")
    config_file.write_cell(5, 2, 0, "1.3.14")
    config_file.save_file()
    config_file.close()
