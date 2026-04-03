from constants import EXPORT_DIR
from dialogs import MessageDialog

import json
import csv

def json_ready(files):
    export_ready = []

    for f in files:
        export_ready.append({
            "filename": f["filename"],
            "path": f["path"],
            "name": f["name"],
            "extension": f["extension"],
            "raw": f["raw"],
            "size": f["size"],
            "type": f["type"].capitalize()
        })

    return export_ready

def txt_ready(files):
    export_ready = []

    for f in files:
        entry = (
            f"File: {f['filename']}\n"
            f"Path: {f['path']}\n"
            f"Name: {f['name']} | Ext: {f['extension']}\n"
            f"Size: {f['size']} ({f['raw']} bytes)\n"
            f"Type: {f['type'].capitalize()}\n"
            "-----------------------------------\n"
        )
        export_ready.append(entry)

    return export_ready

def csv_ready(files):
    rows = []

    rows.append([
        "Filename", "Path", "Name", "Extension",
        "Raw", "Size", "Type"
    ])

    for f in files:
        rows.append([
            f["filename"],
            f["path"],
            f["name"],
            f["extension"],
            f["raw"],
            f["size"],
            f["type"].capitalize()
        ])

    return rows

def format_writers(key, content, file_path):
    if key == "json":
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=4)

            return "Exported data to a .json file, find in Downloads"
        except Exception as error:
            return "An error occured exporting data"
    elif key == "txt":
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("".join(content))
            
            return "Exported data to a .txt file, find in Downloads"
        except Exception as error:
            return "An error occured exporting data"
    elif key == "csv":
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(content)

            return "Exported data to a .csv file, find in Downloads"
        except Exception as error:
            return "An error occured exporting data"