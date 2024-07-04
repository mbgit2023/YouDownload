import select
import sys
import os.path
import requests
import time

import subprocess
from subprocess import Popen, PIPE
from pytube import YouTube
from urllib.parse import urlparse
from urllib.request import urlretrieve
from PyQt6.QtCore import Qt, QSize, QThreadPool, pyqtSlot, QRunnable, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout, QGridLayout, QLayout, QFrame, QRadioButton, QButtonGroup, QScrollArea, QMenu, QLineEdit, \
    QMessageBox, QSpinBox, QProgressBar, QSizePolicy



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('YouDownload')
        self.showMaximized()
        self.setStyleSheet("background-color: #292929; color: white;")

        container = QWidget()

        # Top layout and frame
        topLayout = QHBoxLayout()
        lblTip = QLabel("URL of the video")
        lblTip.setFixedWidth(160)
        lblTip.setStyleSheet("color: blue; font-weight: bold; font-size: 16px;")
        self.lineUrl = QLineEdit()
        self.lineUrl.setPlaceholderText("https://www.youtube.com/watch?v=e1w7R1hEvCs")
        self.lineUrl.setFixedWidth(1300)
        self.lineUrl.setFixedHeight(25)
        self.lineUrl.setStyleSheet("background-color: white; color: black; border-radius: 3px;")
        downButton = QPushButton()
        downButton.setFixedWidth(60)
        downButton.setStyleSheet("border: none;")
        downButton.setIcon(QIcon("./icons/download.png"))
        downButton.setIconSize(QSize(40, 40))
        downButton.clicked.connect(self.download)

        topFrame = QFrame()
        topFrame.setLayout(topLayout)
        topFrame.setStyleSheet("border: 1px solid grey; border-radius: 5px;")
        topFrame.setFixedHeight(50)
        lblTip.setStyleSheet("border: none; color: blue; font-weight: bold;")

        topLayout.addWidget(lblTip, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        topLayout.addWidget(self.lineUrl, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        topLayout.addWidget(downButton, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        topLayout.setAlignment(Qt.AlignmentFlag.AlignTop)


        # Left Layout (download bars and player)
        leftLayout = QVBoxLayout()
        leftFrame = QFrame()
        leftFrame.setFixedWidth(1250)
        leftFrame.setLayout(leftLayout)
        #leftFrame.setStyleSheet("border: 1px solid red;")

        self.downloadScroll = QScrollArea()
        self.downLayout = QVBoxLayout()
        self.downloadScroll.setLayout(self.downLayout)
        self.downloadScroll.setFixedHeight(400)

        self.videoLayout = QVBoxLayout()
        self.videoFrame = QFrame()
        self.videoFrame.setLayout(self.videoLayout)
        self.videoFrame.setFixedHeight(500)

        leftLayout.addWidget(self.downloadScroll, Qt.AlignmentFlag.AlignTop)
        leftLayout.addWidget(self.videoFrame)

        # Right Layout (video list)
        rightLayout = QVBoxLayout()
        rightFrame = QFrame()
        rightFrame.setFixedWidth(630)
        rightFrame.setLayout(rightLayout)
        rightFrame.setStyleSheet("border: 1px solid blue;")

        # Center Layout
        centerLayout = QHBoxLayout()
        centerLayout.addWidget(leftFrame)
        centerLayout.addWidget(rightFrame)

        layout = QVBoxLayout()
        layout.addWidget(topFrame)
        layout.addLayout(centerLayout)

        self.threadpool = QThreadPool()

        container.setLayout(layout)
        self.setCentralWidget(container)

    def download(self):
        p = subprocess.run(["python3", "./checkurl.py", self.lineUrl.text()], capture_output=True)
        if not p.returncode == 0:
            return False
        else:
            #q = subprocess.Popen(["python3", "./download.py", self.lineUrl.text()])
            urlvideo = self.lineUrl.text()

            try:
                yt = YouTube(urlvideo)
            except:
                subprocess.run(["python3", "popup.py", fr"Error during get the list", "", "red"])
                return False

            mp4_streams = yt.streams.filter(file_extension='mp4').all()
            i = 0
            buttonGroup = QButtonGroup()
            self.listlayout = []
            for video in mp4_streams:
                Separator = QFrame()
                Separator.setFrameShape(QFrame.Shape.HLine)
                layoutItem = QHBoxLayout()
                videoitem = QRadioButton(str(i))
                lblVideo = QLabel(f" {video.type}  -  Res: {video.resolution}  -  Size: {video.filesize} Bytes")
                videoitem.setStyleSheet("font-size: 18px;")
                lblVideo.setStyleSheet("font-size: 18px;")
                self.btnDownload = QPushButton()
                self.btnDownload.setText(str(i))
                self.btnDownload.setIcon(QIcon("./icons/download.jpg"))
                self.btnDownload.setIconSize(QSize(30, 30))
                self.btnStop = QPushButton()
                self.btnStop.setText(str(i))
                self.btnStop.setIcon(QIcon("./icons/stop.png"))
                self.btnStop.setIconSize(QSize(30, 30))
                self.btnStop.setDisabled(True)
                self.btnDownload.clicked.connect(self.downloadItem)
                buttonGroup.addButton(videoitem)
                layoutItem.addWidget(videoitem)
                layoutItem.addWidget(lblVideo, Qt.AlignmentFlag.AlignLeft)
                layoutItem.addWidget(self.btnDownload)
                layoutItem.addWidget(self.btnStop)
                self.downLayout.addLayout(layoutItem)
                self.downLayout.addWidget(Separator)
                self.listlayout.append(layoutItem)
                i = i + 1

        self.downloadScroll.setStyleSheet("background-color: #333333; color: white;")

    def downloadItem(self, item):
        item = self.sender().text()
        #p = subprocess.Popen(["python3", "download.py", self.lineUrl.text(), item])

        self.progress = QProgressBar()
        self.videoLayout.addWidget(self.progress)

        worker = Worker()
        worker.url = self.lineUrl.text()
        worker.item = item
        self.threadpool.start(worker)


    def update_progress(self, progress):
        self.progress.setValue(progress)

    def stopDownload(self):
        item = self.sender().text()


class Worker(QRunnable):
    url = ""
    item = 0
    @pyqtSlot()
    def run(self):
        for name in self.url.split("/"):
            pass

        filename = name + f"__{self.item}"
        logfile = fr"{os.environ['HOME']}/Downloads/{filename}.log"

        print (filename)

        p = subprocess.Popen(["python3", "download.py", filename, self.item])

        time.sleep(10)
        with open(logfile) as f:
            while True:
                q = subprocess.run(["zsh", "./getsize.sh", logfile], capture_output=True)
                print(q.stdout)
                size = q.stdout
                if size == 100.00 or size == 100 or size == 100.0:
                    break
                time.sleep(3)



        #if os.path.isfile(f"{os.environ['HOME']}/Downloads/'{filename}'"):
        #filepath = fr"{os.environ['HOME']}/Downloads/'{filename}'"
        #print(filepath)
        #print(str(filepath))

        #while True:
        #    print("CHECk")
        #    size = os.stat(filepath)
            #p = subprocess.run(["du -sb", f"{os.environ['HOME']}/Downloads/'{name}__{self.item}'"], capture_output=True)
            #p = subprocess.run(["zsh", "./getsize.sh", filename])
            #size = p.stdout
        #    print(size.st_size)
        #    time.sleep(3)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
