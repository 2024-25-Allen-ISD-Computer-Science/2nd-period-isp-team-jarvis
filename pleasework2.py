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
        pixmap = QPixmap("Jarvis_Background1.jpg")
        backdrop.setPixmap(pixmap)

        self.welcome = QLabel("Welcome to Jarvis", self) #label at top of window
        self.button1 = QPushButton("(voice icon)", self) #voice button
        self.button2 = QPushButton( self) #calender button
        self.button3 = QPushButton( self) #To-Do list
        self.button4 = QPushButton( self) #weather
        self.button5 = QPushButton( self) #smart appliences

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
        
        self.button2.setGeometry(250, 220, 161, 163)
        self.button2.hide
        self.button2.clicked.connect(self.calender)
        self.button2.setStyleSheet("font-size: 25px;"
                                   #"background-color: blue;"
                                  "border-radius : 80;")
        self.button3.setGeometry(250, 402, 161, 163)
        self.button3.hide
        self.button3.clicked.connect(self.list)
        self.button3.setStyleSheet("font-size: 25px;"
                                   #"background-color: blue"
                                   "border-radius: 80;")    

        self.button4.setGeometry(405, 502, 161, 163)
        self.button4.hide
        self.button4.clicked.connect(self.weather)
        self.button4.setStyleSheet("font-size: 25px;"
                                   #"background-color: blue;"
                                   "border-radius: 80;")    

        self.button5.setGeometry(405, 502, 161, 163)
        self.button5.hide
        self.button5.clicked.connect(self.house)
        self.button5.setStyleSheet("font-size: 25px;"
                                   #"background-color: blue;"
                                   "border-radius: 80;")
        
    def voice(self): #works!
        self.button1.setText("Im not that far yet")  
        #insert caller for whatever our voice method

    def calender(self):
        self.button2.setText("share the code")

    def list(self) :
        self.button3.setText("I dont think its done yet")

    def weather(self):
        self.button3.setText("atleast do this one")

    def house(self):
        self.button5.setText("NOT done. sry")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
