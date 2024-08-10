import sys
from PyQt5.QtCore import QTimer
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel,QTextEdit,QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtTest
from PyQt5 import QtGui
import pandas as pd
from plot_emg import PlotWindow
from src.delsys2 import DataHandle
# from menu import Menu
import configparser
import numpy as np
import shutil
import os

class GetMaxEMG(QWidget):
    closed = pyqtSignal()
    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)

        self.back_button = QPushButton('終了',self)
        self.getEMG_button = QPushButton('EMG取得',self)
        self.label_state = QLabel('Are you ready ?',self)
       

        self.back_button.clicked.connect(self.save_max_emg)
        self.getEMG_button.clicked.connect(self.start_get_emg)

    def getEMG(self):
        # 整流平滑化データ取得
        rectifiedEMG = self.dh.get_emg(mode='notch->rect->lpf')
        # データを保存
        pd.DataFrame(rectifiedEMG).to_csv(f'./max_emg_data/calibration_data.csv', mode='a', index = False, header=False)
        

    def initUI(self):
        self.setWindowTitle("Get Max EMG")
        self.setGeometry(0,0,1920,1080)

        font = QtGui.QFont()
        font.setPointSize(20)
        self.back_button.setFont(font)
        self.getEMG_button.setFont(font)
        font.setPointSize(50)
        self.label_state.setFont(font)

        self.back_button.setGeometry(710,800,500,100)
        self.getEMG_button.setGeometry(710,650,500,100)
        self.label_state.setGeometry(520,400,1000,80)
        self.label_state.setAlignment(Qt.AlignCenter)

    def save_max_emg(self):
        data = np.loadtxt('./max_emg_data/calibration_data.csv',delimiter=',')
        np.savetxt('./max_emg_data/max_data.csv',np.max(data,axis=0))
        self.close()

        
    def start_get_emg(self):
        self.label_state.setText('最大値EMG取得中…')
        self.dh = DataHandle(self.ch)
        self.dh.initialize_delsys()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getEMG)
        self.timer.start(1)

    def start(self):
        shutil.rmtree('./max_emg_data/')
        os.mkdir('./max_emg_data')
        config = configparser.ConfigParser()
        config.read('./setting.ini')
        self.ch = config['settings'].getint('ch')
        self.initUI()
 

    def closeEvent(self, event):
        print('before closed')
        self.timer.stop()
        self.dh.stop_delsys()
        self.closed.emit()
        event.accept()
        print('after close')



        