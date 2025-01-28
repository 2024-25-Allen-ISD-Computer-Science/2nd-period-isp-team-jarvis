import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self): #This is for some window stuff but also defining elements here
        super().__init__()#define any objects/elements that youre using here
        self.setWindowTitle("JaRVIS") 
        self.setGeometry(500, 500, 1000, 750) #(Xoffset, YOffset, width, height)
        Background = QLabel(self) #Background must be first
        label = QLabel("Welcome to Jarvis", self)
        self.button = QPushButton("voice search", self)#making buttons "self.bla" means that they arent local to that function and can interact with other functions
        self.initUI()

    def initUI(self): #define elements and their characteristics here
        background.setGeometry(0 ,0, 1000, 750) #background photo
        pixmap = QPixmap("Jarvis_Background1.jpg")
        background.setPixmap(Pixmap)
        background.setScaledContents(True)

        welcome = Qlabel("Welcome to Jarvis", self)
        welcome.setfont(Qfont("arial", 40))
        welcome.setgeometry(250, 0, 500, 100) 
        label.setStyleSheet("color: white;"
                            "font-weight: bold;"
                            "font-style: italic;")
        label.setAlignment(Qt.AlignCenter | Qt.AlignTop) #alligns text (label) to top and center of its space
        
        
        self.button.setGeometry(400, 200, 200, 200)
        self.button.setStyleSheet("font-size: 20px;")
        self.button.clicked.connect(self.on_click)
        self.button.hide()

        self.label.setGeometry    
        def on_click(self):
            self.button = QPushButton("Im not that far yet", self)#TEST THIS. should change button text when clicked
            #later on needs to open our voice recognition function 

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
