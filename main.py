from pathlib import Path
import os
import sys

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

types = {
    "image": [".png", ".jpg"],
    "video": [".mp4"],
    "text": [".txt", ".json", ".csv"]
}

options = ["1", "2", "3", "4"]
option = input("(1) Print file names\n(2) Print file extensions\n(3) Print both\n(4) Get file count\nEnter: ")

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
elif option == "4":
    chosen_type = input("Pick a type to count (image, text, video): ").lower()

    if chosen_type not in types.keys():
        print(f"{chosen_type} is not a valid type")
        sys.exit()

    file_count = {}
    for f in current_files:
        extension = f["extension"]

        if extension in types[chosen_type]:
            if file_count.get(extension):
                file_count[extension] += 1
            else:
                file_count[extension] = 1

    print(f"There are {sum(file_count.values())} {chosen_type} files in {folder_path}")
    print("Breakdown:")
    for ext, count in file_count.items():
        print(f"Ext: {ext} | {count}")