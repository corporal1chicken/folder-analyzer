from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QRadioButton, QDialog, QCheckBox)
from PyQt5.QtCore import Qt
from constants import SORT_OPTIONS, FILTER_OPTIONS

class ExportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Options")
        self.setFixedSize(360, 150)
        
        layout = QVBoxLayout(self)
        label = QLabel("How would you like to export?")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        btn_layout = QHBoxLayout()
  
        self.txt_btn = QPushButton("Export as .txt")
        self.txt_btn.clicked.connect(self.on_txt_clicked)

        self.json_btn = QPushButton("Export as .json")
        self.json_btn.clicked.connect(self.on_json_clicked)

        self.csv_btn = QPushButton("Export as .csv")
        self.csv_btn.clicked.connect(self.on_csv_clicked)
        
        btn_layout.addWidget(self.txt_btn)
        btn_layout.addWidget(self.json_btn)
        btn_layout.addWidget(self.csv_btn)
        layout.addLayout(btn_layout)

    def on_txt_clicked(self):
        print("Export as .txt")
        self.parent().export_to_txt()
        self.accept()

    def on_json_clicked(self):
        print("Export as .json")
        self.parent().export_to_json()
        self.accept()

    def on_csv_clicked(self):
        print("Export to .csv")
        self.parent().export_to_csv()
        self.accept()

class MessageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Message")
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        btn_layout = QHBoxLayout()
  
        self.txt_btn = QPushButton("Continue")
        self.txt_btn.clicked.connect(self.close_message)
        
        btn_layout.addWidget(self.txt_btn)
        layout.addLayout(btn_layout)

    def close_message(self):
        self.accept()

class SortDialog(QDialog):
    def __init__(self, parent=None, last_sort_choice=None):
        super().__init__(parent)
        self.setWindowTitle("Sort Options")
        self.setFixedSize(480, 240)
        
        layout = QVBoxLayout(self)
        self.message_label = QLabel("Sort files by:")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        self.radio_buttons = []
        
        for text in SORT_OPTIONS:
            radio = QRadioButton(text)
            layout.addWidget(radio)
            self.radio_buttons.append(radio)

            if text == last_sort_choice:
                radio.setChecked(True)
          
        btn_layout = QHBoxLayout()
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.continue_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

    def get_selected_option(self):
        for radio in self.radio_buttons:
            if radio.isChecked():
                return radio.text()
            
        return None
    
class FilterDialog(QDialog):
    def __init__(self, parent=None, applied_filters=None):
        super().__init__(parent)
        self.setWindowTitle("Filter Options")
        self.setFixedSize(480, 240)
        
        layout = QVBoxLayout(self)
        self.message_label = QLabel("Select filters:")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        self.check_buttons = []
        
        for text in FILTER_OPTIONS:
            checkbox = QCheckBox(text)
            layout.addWidget(checkbox)
            self.check_buttons.append(checkbox)

            if text in applied_filters:
                checkbox.setChecked(True)
          
        btn_layout = QHBoxLayout()
        self.continue_btn = QPushButton("Apply")
        self.continue_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.continue_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

    def get_filters(self):
        applied_filters = []

        for btn in self.check_buttons:
            if btn.isChecked():
                applied_filters.append(btn.text())
            
        return applied_filters