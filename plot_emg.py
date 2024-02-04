from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QGraphicsProxyWidget,QWidget, QDesktopWidget
import sys
from src.delsys import DataHandle

N_CHANNELS = 6 # 3以外に設定した時の挙動は未検証

# Screen size (pixels)
WIDTH = 1536
HEIGHT = 960

# Plot scale
XRANGE = 16000
YRANGE = 0.5

class PlotWindow:
    def __init__(self):
        self.win=pg.GraphicsLayoutWidget(show=True) 
        self.win.resize(WIDTH, HEIGHT)
        self.win.move(0, 0)
        self.plt = []
        for c in range(N_CHANNELS):
            self.plt.append(self.win.addPlot(rowSpan=1))
            self.win.nextRow()

        for c in range(N_CHANNELS):
            self.plt[c].setXRange(0, XRANGE)
            self.plt[c].setYRange(-YRANGE,YRANGE)


        self.CHUNK = 40
        self.RATE = 2000

        self.dh = DataHandle(N_CHANNELS)
        self.dh.initialize_delsys()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0.1)

        self.data = np.zeros((N_CHANNELS, self.CHUNK))

        self.curves = [[] for i in range(N_CHANNELS)]
        self.time = np.zeros(N_CHANNELS)

    def update(self):
        rawEMG = self.dh.get_emg()
        for c in range(N_CHANNELS):
            self.data = rawEMG[:, c] * 1000
            self.curve = self.plt[c].plot(pen="y")
            self.curves[c].append(self.curve)
            self.curve = self.curves[c][-1]
            self.curve.setData(np.arange(self.time[c], self.time[c] + 40), self.data)
            self.time[c] += 40
            if self.time[c] > 16000:
                self.plt[c].clear()
                self.curves[c] = []
                self.time[c] = 0

    
if __name__=="__main__":
    
    plotwin=PlotWindow()
    if (sys.flags.interactive!=1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()
        