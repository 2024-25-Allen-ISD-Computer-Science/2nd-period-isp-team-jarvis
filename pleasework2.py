import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()#define any objects/elements that youre using here
        self.setWindowTitle("JaRVIS") 
        self.setGeometry(500, 500, 1000, 1000) #first 2 are where x/y offset. How far the window is from top left corner. last 2 are window size
# this is stuff for text, QLabel is text and everything behind it is color and such
        label = QLabel("Welcome to Jarvis", self)
        
#end of title label, startof first button
        self.button = QPushButton("voice search", self)
        self.label = QLabel("yea I DO NOT know how to implement that yet:/", self)#Add a function later that fades to whatever our voice dude wrote)
        self.initUI()

    def initUI(self): #give more specifics on individual elements here
        label.setfont(QFont("arial", 30))
        label.setgeometry(0, 0, 500, 100) #xy offset and dimensions of the label inside the window
        label.setStyleSheet("color: white;"
                            "background-color: #383071;" #A dark blue or purple
                            "font-weight: bold;"
                            "font-style: italic;")
        label.setAlignment(Qt.AlignCenter | Qt.AlignTop) #alligns text (label) to top and center of its space
        
        self.button.setGeometry(400, 200, 200, 200)
        self.button.setStyleSHeet("font-size: 20px;")
        self.button.clicked.connect(self.on_click)

        self.label.setGeometry    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
