import sys
from PyQt5.QtWidgets import QApplication
from widgets import FolderAnalyzer

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = FolderAnalyzer()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        pass