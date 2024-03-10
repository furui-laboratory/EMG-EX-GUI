import sys
sys.path.append('..')
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtTest
from PyQt5.QtGui import QFont
import pandas as pd
import numpy as np
import statistics
from EMGsignal import EMGsignal
from progress import Progress
from picture import ImageSlider
from src.delsys2 import DataHandle
from reader_chart import RaderChartWindow
from probability_window import ProbabilityWindow



class PredictionWindow(QWidget):
    def __init__(self,ch,class_n,parent=None):
        super().__init__(parent)
        self.m = np.loadtxt('./parameter/mu.csv')
        self.sigma = np.loadtxt('./parameter/sigma.csv')
        self.ch = ch
        self.class_n = class_n
        self.name_label = ['グー','チョキ','パー']
        self.prediction_class_label = QLabel(self)
        self.reader_chart = RaderChartWindow(self.class_n,self)
        self.bar_graph = ProbabilityWindow(self.class_n,self)
        # delsys初期化
        self.dh = DataHandle(self.ch)
        self.dh.initialize_delsys()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getEMG)
        self.timer.start(1) 
        
    
    def initUI(self):
        self.setGeometry(0,0,1920,1080)
        self.reader_chart.setGeometry(780, 10, 900, 900)
        self.bar_graph.setGeometry(350, 10, 900, 900)

    
    def closeEvent(self, event):
        # ウィンドウが閉じられたときにシグナルを送信
        self.dh.stop_delsys()
        self.closed.emit()
        event.accept()
  

    def getEMG(self):
        # 整流平滑化データ取得
        rectifiedEMG = self.dh.get_emg(mode='notch->rect->lpf')
        # レーダーチャートをアップデート
        self.reader_chart.updatePaintEvent(rectifiedEMG)
        # 予測確率と予測クラスを取得
        prb = self.prediction(rectifiedEMG)
        # 棒グラフをアップデート
        self.bar_graph.update(prb)
        # 予測クラスを取得
        self.prediction_class=statistics.mode(np.argmax(prb,axis=1))
        # 予測ラベルを更新する
        self.prediction_class_label.setText(self.name_label[self.prediction_class])
        self.prediction_class_label.setAlignment(Qt.AlignCenter)
        
        


    def prediction(self,data):
        n_data = len(data)
        g = np.empty((n_data, self.class_n))

        # テストデータに対する識別関数値の計算 & クラス予測
        prior = 1. / self.class_n
        for c in range(self.class_n):
            g[:, c] = self._gaussian_discriminant_function(data, self.m[c], self.sigma, prior)+10000

        g /= np.sum(g, axis=1, keepdims=True)

        return g


    def _gaussian_discriminant_function(self, X, mu_each, sigma_each, prior):
        """クラスごとにガウス分布識別関数を計算
        """
        centered_X = X.T - mu_each.reshape(-1,1)
        # quad = np.sum(centered_X * (np.dot(np.linalg.pinv(sigma_each), centered_X)), axis = 0)
        quad = np.sum(centered_X * (np.dot(np.linalg.inv(sigma_each), centered_X)), axis = 0)
        log_pro = (-1/2)*(quad + np.log(np.linalg.det(sigma_each)) - 2 * np.log(prior))

        return np.exp(log_pro)