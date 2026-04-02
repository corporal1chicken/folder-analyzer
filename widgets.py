from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QScrollArea, QTextEdit, QFileDialog, QDialog, QLineEdit, QAction)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from pathlib import Path
from helpers import validate_folder, add_files, display_message, sort_files
from dialogs import SortDialog, ExportDialog

import json

class FolderAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.current_files = []
        self.display_files = []
        self.file_widgets = []
        self.last_sort_choice = "Name (A-Z)"
        self.initUI()

    def initUI(self):        
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
        self.folder_btn = QPushButton()
        self.folder_btn.setIcon(QIcon("icons/folder.png")) 
        self.folder_btn.setFixedSize(60, 60)
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

        box_style = "QFrame {background-color: white; border: 1px solid #C0C0C0; border-radius: 2px;}"

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

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("No Folder Selected")
        search_icon = QIcon("icons/sort.png")
        search_action = QAction(search_icon, "Search", self.search_bar)
        self.search_bar.addAction(search_action)
        self.search_bar.setEnabled(False)
        self.search_bar.setStyleSheet("padding: 8px; border-bottom: 1px;")
        self.search_bar.textChanged.connect(self.search_files)
        files_inner.addWidget(self.search_bar)
        
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

        # Export, Filters, Sort Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(10, 10, 10, 10)
        btn_layout.addStretch()

        self.export_btn = QPushButton()
        self.export_btn.setIcon(QIcon("icons/export.png"))
        self.export_btn.setFixedSize(35, 35)
        self.export_btn.setEnabled(False)

        self.filters_btn = QPushButton()
        self.filters_btn.setIcon(QIcon("icons/filter.png"))
        self.filters_btn.setFixedSize(35, 35)
        self.filters_btn.setEnabled(False)

        self.sort_btn = QPushButton()
        self.sort_btn.setIcon(QIcon("icons/sort.png"))
        self.sort_btn.setFixedSize(35, 35)
        self.sort_btn.setEnabled(False)

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

        self.setLayout(main_layout)
        self.resize(750, 550)
        self.show()

    def add_entry(self, name, info):
        item = FileItem(name, info)
        item.clicked.connect(self.file_clicked)
        self.scroll_layout.addWidget(item)
        self.file_widgets.append(item)

    def file_clicked(self, clicked_item):
        is_currently_visible = clicked_item.info_label.isVisible()

        for item in self.file_widgets:
            item.toggle(False)
        
        if not is_currently_visible:
            clicked_item.toggle(True)

    def clear_entries(self):
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

        if not folder_string:
            self.folder_label.setText("No Folder Selected")

            display_message(self, "No Folder Selected")
            return

        success, error = validate_folder(folder_path)
        file_count = {}

        if not success: 
            self.folder_label.setText("No Folder Selected")

            display_message(self, error)

            return
        else:
            self.clear_entries()
            self.folder_label.setText(folder_string)
            self.export_btn.setEnabled(True)
            self.sort_btn.setEnabled(True)
            self.filters_btn.setEnabled(True)
            self.search_bar.setPlaceholderText("Search Files")
            self.search_bar.setEnabled(True)

            self.current_files = add_files(folder_path)
            self.display_files = self.current_files.copy()
            
            for f in self.display_files:
                self.add_entry(f['filename'], f"Type: {f['type'].capitalize()}\nRaw: {f['raw']} | Size: {f['size']}\nLast Modified: {f['last_modified']}\nPath: {f['path']}")

            self.metadata_display.setText("Metadata not yet set")

            #    if file_count.get(f['type']):
            #        file_count[f['type']] += 1
            #    else:
            #        file_count[f['type']] = 1
            
            #details = "\n-".join(f"{c} {t} files" for t, c in file_count.items())

            #self.metadata_display.setText(
            #    f"-Total Files: {sum(file_count.values())}\n-{details}"
            #)
    
    def filter_data(self):
        print("Filtering data")

    def sort_data(self):
        print("Sorting data")

        if not self.current_files:
            display_message(self, "No files to sort")
            return

        dialog = SortDialog(self, self.last_sort_choice)

        if dialog.exec_() == QDialog.Accepted:
            choice = dialog.get_selected_option()

            self.last_sort_choice = choice

            sorted_files = sort_files(self.display_files, choice)
            self.display_files = sorted_files

            self.clear_entries()

            for f in self.display_files:
                self.add_entry(f['filename'], f"Type: {f['type'].capitalize()}\nRaw: {f['raw']} | Size: {f['size']}\nLast Modified: {f['last_modified']}\nPath: {f['path']}")

            display_message(self, f"Applied {choice} Sort")


    def export_data(self):
        print("Exporting data")

        if not self.current_files:
            display_message(self, "No files to export")
            return

        dialog = ExportDialog(self)
        dialog.exec_()

    def export_to_json(self):
        print("Now actually exporting to json")
        
        downloads_path = Path.home() / "Downloads"
        #timestamp = datetime.datetime.now()
        
        file_path = downloads_path / f"folder_analysis.json"

        export_ready = []

        for f in self.current_files:
            export_ready.append({
                "filename": f["filename"],
                "path": f["path"],
                "name": f["name"],
                "extension": f["extension"],
                "raw": f["raw"],
                "size": f["size"],
                "type": f["type"].capitalize()
            })

        try:
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(export_ready, json_file, indent=4)

            display_message(self, f"Exported data to a .json file, find in Downloads")

        except Exception as error:
            display_message(self, f"Export failed: {error}")

    def export_to_txt(self):
        print("Now actually exporting to txt")

        downloads_path = Path.home() / "Downloads"
        #timestamp = datetime.datetime.now()

        file_path = downloads_path / f"folder_analysis.txt"

        try:
            with open(file_path, "w", encoding="utf-8") as txt_file:
                txt_file.write("Folder Analyzer Export\n")
                txt_file.write("-----------------------------------\n")

                for f in self.current_files:
                    txt_file.write(f"File: {f['filename']}\n")
                    txt_file.write(f"Path: {f['path']}\n")
                    txt_file.write(f"Name: {f['name']} | Ext: {f['extension']}\n")
                    txt_file.write(f"Size: {f['size']} ({f['raw']} bytes)\n")
                    txt_file.write(f"Type: {f['type'].capitalize()}\n")
                    txt_file.write("-----------------------------------\n")

            display_message(self, f"Exported data to a .txt file, find in Downloads")

        except Exception as error:
            display_message(self, f"Export failed: {error}")

    def search_files(self, text):
        query = text.lower().strip()

        for item in self.file_widgets:
            if query in item.filename:
                item.show()
            else:
                item.hide()
                item.toggle(False)

class FileItem(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, filename, metadata_text):
        super().__init__()
        self.filename = filename
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

        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)

        # File Button
        self.btn = QPushButton(f"📄 {filename}")
        self.btn.clicked.connect(lambda: self.clicked.emit(self))
        header_layout.addWidget(self.btn, 1)

        # Open File Button
        self.file_btn = QPushButton("OPEN") 
        self.file_btn.setFixedSize(55, 30)
        self.file_btn.clicked.connect(self.open_file)
        header_layout.addWidget(self.file_btn)

        self.layout.addLayout(header_layout)

        # Expanding info
        self.info_label = QLabel(metadata_text)
        self.info_label.setVisible(False) 
        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)

    def toggle(self, expand):
        self.info_label.setVisible(expand)

    def open_file(self):
        print("opening")
        print(self.filename)