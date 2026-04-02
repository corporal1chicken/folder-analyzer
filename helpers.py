from constants import TYPES
from dialogs import MessageDialog
import math
import os
import datetime

def validate_folder(path):
    if not path.exists():
        return False, "Path does not exist"

    if path.is_file():
        return False, "Path is a file, not a folder"
    
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
            last_mod = datetime.datetime.fromtimestamp(extra_info.st_mtime)

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

def display_message(parent, text: str):
    message = MessageDialog(parent)
    message.message_label.setText(text)
    message.exec_()