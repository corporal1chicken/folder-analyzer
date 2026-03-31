from pathlib import Path
import os
import sys

current_files = []

def validate_drive(drive):
    if len(drive) != 1:
        print("Drive must be exactly 1 letter")
        return False

    if not os.path.exists(f"{drive}:/"):
        print("Drive does not exist")
        return False
    
    return True

def validate_folder(path):
    if path.is_file():
        print(f"{path} is a file, not a folder")
        return False

    if not path.exists():
        print(f"{path} does not exist")
        return False
    
    return True

def add_files(path):
    files = []

    for root, folders, file_list in os.walk(path):
        for file in file_list:
            name, extension = os.path.splitext(file)

            files.append({"name": name, "extension": extension})

    return files

drive = input("Enter the drive to use. Must be 1 letter: ").upper()
drive_valid = validate_drive(drive)

if not drive_valid:
    sys.exit()

folder_name = input(f"Enter a folder name in drive {drive}: ")
folder_path = Path(f"{drive}:/{folder_name}")

folder_valid = validate_folder(folder_path)

if not folder_valid:
    sys.exit()
else:
    current_files = add_files(folder_path)

options = ["1", "2", "3"]
option = input("(1) Print file names\n(2) Print file extensions\n(3) Print both\nEnter: ")

if option not in options:
    print(f"{option} is not a valid option")
    sys.exit()
elif option == "1":
    for f in current_files:
        print(f["name"])
elif option == "2":
    for f in current_files:
        print(f["extension"])
elif option == "3":
    for f in current_files:
        print(f"Name: {f["name"]} | Ext: {f["extension"]}")