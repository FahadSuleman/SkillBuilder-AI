import sys
from PyQt5.QtWidgets import QApplication
from ui_main import MainWindow

def load_stylesheet():
    try:
        with open("assets/style.qss", "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
