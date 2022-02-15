# -*- coding: utf-8 -*-
# @Author: @IamRezaMousavi
# @Date:   2022-02-14 06:20:06
# @Last Modified by:   @IamRezaMousavi
# @Last Modified time: 2022-02-15 05:49:15

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
    
    def initUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.windowFrame.setStyleSheet("""QFrame#windowFrame
                            {
                                background-color: rgba(0, 0, 0, 200);
                            }
                            """)
        
        self.ui.backwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.ui.backwardButton.clicked.connect(self.changeSize)
        self.ui.playButton.setEnabled(False)
        self.ui.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.playButton.clicked.connect(self.playMusic)
        self.ui.forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.ui.forwardButton.clicked.connect(self.forwardMusic)
        
        self.ui.openButton.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.ui.openButton.clicked.connect(self.openFile)
        self.ui.songSlider.setRange(0, 0)
        self.ui.songSlider.sliderMoved.connect(self.setPosition)
        
        self.player = QMediaPlayer()
        
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.ui.songList.clicked.connect(self.setState)
        self.ui.songList.doubleClicked.connect(self.playMusic)
    
    def changeSize(self):
        height = self.ui.bodyFrame.height()
        newHeight = 0 if height == 331 else 331
        
        minHeightAnimation = QPropertyAnimation(self.ui.bodyFrame, b"minimumHeight")
        minHeightAnimation.setDuration(600)
        minHeightAnimation.setStartValue(height)
        minHeightAnimation.setEndValue(newHeight)
        
        maxHeightAnimation = QPropertyAnimation(self.ui.bodyFrame, b"maximumHeight")
        maxHeightAnimation.setDuration(600)
        maxHeightAnimation.setStartValue(height)
        maxHeightAnimation.setEndValue(newHeight)
        
        windowHeight = self.ui.windowFrame.height()
        newWindowHeight = 114 if height else newHeight + 114
        
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
                                          "Audio Files (*.mp3 *.wav *.ogg)") #MP3, FLAC, M4A, AAC, OGG, 3GP, AMR, APE, MKA, Opus, Wavpack, Musepack
        if not names[0]:
            return
        self.ui.songList.addItems(names[0])
        self.ui.songList.setCurrentRow(0)
        self.ui.playButton.setEnabled(True)
        self.changeSize()
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
            self.ui.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.player.pause()
            self.position = self.player.position()
            self.ui.playButton.setText("Play")
            self.ui.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
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
        self.ui.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
    def forwardMusic(self):
        index = self.songList.currentRow()
        index = index if index < self.songList.count()-1 else -1
        try:
            self.ui.songList.setCurrentRow(index + 1)
            self.ui.playButton.setText("Play")
            self.playMusic()
        except:
            self.setFocus(True)
    
    def backwardMusic(self):
        index = self.songList.currentRow()
        index = index if index > 0 else self.songList.count()
        try:
            self.ui.songList.setCurrentRow(index - 1)
            self.ui.playButton.setText("Play")
            self.playMusic()
        except:
            self.setFocus(True)
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down:
            print("DOWN")
            volume = self.player.volume()
            self.player.setVolume(volume - 5)
        elif event.key() == Qt.Key_Up:
            print("UP")
            volume = self.player.volume()
            self.player.setVolume(volume + 5)
        elif event.key() == Qt.Key_Right:
            self.position = self.player.position()
            self.player.setPosition(self.position + 5000)
        elif event.key() == Qt.Key_Left:
            self.position = self.player.position()
            self.player.setPosition(self.position - 5000)
        elif event.key() == Qt.Key_Space:
            self.playMusic()
        elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.close()
            print("Enter")

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
