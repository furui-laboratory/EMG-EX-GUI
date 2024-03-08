import sys
sys.path.append('..')
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtTest
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import time

class Test(QWidget):

    def __init__(self,parent=None):

        super().__init__(parent)
        self.setGeometry(0,0,1920,1080)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10000)
        

    def update(self):
        self.close()


def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Test()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()