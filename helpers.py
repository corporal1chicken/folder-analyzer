from constants import TYPES
from dialogs import MessageDialog
from pathlib import Path

import math
import os
import datetime

def validate_folder(path):
    if not path.exists():
        return False, "Path Invalid: Path does not exist"

    if path.is_file():
        return False, "Path Invalid: Path is not a folder"
    
    if not any(path.iterdir()):
        return False, "Path Invalid: Folder is empty"
    
    return True, "Success"

def format_size(actual_bytes, decimal = 2):
    if actual_bytes == 0:
        return "0 Bytes"
    
    power = 1024
    units = ["Bytes", "KB", "MB", "GB", "TB"]

    i = int(math.floor(math.log(actual_bytes, power)))
    formatted = f"{actual_bytes / (power ** i):.{decimal}f} {units[i]}"

    return formatted

def detect_type(extension):
    extension = extension.lower()

    for f_type, allowed_ext in TYPES.items():
        if extension in allowed_ext:
            return f_type
        
    return "Unknown"

def add_files(path):
    files = []

    for root, folders, file_list in os.walk(path):
        for file in file_list:
            name, extension = os.path.splitext(file)

            full_path = os.path.join(root, file)
            extra_info = os.stat(full_path)

            size = extra_info.st_size
            last_mod = str(datetime.datetime.fromtimestamp(extra_info.st_mtime))

            files.append(
                {
                    "filename": file,
                    "path": full_path,
                    "name": name, 
                    "extension": extension,
                    "raw": size,
                    "size": format_size(size),
                    "last_modified": last_mod,
                    "type": detect_type(extension)
                }
            )

    return files

def sort_files(files, option):
    if option == "Name (A-Z)":
        return sorted(files, key=lambda x: x["name"].lower())
    elif option == "Name (Z-A)":
        return sorted(files, key=lambda x: x["name"].lower(), reverse=True)
    elif option == "Size (Large to Small)":
        return sorted(files, key=lambda x: x["raw"], reverse=True)
    elif option == "Size (Small to Large)":
        return sorted(files, key=lambda x: x["raw"])
    
def get_metadata(files):
    file_count = {}
    smallest_file = None
    largest_file = None
    total_size = 0

    for f in files:
        if file_count.get(f['type']):
            file_count[f['type']] += 1
        else:
            file_count[f['type']] = 1

        if smallest_file is None or f['raw'] < smallest_file['raw']:
            smallest_file = f
        
        if largest_file is None or f['raw'] > largest_file['raw']:
            largest_file = f
        
        total_size += f['raw']

    details = "\n".join(
        f"- {count} {file_type} file{'s' if count > 1 else ''}"
        for file_type, count in file_count.items()
    )

    # Final message
    message = (
        f"- Total Files: {len(files)}\n"
        f"{details}\n"
        f"- Total Size: {format_size(total_size)}\n"
        f"- Smallest File: {smallest_file['filename']} ({format_size(smallest_file['raw'])})\n"
        f"- Largest File: {largest_file['filename']} ({format_size(largest_file['raw'])})"
    )

    return message

def display_message(parent, text: str):
    message = MessageDialog(parent)
    message.message_label.setText(text)
    message.exec_()