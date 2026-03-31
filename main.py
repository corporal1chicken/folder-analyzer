from pathlib import Path
import os
import sys

drive = input("Enter the drive to use. Must be 1 letter: ").upper()

if len(drive) != 1:
    print("Drive cannot be more than 1 letter")
    sys.exit()

if not os.path.exists(f"{drive}:/"):
    print("Drive does not exist")
    sys.exit()

folder_name = input(f"Enter a folder name in drive {drive}: ")
folder_path = Path(drive + ":/" + folder_name)

if folder_path.is_file():
    print(f"{folder_name} is a file, not a folder")
    sys.exit()

if not os.path.exists(drive + ":/" + folder_name):
    print(f"{folder_name} does not exist in drive {drive}")
    sys.exit()

file_names = []
file_extensions = []

for root, folders, files in os.walk(folder_path):
    for file in files:
        name, extension = os.path.splitext(file)

        file_names.append(name)
        file_extensions.append(extension)

options = ["1", "2", "3"]
option = input("(1) Print files names\n(2) Print file extentions\n(3) Print both\nEnter: ")

if option not in options:
    print(f"{option} is not a valid option")
    sys.exit()
elif option == "1":
    for f in file_names:
        print(f)
elif option == "2":
    for f in file_extensions:
        print(f)
elif option == "3":
    for name, ext in zip(file_names, file_extensions):
        print(f"Name: {name} | Ext: {ext}")