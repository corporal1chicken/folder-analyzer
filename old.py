from pathlib import Path
import os
import sys
import datetime
import math

types = {
    "image": [".png", ".jpg"],
    "video": [".mp4"],
    "text": [".txt", ".json", ".csv"]
}

def validate_drive(drive):
    if len(drive) != 1:
        print("Drive must be exactly 1 letter")
        return False

    if not os.path.exists(f"{drive}:/"):
        print("Drive does not exist")
        return False
    
    return True

def validate_folder(path):
    if not path.exists():
        print(f"{path} does not exist")
        return False

    if path.is_file():
        print(f"{path} is a file, not a folder")
        return False
    
    return True

def add_files(text_path):
    files = []
    windows_path = Path(text_path)

    for root, folders, file_list in os.walk(windows_path):
        for file in file_list:
            name, extension = os.path.splitext(file)

            full_path = os.path.join(root, file)
            extra_info = os.stat(full_path)

            size = extra_info.st_size
            last_mod = datetime.datetime.fromtimestamp(extra_info.st_mtime)
            
            file_type = "Unknown"
            for f_type, allowed_ext in types.items():
                if extension in allowed_ext:
                    file_type = f_type

            files.append(
                {
                    "full": file,
                    "name": name, 
                    "extension": extension,
                    "size": size,
                    "last_modified": last_mod,
                    "type": file_type
                }
            )

    return files

def format_size(actual_bytes, decimal = 2):
    if actual_bytes == 0:
        return "0 Bytes"
    
    power = 1024
    units = ["Bytes", "KB", "MB", "GB", "TB"]

    i = int(math.floor(math.log(actual_bytes, power)))
    format = f"{actual_bytes / (power ** i):.{decimal}f} {units[i]}"

    return format

def generate_report(files, folder_path):
    file_count = {}

    print("-----------------------------------")
    print(f"FOLDER PATH: {folder_path}")
    print("-----------------------------------")

    for f in files:
        print(f"Name: {f['name']} | Ext: {f['extension']}")
        print(f"Type: {f['type'].capitalize()}")
        print(f"Raw: {f['size']} Bytes | Size: {format_size(f['size'])}")
        print(f"Last Modified: {f['last_modified']}")
        print("-----------------------------------")

        if file_count.get(f['type']):
            file_count[f['type']] += 1
        else:
            file_count[f['type']] = 1

    print(f"There are {sum(file_count.values())} files")

    for t, c in file_count.items():
        print(f"{c} {t} files")

    print("-----------------------------------")


drive = input("Enter the drive to use. Must be 1 letter: ").upper()
drive_valid = validate_drive(drive)

if not drive_valid:
    sys.exit()

folder_name = input(f"Enter a folder name in drive {drive}: ")
folder_path = f"{drive}:/{folder_name}"

folder_valid = validate_folder(Path(folder_path))

if not folder_valid:
    sys.exit()
else:
    current_files = add_files(folder_path)

generate_report(current_files, folder_path)