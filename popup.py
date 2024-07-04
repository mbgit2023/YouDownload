# Popup window for messages from the application

import sys
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Info')
        #self.setFixedWidth(400)
        self.setFixedHeight(150)
        self.setStyleSheet(fr"background-color: #292929; color: {sys.argv[3]};")
        screen = QApplication.primaryScreen().geometry()
        point = QPoint()
        point.setX(int(screen.width()/2-200))
        point.setY(int(screen.height()/2-75))
        self.move(point)

        lblText = QLabel()
        lblText.setText(fr"{sys.argv[1]} {sys.argv[2]}")
        lblText.setStyleSheet("font-size: 18px;")
        btnOk = QPushButton("Ok")
        btnOk.setFixedWidth(100)
        btnOk.setStyleSheet("color: white; font-size: 18px;")
        btnOk.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(lblText, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(btnOk, alignment=Qt.AlignmentFlag.AlignHCenter)

        container = QWidget()

        container.setLayout(layout)
        self.setCentralWidget(container)

    def close(self):
        app.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()