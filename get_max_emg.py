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
    def __init__(self,parent=None,dh=None):
        super().__init__(parent)
        self.dh = dh
        self.save_flag=0
        self.back_button = QPushButton('終了',self)
        self.getEMG_button = QPushButton('EMG取得',self)
        self.label_state = QLabel('Are you ready ?',self)
       

        self.back_button.clicked.connect(self.save_max_emg)
        self.getEMG_button.clicked.connect(self.start_get_emg)

    def getEMG(self):
        # 整流平滑化データ取得
        rectifiedEMG = self.dh.get_emg(mode='notchlpf')
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
        if self.save_flag==1:
            data = np.loadtxt('./max_emg_data/calibration_data.csv',delimiter=',')
            if data.ndim == 1:
                max_data = np.max(data)
                max_data = np.array([max_data])
            else:
                max_data = np.max(data, axis=0)
            np.savetxt('./max_emg_data/max_data.csv',max_data)
        
        self.close()
        

        
    def start_get_emg(self):
        try:
            shutil.rmtree('./max_emg_data/')
        except FileNotFoundError:
            pass  # ディレクトリが存在しない場合は無視
        os.mkdir('./max_emg_data')
        self.label_state.setText('最大値EMG取得中…')
        self.save_flag=1
        #self.dh = DataHandle(self.ch)
        #self.dh.initialize_delsys() # EMG信号の初期化
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getEMG)
        self.timer.start(1)

    def start(self):
        
        config = configparser.ConfigParser()
        config.read('./setting.ini')
        self.ch = config['settings'].getint('ch')
        self.initUI()
 

    def closeEvent(self, event):
        print('before closed')
        if hasattr(self, 'timer'):
            self.timer.stop()
        #self.dh.stop_delsys()
        self.closed.emit()
        self.deleteLater()  # ウィジェットを削除する準備をする
        event.accept()
        print('after close')



        