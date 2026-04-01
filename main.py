import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QScrollArea, QTextEdit, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from pathlib import Path
import os
import datetime
import math

TYPES = {
    "image": [".png", ".jpg"],
    "video": [".mp4"],
    "text": [".txt", ".json", ".csv"]
}

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
                    "full": file,
                    "name": name, 
                    "extension": extension,
                    "raw": size,
                    "size": format_size(size),
                    "last_modified": last_mod,
                    "type": detect_type(extension)
                }
            )

    return files

class FileItem(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, filename, metadata_text):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)

        self.setStyleSheet("""
            QPushButton { 
                text-align: left; 
                border: none; 
                font-weight: bold; 
                padding: 8px;
                background: transparent;
                font-size: 14px;
            }
            QLabel { 
                color: #666; 
                padding: 5px 15px 10px 15px; 
                font-size: 13px;
                background-color: #FAFAFA;
            }
        """)

        # File Button
        self.btn = QPushButton(f"📄 {filename}")
        self.btn.clicked.connect(lambda: self.clicked.emit(self))
        self.layout.addWidget(self.btn)

        # Expanding info
        self.info_label = QLabel(metadata_text)
        self.info_label.setVisible(False) 
        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)

    def toggle(self, expand):
        self.info_label.setVisible(expand)

class FolderAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.file_widgets = []
        self.current_files = None
        self.initUI()

    def initUI(self):
        #self.setFont(QFont('Segoe UI', 15))
        
        # Window
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel("Folder Analyzer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        main_layout.addWidget(title_label)

        # Select Folder Button
        folder_section = QHBoxLayout()
        self.folder_btn = QPushButton("📂") 
        self.folder_btn.setFixedSize(60, 60)
        self.folder_btn.setStyleSheet("font-size: 24px;")
        self.folder_btn.clicked.connect(self.select_folder) # Logic Hook
        
        # Folder Label
        self.folder_label = QLabel("Select a folder")
        self.folder_label.setStyleSheet("font-size: 20px; font-weight: 500;")
        
        folder_section.addWidget(self.folder_btn)
        folder_section.addWidget(self.folder_label)
        folder_section.addStretch()
        main_layout.addLayout(folder_section)

        # Main Content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        box_style = "QFrame { background-color: white; border: 1px solid #C0C0C0; border-radius: 2px; }"

        # Metadata
        metadata_col = QVBoxLayout()
        metadata_col.addWidget(QLabel("Metadata:"))
        
        self.metadata_container = QFrame()
        self.metadata_container.setStyleSheet(box_style)
        meta_inner = QVBoxLayout(self.metadata_container)
        
        self.metadata_display = QTextEdit("No Folder Selected")
        self.metadata_display.setReadOnly(True)
        self.metadata_display.setStyleSheet("border: none; font-size: 14px;")
        
        meta_inner.addWidget(self.metadata_display)
        
        metadata_col.addWidget(self.metadata_container)

        # Files
        files_col = QVBoxLayout()
        files_col.addWidget(QLabel("Files:"))
        
        self.files_container = QFrame()
        self.files_container.setStyleSheet(box_style)
        files_inner = QVBoxLayout(self.files_container)
        files_inner.setContentsMargins(0, 0, 0, 0)
        
        # Scrolling area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll.setWidget(self.scroll_content)
        files_inner.addWidget(self.scroll)

        # Export Button
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(10, 10, 10, 10)
        btn_layout.addStretch()

        self.export_btn = QPushButton("E")
        self.export_btn.setFixedSize(35, 35)

        self.filters_btn = QPushButton("F")
        self.filters_btn.setFixedSize(35, 35)

        self.sort_btn = QPushButton("S")
        self.sort_btn.setFixedSize(35, 35)

        self.export_btn.clicked.connect(self.export_data)
        self.filters_btn.clicked.connect(self.filter_data)
        self.sort_btn.clicked.connect(self.sort_data)

        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.filters_btn)
        btn_layout.addWidget(self.sort_btn)
        files_inner.addLayout(btn_layout)
        
        files_col.addWidget(self.files_container)

        # Layout
        content_layout.addLayout(metadata_col)
        content_layout.addLayout(files_col)
        main_layout.addLayout(content_layout)

        # Test Data
        #self.add_file_entry("document.txt", "Type: Text\nSize: 12KB\nLines: 150")
        #self.add_file_entry("video.mp4", "Codec: H.264\nSize: 850MB\nLength: 12:45")

        self.setLayout(main_layout)
        self.resize(750, 550)
        self.show()

    def add_file_entry(self, name, info):
        item = FileItem(name, info)
        item.clicked.connect(self.handle_accordion)
        self.scroll_layout.addWidget(item)
        self.file_widgets.append(item)

    def handle_accordion(self, clicked_item):
        is_currently_visible = clicked_item.info_label.isVisible()

        for item in self.file_widgets:
            item.toggle(False)
        
        if not is_currently_visible:
            clicked_item.toggle(True)

    def clear_file_entries(self):
        while self.file_widgets:
            item = self.file_widgets.pop()

            self.scroll_layout.removeWidget(item)
            
            item.setParent(None)
            item.deleteLater()
            
        print("File entries cleared.")

    def select_folder(self):
        print("Selecting folder...")
        folder_string = QFileDialog.getExistingDirectory(self, "Select a Folder", str(Path.home()))
        folder_path = Path(folder_string)
        #self.folder_label.setText(folder_string)

        if not folder_string:
            self.folder_label.setText("No Folder Selected")
            return

        success, message = validate_folder(folder_path)
        file_count = {}

        if not success:
            self.folder_label.setText(message)
            return
        else:
            self.clear_file_entries()
            self.folder_label.setText(folder_string)

            self.current_files = add_files(folder_path)

            for f in self.current_files:
                self.add_file_entry(f['full'], f"Type: {f['type'].capitalize()}\nRaw: {f['raw']} | Size: {f['size']}\nLast Modified: {f['last_modified']}")

                if file_count.get(f['type']):
                    file_count[f['type']] += 1
                else:
                    file_count[f['type']] = 1
            
            details = "\n-".join(f"{c} {t} files" for t, c in file_count.items())

            self.metadata_display.setText(
                f"-Total Files: {sum(file_count.values())}\n-{details}"
            )
    
    def filter_data(self):
        print("Filtering data")

    def sort_data(self):
        print("Sorting data")

    def export_data(self):
        print("Exporting data")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderAnalyzer()
    sys.exit(app.exec_())