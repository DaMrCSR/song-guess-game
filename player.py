import sys, os, time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton, QPlainTextEdit, QListWidget, QSlider,QProgressBar, QCompleter, QLineEdit,QVBoxLayout,QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QStandardItem, QStandardItemModel,QFont
import wave
import contextlib
import random


class UI(QMainWindow):
    
    
    global time_sec
    time_sec = 1
    
    def __init__(self):
        super(UI,self).__init__()

        #Load ui file
        uic.loadUi("heardle2.ui", self)

        self.setWindowTitle("Heardle 2")



        #Widget Definitions
        self.listview = self.findChild(QListWidget, "guessedSong")
        self.textedit = self.findChild(QLineEdit, "typeGuess")
        self.button1 =  self.findChild(QPushButton, "playSong")
        self.button2 =  self.findChild(QPushButton, "skipButton")
        self.button3 =  self.findChild(QPushButton, "pushButton")
        self.slider = self.findChild(QSlider, 'verticalSlider')
        self.progressbar = self.findChild(QProgressBar,'progressBar')

        #play sound
        self.button1.clicked.connect(self.playSound)

        self.textedit.returnPressed.connect(self.guess)


        #extra time
        self.button2.clicked.connect(self.skip)

        #reset
        self.button3.clicked.connect(self.reset)

        #change volume
        self.slider.valueChanged.connect(self.volume)

        self.player = QMediaPlayer()

        fnt = QFont("Open Sans", 12)

        mainLayout = QVBoxLayout()
        #input field
        
        self.textedit.setFixedHeight(50)
        self.textedit.setFont(fnt)
       # self.textedit.editingFinished.connect(self.addEntry)
        mainLayout.addWidget(self.textedit)
        
        self.model = QStandardItemModel()
        completer = QCompleter(self.model, self)
        self.textedit.setCompleter(completer)

        self.console = QTextEdit()
        self.console.setFont(fnt)
        mainLayout.addWidget(self.console)

        

        #Show the App
        self.show()




        for root, dirs, files in os.walk("."):
        # select file name
            for file in files:
        # check the extension of files
                if file.endswith(('.wav','.mov')):
            # print whole path of files
                    entryItem = os.path.join(file.lower())
                    
                
                    

                    self.console.append(entryItem)

                    if not self.model.findItems(entryItem):
                        self.model.appendRow(QStandardItem(entryItem))

        global list
        list = []
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(('.wav','.mov','.mp3')):
                    entryItem = os.path.join(file.lower())
                    list.append(entryItem)
                    print(entryItem)
        
        global selection
        selection = random.choice(list)
    
        
    def guess(self):
        guess = self.textedit.text()
        if guess == selection:
            print("Win")
        else:
            print("WRONG!")
            self.listview.addItem(guess)
            #self.listview.setIcon(qIcon)
    
    def reset(self):
        selection = random.choice(list)
        print(selection)
        
    def playSound(self):
        full_file_path = os.path.join(os.getcwd(), selection)
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)

        self.player.setMedia(content)
        self.player.play()
        
        global time_sec
        temp  = time_sec
        
        while time_sec:
            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            time_sec -= 1
            with contextlib.closing(wave.open(selection,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                x = (time_sec/duration)*100
            self.progressbar.setValue(int(x))
        time_sec = temp


        self.player.stop()
        print("played for " + str(time_sec)  + " sec")

    def skip(self):
        
        global time_sec

        time_sec +=1

    def volume(self, value):
        currentVolume = self.player.volume()
        self.player.setVolume(value)
       # self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(5)

# Initialize App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
    