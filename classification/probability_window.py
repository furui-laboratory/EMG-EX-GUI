import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
from PyQt5 import QtGui
# importing pyqtgraph as pg 
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg 
import random
import numpy as np


class ProbabilityWindow(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.class_n = 3
        layout = QVBoxLayout(self)
        self.win = pg.plot() 
        self.win.setBackground("#FFFFFF00")     
        layout.addWidget(self.win)

        self.win.setGeometry(100, 100, 600, 500)

        # create pyqt5graph bar graph item 
        # with width = 0.6 
        # with bar colors = green 
        self.prb = [0, 0, 0]
        y = [1, 2, 3]
        self.bargraph = pg.BarGraphItem(x0=0, y=y, height=0.6, width=self.prb)
        # self.bargraph = pg.BarGraphItem(x = self.x, height = self.prb, width = 0.6, brush ='g') 

        # add item to plot window 
        # adding bargraph item to the window 
        self.win.addItem(self.bargraph) 

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(10)

    def update(self,prb):
        # rng = np.random.default_rng()
        # self.prb = rng.random(3)*100
        self.prb = np.mean(prb,axis=0)
        self.bargraph.setOpts(width=self.prb)



def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    window = ProbabilityWindow(3)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()