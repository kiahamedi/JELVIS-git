#!/usr/bin/env python3
import os
import sys
import time
import aiml
import pyttsx3
import urllib3
import warnings
import threading
import pocketsphinx
from os import system
import speech_recognition as sr
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import QMovie , QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu , QMessageBox


mode = "voice"
if len(sys.argv) > 1:
    if sys.argv[1] == "--voice" or sys.argv[1] == "voice":
        try:
            import speech_recognition as sr
            mode = "voice"
        except ImportError:
            print("\nInstall SpeechRecognition to use this feature.\nStarting text mode\n")
terminate = ['bye','buy','shutdown','exit','quit','gotosleep','goodbye']


class QTextMovieLabel(QLabel):

    def __init__(self, fileName):
        QLabel.__init__(self)

        thread = Thread(self)
        m = QMovie(fileName)
        m.start()
        self.setMovie(m)
        app.aboutToQuit.connect(thread.stop)
        thread.start()

    def setMovie(self, movie):
        QLabel.setMovie(self, movie)
        s=movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()




class Thread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.window = parent
        self._lock = threading.Lock()
        self.running = True

    def run(self):
        self.running = True

        def internet_on():
            try:
                urllib2.urlopen('http://216.58.192.142', timeout=1)
                return True
            except urllib2.URLError as err:
                return False


        def speak(jarvis_speech):
           tts = gTTS(text=jarvis_speech, lang='en')
           tts.save('jarvis_speech.mp3')
           mixer.init()
           mixer.music.load('jarvis_speech.mp3')
           mixer.music.play()
           while mixer.music.get_busy():
               time.sleep(1)

        def offline_speak(jarvis_speech):
            engine = pyttsx3.init()
            engine.say(jarvis_speech)
            engine.runAndWait()

        def listen():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Talk to JELVIS: ")
                audio = r.listen(source)
            try:
                print (r.recognize_google(audio))
                return  r.recognize_google(audio)
                #if internet_on() == True:
                #    print r.recognize_google(audio)
                #    return  r.recognize_google(audio)
                #else:
                #    print r.recognize_sphinx(audio)
                #    return  r.recognize_sphinx(audio)

            except sr.UnknownValueError:
                #offline_speak("I couldn't understand what you said! Would you like to repeat?")
                return(listen())
            except sr.RequestError as e:
                print("Could not request results from speech service; {0}".format(e))
            #except sr.UnknownValueError:
            #    return(listen())

        kernel = aiml.Kernel()

        if os.path.isfile("bot_brain.brn"):
            kernel.bootstrap(brainFile = "bot_brain.brn")
        else:
            kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
            #kernel.saveBrain("bot_brain.brn")
        # kernel now ready for use
        while True:
            if mode == "voice":
                response = listen()
            else:
                response = raw_input("Talk to JELVIS : ")
            if response.lower().replace(" ","") in terminate:
                #break
                response = listen()
            jarvis_speech = kernel.respond(response)
            print ("JELVIS: " + jarvis_speech)
            offline_speak(jarvis_speech)
            #if internet_on() == True:
            #    speak(jarvis_speech)
            #else:
            #    offline_speak(jarvis_speech)

    def stop(self):
        engine = pyttsx3.init()
        engine.say("goodbye sir")
        engine.runAndWait()
        self.running = False



if __name__ == '__main__':

    app = QApplication(sys.argv)

    # Body with show jelvis
    l = QTextMovieLabel('icons/jelvis.gif')
    l.setWindowTitle("JELVIS")
    l.show()


    # Tray icon and menu
    trayIcon = QSystemTrayIcon(QIcon('icons/jelvis_try.png'), parent=app)
    trayIcon.setToolTip('JELVIS 1.0.2')
    trayIcon.show()
    menu = QMenu()

    # Show Jelvis window
    showAction = menu.addAction('Show JELVIS')
    showAction.triggered.connect(l.show)

    # Hide Jelvis Window
    showAction = menu.addAction('Hide JELVIS')
    showAction.triggered.connect(l.hide)

    # QMessageBox Info
    msg = QMessageBox()
    msg.setWindowTitle("Info")
    msg.setText("\nJELVIS v1.0.2\n\nThis project can be an audio assistant on your operating system and perform the tasks that you are considering for it. You can use different scripts to use in the language interface\n\nhttps://github.com/kiahamedi/JELVIS\nkia.arta9793@gmail.com\n")
    moreAction = menu.addAction('More info')
    moreAction.triggered.connect(msg.show)

    # Exit Tray icon
    exitAction = menu.addAction('Exit')
    exitAction.triggered.connect(app.quit)

    trayIcon.setContextMenu(menu)


    sys.exit(app.exec_())
