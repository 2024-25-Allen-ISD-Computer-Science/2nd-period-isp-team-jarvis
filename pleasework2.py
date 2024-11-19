import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JaRVIS") 
        self.setGeometry(0, 0, 500, 500) #first 2 are where x/y offset. How far the window is from top left corner. last 2 are window size
# this is stuff for text, QLabel is text and everything behind it is color and such
        label = QLabel("System: Downloading more ram...", self)
        label.setfont(QFont("arial", 30))
        label.setgeometry(0, 0, 500, 100) #xy offset and dimensions of the label inside the window
        label.setStyleSheet("color: white;"
                            "background-color: #314f71;"
                            "font-weight: bold;"
                            "font-style: italic;")

        label.setAlignment(Qt.AlignCenter | Qt.AlignTop) #alligns text (label) to top and center of its space

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
