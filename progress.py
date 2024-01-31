import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
import time

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.motion_sec = 7
        self.freq = 2000
        self.timing = 40
        self.count = self.motion_sec*self.freq/self.timing
        self.kote =  self.motion_sec*self.freq/self.timing

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(0, 0, 300, 50)
        self.pbar.setValue(100)
        
        self.setWindowTitle("QT Progressbar Example")
        self.setGeometry(0,0,500,500)
        # self.showFullScreen()


        self.reset_button = QPushButton('Reset',self)
        self.reset_button.clicked.connect(self.close)
        self.reset_button.setGeometry(0,100,200,50)

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_emg)
        self.timer.start(1)

        layout = QVBoxLayout()
        layout.addWidget(self.pbar)
        layout.addWidget(self.reset_button)
        self.setLayout(layout)

        self.show()

    def handleTimer(self):
        value = self.pbar.value()
        if self.count > 0:
            self.count = self.count - 1
            value = (100/self.kote)*self.count
            self.pbar.setValue(value)
        else:
            self.timer.stop()
        pass
    
    def get_emg(self):
        time.sleep(0.02)
        self.handleTimer()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())