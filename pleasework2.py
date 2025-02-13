import sys
from tokenize import String

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

import Fawad_Wether 
from Fawad_WeatherWether import temp, weather
#import voice_stuff
#from voice_stuff import jarvis_main #no worky


class MainWindow(QMainWindow):
   def __init__(self):  # This is for some window stuff but also defining elements here
       super().__init__()  # define any objects/elements that youre using here
       self.setWindowTitle("JaRVIS")
       self.setGeometry(1800, 300, 950, 750)# (Xoffset, YOffset, width, height)

       backdrop = QLabel(self)  # Background must be first
       backdrop.setGeometry(0, 0, 1100, 780)  #these are weird and refuse to go to initUI
       pixmap = QPixmap("jarvis_homescreen2.jpg")
       backdrop.setPixmap(pixmap)

       self.welcome = QLabel("Welcome to Jarvis", self) #label at top of window
       self.button1 = QPushButton("(voice icon)", self) #voice button
       self.button2 = QPushButton( self) #calender button
       self.button3 = QPushButton("here", self) #ToDo list
       self.button4 = QPushButton("lever", self) #weather
       self.button5 = QPushButton("house", self) #smart home stuff if we get to it

       self.button_other = QPushButton(self)
       self.userinput = QLineEdit("city name", self)
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

       self.button3.setGeometry(250, 410  , 161, 163)
       self.button3.hide
       self.button3.clicked.connect(self.list)
       self.button3.setStyleSheet("font-size: 25px;"
                                  #"background-color: blue;"
                                  "border-radius : 80;")

       self.button4.setGeometry(408, 508, 158, 163)
       self.button4.hide
       self.counter = -1
       self.button4.clicked.connect(self.weather)
       self.button4.setStyleSheet("font-size: 25px;"
                                  #"background-color: blue;"
                                 "border-radius : 80;")

       self.button5.setGeometry(560, 220, 161, 163)
       self.button5.hide
       self.button5.clicked.connect(self.house)
       self.button5.setStyleSheet("font-size: 25px;"
                                  #"background-color: blue;"
                                  "border-radius: 80;")

       self.button_other.setGeometry(560, 410, 161, 163)
       self.button_other.hide
       self.button_other.clicked.connect(self.otherButton)
       self.button_other.setStyleSheet("font-size: 25px;"
                                        #"background-color: blue;"
                                       "border-radius: 80;")

       self.userinput.setGeometry(300, 680, 400, 50)
       self.userinput.setStyleSheet("font-size: 25px;"
                                    "background-color: #802424;")
       self.userinput.hide()




   def voice(self): #works!
       #voice_stuff.jarvis_main() #go install the thingys :)
       self.button1.setText("it no worky")  # TEST THIS. should change button text when clicked
       #voice_stuff.jarvis_main()

   def calender(self):
       self.button2.setText("share the code")
       print("share the calender code")

   def list(self):
           self.button3.setText("I dont think its done yet")
           print("share the code for ToDo list plz")

   def weather(self): #invoked when button clicked
       self.counter += 1
       if(self.counter % 2 == 0):

           #self.button4.setText("blob")
           self.button4.show()
           self.button4.setText("")
           self.button4.setStyleSheet("background-color: #52727a;"#hide icon
                                      "border-radius: 75;"
                                      "font-size: 25px;")
           self.userinput.show() #editable text box
           self.userinput.returnPressed.connect(lambda: doThing())#when hit enter, invokes doThing

           def doThing():
               city = self.userinput.text()
               windy = weather(city)
               dawgie = temp(city)
               windyDawg = str(dawgie) + "°F, " + windy
               print(windyDawg)
               asd = 44
               self.button4.setText(windyDawg)
       else:
           self.userinput.hide()
           self.button4.hide()

   def house(self):
       self.button5.setText("NOT done. sry")
       print("no ones done stuff for the smart applince yet")

   def otherButton(self):
       self.button_other.setText("non-functional")
       print("useless")

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec_())

