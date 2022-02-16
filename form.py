# -*- coding: utf-8 -*-
# @Author: @IamRezaMousavi
# @Date:   2022-02-14 06:20:06
# @Last Modified by:   @IamRezaMousavi
# @Last Modified time: 2022-02-16 21:19:55

from PyQt5.QtWidgets import (QApplication, QMainWindow, QStyle, QFileDialog)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import uic
import sys
import os

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.song = ""
        self.position = 0
        self.ui = uic.loadUi("form.ui", self)
        self.initUi()
        self.addShurtcut()
        self.oldPos = QPoint()
    
    def initUi(self):
        self.setWindowTitle("Musicing")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.ui.backwardButton.setIcon(QIcon("./files/backwardIcon.png"))
        self.ui.backwardButton.clicked.connect(self.backwardMusic)
        self.ui.playButton.setEnabled(False)
        self.ui.playButton.setIcon(QIcon("./files/whitePlayIcon.png"))
        self.ui.playButton.setIconSize(QSize(14, 14))
        self.ui.playButton.clicked.connect(self.playMusic)
        self.ui.forwardButton.setIcon(QIcon("./files/forwardIcon.png"))
        self.ui.forwardButton.clicked.connect(self.forwardMusic)
        
        self.ui.songSlider.setRange(0, 0)
        self.ui.songSlider.sliderMoved.connect(self.setPosition)
        
        self.ui.moreButton.clicked.connect(self.changeSize)
        self.ui.lessButton.clicked.connect(self.changeSize)
        
        self.ui.openButton.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.ui.openButton.clicked.connect(self.openFile)
        self.ui.aboutButton.clicked.connect(self.showAboutMessage)
        
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        
        self.ui.songList.clicked.connect(self.setState)
        self.ui.songList.doubleClicked.connect(self.playMusic)
        
        self.ui.feedbackLabel.setText("Start Program")
    
    def addShurtcut(self):
        self.openShortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.openShortcut.activated.connect(self.openFile)
    
    def changeSize(self):
        height = self.ui.bodyFrame.height()
        newHeight = 0 if height == 332 else 332
        
        minHeightAnimation = QPropertyAnimation(self.ui.bodyFrame, b"minimumHeight")
        minHeightAnimation.setDuration(600)
        minHeightAnimation.setStartValue(height)
        minHeightAnimation.setEndValue(newHeight)
        
        maxHeightAnimation = QPropertyAnimation(self.ui.bodyFrame, b"maximumHeight")
        maxHeightAnimation.setDuration(600)
        maxHeightAnimation.setStartValue(height)
        maxHeightAnimation.setEndValue(newHeight)
        
        windowHeight = self.ui.windowFrame.height()
        newWindowHeight = 111 if height else newHeight + 111
        
        minWindowAnimation = QPropertyAnimation(self.ui.windowFrame, b"minimumHeight")
        minWindowAnimation.setDuration(600)
        minWindowAnimation.setStartValue(windowHeight)
        minWindowAnimation.setEndValue(newWindowHeight)
        
        maxWindowAnimation = QPropertyAnimation(self.ui.windowFrame, b"maximumHeight")
        maxWindowAnimation.setDuration(600)
        maxWindowAnimation.setStartValue(windowHeight)
        maxWindowAnimation.setEndValue(newWindowHeight)
        
        self.animation = QParallelAnimationGroup()
        self.animation.addAnimation(minHeightAnimation)
        self.animation.addAnimation(maxHeightAnimation)
        self.animation.addAnimation(maxWindowAnimation)
        self.animation.addAnimation(minWindowAnimation)
        self.animation.start()
        self.setFocus(True)
    
    def openFile(self):
        fileName = QFileDialog()
        fileName.setFileMode(QFileDialog.ExistingFile)
        names = fileName.getOpenFileNames(self,
                                          "Open Files",
                                          os.path.expanduser("~"),
                                          "Audio Files (*.mp3 *.wav *.ogg *.aac *.3gp *.amr *.flac, *.m4a, *.amr, *.ape, *.mka, *.opus, *.wavpack, *.musepack)")
        if not names[0]:
            return
        self.ui.songList.addItems(names[0])
        self.ui.songList.setCurrentRow(0)
        self.ui.playButton.setEnabled(True)
        self.ui.feedbackLabel.setText("Open File(s)")
        self.setFocus(True)
    
    def playMusic(self):
        self.setFocus(True)
        if self.ui.playButton.text() == "Play":
            path = self.songList.currentItem().text()
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.position = self.position if path == self.song else 0
            self.player.setPosition(self.position)
            self.player.play()
            self.song = path
            self.ui.playButton.setText("Pause")
            self.ui.playButton.setIcon(QIcon("./files/pauseIcon.png"))
            self.ui.feedbackLabel.setText("Play...")
        else:
            self.player.pause()
            self.position = self.player.position()
            self.ui.playButton.setText("Play")
            self.ui.playButton.setIcon(QIcon("./files/whitePlayIcon.png"))
            self.ui.feedbackLabel.setText("Pause")
    
    def setPosition(self, position):
        self.player.setPosition(position)
    
    def positionChanged(self, position):
        self.ui.songSlider.setValue(position)
        duration = self.player.duration()
        if position == duration and (position, duration) != (0, 0):
            self.forwardMusic()
    
    def durationChanged(self, duration):
        self.ui.songSlider.setRange(0, duration)
    
    def setState(self):
        self.ui.playButton.setEnabled(True)
        self.ui.playButton.setText("Play")
        self.ui.playButton.setIcon(QIcon("./files/whitePlayIcon.png"))
    
    def forwardMusic(self):
        index = self.songList.currentRow()
        index = index if index < self.songList.count()-1 else -1
        try:
            self.ui.songList.setCurrentRow(index + 1)
            self.ui.playButton.setText("Play")
            self.playMusic()
        except:
            self.setFocus(True)
        self.ui.feedbackLabel.setText("Play Forward Music")
    
    def backwardMusic(self):
        index = self.songList.currentRow()
        index = index if index > 0 else self.songList.count()
        try:
            self.ui.songList.setCurrentRow(index - 1)
            self.ui.playButton.setText("Play")
            self.playMusic()
        except:
            self.setFocus(True)
        self.ui.feedbackLabel.setText("Play Backward Music")
    
    def showAboutMessage(self):
        message = QMessageBox()
        message.setStyleSheet("""QMessageBox
                              {
                                  background-color: rgb(19, 19, 19);
                              }
                              QMessageBox QLabel
                              {
                                  color: white;
                              }
                              """)
        message.setWindowTitle("About")
        message.setText("Created by")
        message.setInformativeText("@IamRezaMousavi")
        message.setDetailedText("Meet me at\nGithub.com/IamRezaMousavi")
        message.exec()
        
        
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            volume = self.player.volume()
            newVolume = volume - 5
            self.player.setVolume(newVolume)
            self.ui.feedbackLabel.setText("Volume Down: " + str(newVolume if newVolume >= 0 else 0))
        
        elif event.key() == Qt.Key_Up:
            volume = self.player.volume()
            newVolume = volume + 5
            self.player.setVolume(newVolume)
            self.ui.feedbackLabel.setText("Volume Up: " + str(newVolume if newVolume <= 100 else 100))
        
        elif event.key() == Qt.Key_Right:
            self.position = self.player.position()
            self.player.setPosition(self.position + 5000)
            self.ui.feedbackLabel.setText("Go to +5 sec")
        
        elif event.key() == Qt.Key_Left:
            self.position = self.player.position()
            self.player.setPosition(self.position - 5000)
            self.ui.feedbackLabel.setText("Go to -5 sec")
        
        elif event.key() == Qt.Key_Space:
            self.playMusic()
        
        elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.close()

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
