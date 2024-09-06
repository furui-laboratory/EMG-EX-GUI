from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QGraphicsProxyWidget,QWidget,QVBoxLayout
import sys
from src.delsys import DataHandle



# Screen size (pixels)
WIDTH = 1536
HEIGHT = 960

# Plot scale
XRANGE = 14000
YRANGE = 0.5

class PlotWindow(QWidget):
    def __init__(self,ch,parent=None):
        super().__init__(parent)
        
        self.ch = ch
        layout = QVBoxLayout(self)
        self.win=pg.GraphicsLayoutWidget(show=True)
        self.win.setBackground("#FFFFFF00")     
        layout.addWidget(self.win)
        
       

        self.plt = []
        self.curves = []
        

        for c in range(self.ch):
            plot=self.win.addPlot(row=c, col=0)
            plot.setXRange(0, XRANGE)
            plot.setYRange(-YRANGE,YRANGE)
            curve = plot.plot(pen=(c * 85, 0, 255 - c * 85))
            self.plt.append(plot)
            self.curves.append(curve)


        self.CHUNK = 40
        self.RATE = 2000


        self.timer = QtCore.QTimer()

        self.data = np.zeros((self.ch, 14000))
        self.current_column =0
        self.time = np.zeros(self.ch)

    def update(self,rawEMG):
        newdata = rawEMG.T * 1000
        if self.current_column + 40 > self.data.shape[1]:
            self.data = np.roll(self.data, -40, axis=1)
            self.current_column = self.data.data.shape[1] - 40
        self.data[:, self.current_column:self.current_column + 40] = newdata
        self.current_column += 40

        for c in range(self.ch):
            if self.current_column >14000:
                start_col = self.current_column - 14000
                self.curves[c].setData(self.data[c, start_col:self.current_column])
            else:
                self.curves[c].setData(self.data[c, :self.current_column])

       
    
    def reset(self, flag):
        if not flag:
        # Clear existing plots
            self.win.clear()  # Clears the entire GraphicsLayoutWidget

            self.plt = []
            self.curves = []
            self.data = np.zeros((self.ch, 14000))

        # Re-add plots
            for c in range(self.ch):
                plot = self.win.addPlot(row=c, col=0)
                plot.setXRange(0, XRANGE)
                plot.setYRange(-YRANGE, YRANGE)
                curve = plot.plot(pen=(c * 85, 0, 255 - c * 85))
                self.plt.append(plot)
                self.curves.append(curve)
            self.data = np.zeros((self.ch, 14000))
            self.current_column =0
            self.time = np.zeros(self.ch)
    
