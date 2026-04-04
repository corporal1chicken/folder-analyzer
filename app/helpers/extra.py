from constants import SAVE_PATH
import json

def save_old_files(path, metadata, files):
    old_data = {
        "path": path,
        "metadata": metadata,
        "files": files,
    }

    try:
        with open("last_save.json", "w") as file:
            json.dump(old_data, file)
    except Exception as error:
        pass

def load_old_files(current_path):
    last_save = {}

    try:
        with open(SAVE_PATH, 'r') as f:
            last_save = json.load(f)
        
    except FileNotFoundError:
        return False, "Save file was not found"
    except json.JSONDecodeError:
        return False, "No data available"
        
    if last_save['path'] == current_path:
        return False, "Last save is the same as the current"
    
    return True, last_save