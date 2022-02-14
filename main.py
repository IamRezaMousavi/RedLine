# -*- coding: utf-8 -*-
# @Author: @IamRezaMousavi
# @Date:   2022-02-13 14:21:49
# @Last Modified by:   @IamRezaMousavi
# @Last Modified time: 2022-02-13 20:03:00

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel,
                             QHBoxLayout, QPushButton, QGroupBox, QSlider,
                             QListWidget, QStyle, QFileDialog)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import Qt, QUrl
import sys
import os

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.initUi()
        self.song = ""
        self.position = 0
    
    def initUi(self):
        self.setStyleSheet("""QMainWindow
                           {
                               background-color: gray;
                           }
                           """)
        
        vbLayout = QVBoxLayout()
        vbLayout.setAlignment(Qt.AlignCenter)
        
        nameLabel = QLabel("Music Player")
        nameLabel.setAlignment(Qt.AlignCenter)
        vbLayout.addWidget(nameLabel)
        
        hbLayout = QHBoxLayout()
        backwardButton = QPushButton(clicked=self.backwardMusic)
        backwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.playButton = QPushButton("Play", clicked=self.playMusic)
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        forwardButton = QPushButton(clicked=self.forwardMusic)
        forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        hbLayout.addWidget(backwardButton)
        hbLayout.addWidget(self.playButton)
        hbLayout.addWidget(forwardButton)
        vbLayout.addLayout(hbLayout)
        
        hbLayout2 = QHBoxLayout()
        openFileButton = QPushButton(clicked=self.openFile)
        openFileButton.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)
        
        hbLayout2.addWidget(openFileButton)
        hbLayout2.addWidget(self.slider)
        vbLayout.addLayout(hbLayout2)
        
        self.songList = QListWidget()
        vbLayout.addWidget(self.songList)
        
        box = QGroupBox()
        box.setLayout(vbLayout)
        self.setCentralWidget(box)
        
        self.player = QMediaPlayer()
        
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.songList.clicked.connect(self.setState)
        self.songList.doubleClicked.connect(self.playMusic)
    
    def openFile(self):
        fileName = QFileDialog()
        fileName.setFileMode(QFileDialog.ExistingFile)
        names = fileName.getOpenFileNames(self,
                                          "Open Files",
                                          os.path.expanduser("~"),
                                          "Audio Files (*.mp3 *.wav *.ogg)")
        if not names[0]:
            return
        self.songList.addItems(names[0])
        self.songList.setCurrentRow(0)
        self.playButton.setEnabled(True)
    
    def playMusic(self):
        if self.playButton.text() == "Play":
            path = self.songList.currentItem().text()
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.position = self.position if path == self.song else 0
            self.player.setPosition(self.position)
            self.player.play()
            self.song = path
            self.playButton.setText("Pause")
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.player.pause()
            self.position = self.player.position()
            self.playButton.setText("Play")
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
    def setPosition(self, position):
        self.player.setPosition(position)
    
    def positionChanged(self, position):
        self.slider.setValue(position)
        duration = self.player.duration()
        if position == duration and (position, duration) != (0, 0):
            self.forwardMusic()
    
    def durationChanged(self, duration):
        self.slider.setRange(0, duration)
    
    def setState(self):
        self.playButton.setEnabled(True)
        self.playButton.setText("Play")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
    def forwardMusic(self):
        index = self.songList.currentRow()
        index = index if index < self.songList.count()-1 else -1
        self.songList.setCurrentRow(index + 1)
        self.playButton.setText("Play")
        self.playMusic()
    
    def backwardMusic(self):
        index = self.songList.currentRow()
        index = index if index > 0 else self.songList.count()
        self.songList.setCurrentRow(index - 1)
        self.playButton.setText("Play")
        self.playMusic()

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
