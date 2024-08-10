from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication,QLabel,QWidget,QVBoxLayout,QTextEdit
import sys
from src.delsys import DataHandle
import configparser
from PyQt5.QtCore import Qt, pyqtSignal
from scipy import signal



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
        self.order_lpf = 2
        self.low_cut_lpf = 2
        layout = QVBoxLayout(self)
        self.win=pg.GraphicsLayoutWidget(show=True)
        self.win.setBackground("#FFFFFF00")     
        layout.addWidget(self.win)
        

        self.plt = []
        for c in range(self.ch):
            self.plt.append(self.win.addPlot(rowSpan=1))
            self.win.nextRow()

        for c in range(self.ch):
            self.plt[c].setXRange(0, XRANGE)
            self.plt[c].setYRange(-YRANGE,YRANGE)


        self.CHUNK = 40
        self.RATE = 2000

        self.dh = DataHandle(self.ch)
        self.dh.initialize_delsys()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getEMG)
        self.timer.start(1)

        self.data = np.zeros((self.ch, self.CHUNK))

        self.curves = [[] for i in range(self.ch)]
        self.time = np.zeros(self.ch)

        # False : 生波形
        # True : 整流平滑化波形
        self.state = False

        self.initial_lpf(self.order_lpf,self.low_cut_lpf)
        

    def change_state_raw(self):
        self.state = False
    
    def change_state_lpfreflected(self):
        self.state = True
    
    def update_lpw_parametar(self,order,low_cut_lpf):
        self.order_lpf = order
        self.low_cut_lpf = low_cut_lpf
        self.initial_lpf(self.order_lpf,self.low_cut_lpf)


    def getEMG(self):
        if self.state:
            rawEMG = self.dh.get_emg()
            processedEMG = self.rectified_lpf_emg(rawEMG)
        else:
            processedEMG = self.dh.get_emg()
        self.update(processedEMG)

    def update(self,rawEMG):
        for c in range(self.ch):
            self.data = rawEMG[:, c] * 1000
            self.curve = self.plt[c].plot(pen={"color": "r", "width": 1})
            self.curves[c].append(self.curve)
            self.curve = self.curves[c][-1]
            self.curve.setData(np.arange(self.time[c], self.time[c] + 40), self.data)
            self.time[c] += 40

            if self.time[c] > 14000:
                self.plt[c].clear()
                self.curves[c] = []
                self.time[c] = 0

    

    def initial_lpf(self,order,low_cut_lpf):
        """Initialization for the low-pass filter
            """
        # Nyquist frequency
        nyq = (self.dh.fs / 2)

        w = low_cut_lpf / nyq

        self.b_lpf, self.a_lpf = signal.butter(order, w, "low")
        self.z_lpf = np.zeros((max(len(self.a_lpf), len(self.b_lpf)) - 1, 
                                self.ch))

    def _lpf(self, data):
        """Applying the low-pass filter
        """
        processedEMG, self.z_lpf = \
                signal.lfilter(self.b_lpf, self.a_lpf, data, axis=0, 
                               zi=self.z_lpf)
        return processedEMG
    
    def rectified_lpf_emg(self, rawEMG):
        """Get rectified EMG
        """
        rectifiedEMG = np.abs(rawEMG)
        return self._lpf(rectifiedEMG)
    
class WindowPlotOnlineEMG(QWidget):
    closed = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
        
        self.label = QLabel('生波形', self)
        self.lable_lpfinfo = QLabel('', self)
        self.button_raw = QPushButton('生波形',self)
        self.button_lpfreflected = QPushButton('整流平滑化',self)
        self.button_back = QPushButton('戻る',self)
        self.label_order = QLabel('次数:', self)
        self.label_passband = QLabel('通過帯域:', self)
        self.button_adaptation = QPushButton('適応',self)
        self.text_order = QTextEdit('2',self)
        self.text_passband = QTextEdit('2',self)  
        self.label.setAlignment(Qt.AlignCenter)
        self.button_back.clicked.connect(self.close)
   
    
    def start(self):
        config = configparser.ConfigParser()
        config.read('./setting.ini')
        self.ch = config['settings'].getint('ch')
        self.plotEMG = PlotOnlineEMG(self.ch,self)
        self.initUI()


    def initUI(self):
        self.setGeometry(0,0,1920,1080)
        self.label.setAlignment(Qt.AlignCenter)
        self.lable_lpfinfo.setAlignment(Qt.AlignCenter)
        

        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_raw.setFont(font)
        self.button_lpfreflected.setFont(font)
        self.button_adaptation.setFont(font)
        self.button_back.setFont(font)
        self.label_order.setFont(font)
        self.label_passband.setFont(font)
        self.text_order.setFont(font)
        self.text_passband.setFont(font)
        self.lable_lpfinfo.setFont(font)
        font.setPointSize(40)
        self.label.setFont(font)

       
        self.plotEMG.setGeometry(100,10,900,900)
        self.label.setGeometry(1100,150,600,80)
        self.button_raw.setGeometry(1100,350,600,80)
        self.button_lpfreflected.setGeometry(1100,450,600,80)
        self.label_order.setGeometry(1180,550,200,80)
        self.text_order.setGeometry(1270,565,70,50)
        self.label_passband.setGeometry(1390,550,200,80)
        self.text_passband.setGeometry(1550,565,70,50)
        self.button_adaptation.setGeometry(1345,630,120,60)
        self.button_back.setGeometry(1100,750,600,80)
        self.lable_lpfinfo.setGeometry(1100,250,600,80)

        self.button_raw.clicked.connect(self.updatelabel_raw)
        self.button_lpfreflected.clicked.connect(self.updatelabel_lpfreflected)
        self.button_adaptation.clicked.connect(self.updatelabel_lpfinfo)
      
        self.text_order.hide()
        self.text_passband.hide()
        self.label_order.hide()
        self.label_passband.hide()
        self.lable_lpfinfo.hide()
        self.button_adaptation.hide()

    def updatelabel_raw(self):
        self.plotEMG.change_state_raw()
        self.label.setText('生波形')
        self.text_order.hide()
        self.text_passband.hide()
        self.label_order.hide()
        self.label_passband.hide()
        self.lable_lpfinfo.hide()
        self.button_adaptation.hide()

    def updatelabel_lpfreflected(self):
        self.plotEMG.change_state_lpfreflected()
        self.button_adaptation.show()
        self.text_order.show()
        self.text_passband.show()
        self.label_order.show()
        self.label_passband.show()
        self.lable_lpfinfo.show()
        self.label.setText(f'整流平滑化')

    def updatelabel_lpfinfo(self):
        if self.text_order.toPlainText().isdecimal():
            if self.text_passband.toPlainText().isdecimal():
                self.lable_lpfinfo.setText(f'次数:{self.text_order.toPlainText()} 通過帯域:{self.text_passband.toPlainText()}')

                self.plotEMG.update_lpw_parametar(int(self.text_order.toPlainText()),int(self.text_passband.toPlainText()))

    def closeEvent(self, event):
        print('before closed')
        self.plotEMG.timer.stop()
        self.plotEMG.dh.stop_delsys()
        self.plotEMG.close()
        self.closed.emit()
        event.accept()
        print('after close')

        
      

