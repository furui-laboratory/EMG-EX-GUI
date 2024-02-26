from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication,QLabel,QWidget,QVBoxLayout
import sys
from src.delsys import DataHandle
from PyQt5.QtCore import Qt


# Screen size (pixels)
WIDTH = 1536
HEIGHT = 960

# Plot scale
XRANGE = 14000
YRANGE = 0.5

class PlotOnlineEMG(QWidget):
    def __init__(self,ch,parent=None):
        super().__init__(parent)
        
        self.ch = ch
        layout = QVBoxLayout(self)
        self.win=pg.GraphicsLayoutWidget(show=True)
        self.win.setBackground("#FFFFFF00")     
        layout.addWidget(self.win)
        
       
        # self.win.resize(WIDTH, HEIGHT)
        # self.win.move(0, 0)
        self.plt = []
        for c in range(self.ch):
            self.plt.append(self.win.addPlot(rowSpan=1))
            self.win.nextRow()

        for c in range(self.ch):
            self.plt[c].setXRange(0, XRANGE)
            self.plt[c].setYRange(-YRANGE,YRANGE)


        self.CHUNK = 40
        self.RATE = 2000

        # self.dh = DataHandle(self.ch)
        # self.dh.initialize_delsys()

        self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(0.1)

        self.data = np.zeros((self.ch, self.CHUNK))

        self.curves = [[] for i in range(self.ch)]
        self.time = np.zeros(self.ch)

    def update(self,rawEMG):
        for c in range(self.ch):
            self.data = rawEMG[:, c] * 1000
            self.curve = self.plt[c].plot(pen="y")
            self.curves[c].append(self.curve)
            self.curve = self.curves[c][-1]
            self.curve.setData(np.arange(self.time[c], self.time[c] + 40), self.data)
            self.time[c] += 40

            # if self.time[c] > 14000:
            #     self.plt[c].clear()
            #     self.curves[c] = []
            #     self.time[c] = 0
    
    def reset(self,flag):
        if flag==False:
            for c in range(self.ch):
                self.plt[c].clear()
                self.curves[c] = []
                self.time[c] = 0

    

class WindowPlotOnlineEMG(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.label = QLabel('生波形', self)
        self.button_raw = QPushButton('生波形',self)
        self.button_reflected = QPushButton('整流化＋平滑化',self)
        self.button_lpf = QPushButton('平滑化',self)
        self.button_back = QPushButton('戻る',self)
        
        self.label.setAlignment(Qt.AlignCenter)
        

    # maxemgを将来的に設定
    def set_parameter(self,number_electrode):
        self.plotEMG = PlotOnlineEMG(number_electrode,self)
        self.initUI()

    def initUI(self):
        self.setGeometry(0,0,1920,1080)
        self.label.setAlignment(Qt.AlignCenter)
        

        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_raw.setFont(font)
        self.button_reflected.setFont(font)
        self.button_lpf.setFont(font)
        self.button_back.setFont(font)
        font.setPointSize(40)
        self.label.setFont(font)
        # layout = QVBoxLayout()

       
        self.plotEMG.setGeometry(100,10,900,900)
        self.label.setGeometry(1100,200,600,80)
        self.button_raw.setGeometry(1100,350,600,80)
        self.button_reflected.setGeometry(1100,450,600,80)
        self.button_lpf.setGeometry(1100,550,600,80)
        self.button_back.setGeometry(1100,650,600,80)

        self.button_raw.clicked.connect(self.updatelabel_raw)
        self.button_reflected.clicked.connect(self.updatelabel_reflected)
        self.button_lpf.clicked.connect(self.updatelabel_lpf)
        self.button_back.clicked.connect(self.close)
      

    def updatelabel_raw(self):
        self.label.setText('生波形')

    def updatelabel_reflected(self):
        self.label.setText('整流化＋平滑化')
    
    def updatelabel_lpf(self):
        self.label.setText('平滑化')



    # def close(self):
    #     self.hide()
    #     self.chart_widget.timer.stop()
    #     self.chart_widget.dh.stop_delsys()

        
      

def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = WindowPlotOnlineEMG()
    mv.set_parameter(3)
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()        

