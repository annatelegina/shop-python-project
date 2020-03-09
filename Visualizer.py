import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Visualizer:
    def __init__(self):
        self.start_window()


    def start_window(self):
        app = QApplication(sys.argv)
        widget = QWidget()
        textLabel = QLabel(widget)

        button1 = QPushButton(widget)
        button1.setText("Start experiment")
        button1.setFixedSize(200, 30)
        button1.move(150,650)
        button1.clicked.connect(button1_clicked)

        button2 = QPushButton(widget)
        button2.setText("Pause")
        button2.setFixedSize(200, 30)
        button2.move(450,650)
        button2.clicked.connect(button2_clicked)

        button3 = QPushButton(widget)
        button3.setText("Exit app")
        button3.setFixedSize(200, 30)
        button3.move(750,650)
        button3.clicked.connect(button2_clicked)

        widget.setGeometry(300,300,1000,700)
        widget.setWindowTitle("Supermarket imitation")
        widget.show()
        sys.exit(app.exec_())

