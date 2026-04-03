from pathlib import Path

EXPORT_DIR = Path.home() / "Downloads"

TYPES = {
    "image": {".png", ".jpg,", ".jpeg", ".bmp", ".webp", ".svg", ".tiff"},
    "video": {".mp4", ".avi", ".mkv", ".webm"},
    "audio": {".mp3", ".wav", ".ogg"},
    "text": {".txt", ".md"},
    "data": {".json", ".csv", ".xml", ".yml"},
    "document": {".pdf", ".doc", ".docx", ".ppt", ".pttx"},
    "code": {".py", "js", "ts", ".java", ".cs", ".html", ".css", ".gd"},
    "executable": {".exe"}
}

SORT_OPTIONS = [
    "Name (A-Z)", 
    "Name (Z-A)", 
    "Size (Large to Small)", 
    "Size (Small to Large)", 
    #"Date Modified (Newest to Oldest)",
    #"Date Modified (Oldest to Newst)"
]

FILTER_OPTIONS = [
    "Text",
    "Video",
    "Image",
    "Unknown",
    "Root Only",
]