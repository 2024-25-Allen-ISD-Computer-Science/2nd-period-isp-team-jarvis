import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):  # This is for some window stuff but also defining elements here
        super().__init__()  # define any objects/elements that youre using here
        self.setWindowTitle("JaRVIS")
        self.setGeometry(2200, 300, 950, 750)# (Xoffset, YOffset, width, height)

        backdrop = QLabel(self)  # Background must be first
        backdrop.setGeometry(0, 0, 1100, 780)  #these are weird and refuse to go to initUI
        pixmap = QPixmap("this is bad.jpg")
        backdrop.setPixmap(pixmap)

        self.welcome = QLabel("Welcome to Jarvis", self) #label at top of window


        self.button1 = QPushButton("(voice icon)", self) #voice button


        self.button2 = QPushButton( self) #calender button
        self.initUI()

    def initUI(self): #the CSS of buttons and such
        self.welcome.setFont(QFont("courier new", 20))
        self.welcome.setGeometry(220, 0, 500, 100)
        self.welcome.setStyleSheet("color: white;")
        self.welcome.setAlignment(Qt.AlignCenter | Qt.AlignTop)# aligns text (label) to top and center of its space

        self.button1.setGeometry(405, 130, 161, 163)
        self.button1.hide
        self.button1.clicked.connect(self.voice)
        self.button1.setStyleSheet("font-size: 25px;"
                                   #"background-color: blue;"
                                   "border-radius : 80;")  # makes button circular

        self.button2.setGeometry(250, 220, 161, 163)
        self.button2.hide
        self.button2.clicked.connect(self.calender)
        self.button2.setStyleSheet("font-size: 25px;"
                                   #"background-color: blue;"
                                  "border-radius : 80;")




    def voice(self): #works!

        self.button1.setText("Im not that far yet")  # TEST THIS. should change button text when clicked
        #insert caller for whatever our voice method
    def calender(self):
        self.button2.setText("share the code")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
