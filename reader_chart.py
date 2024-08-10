import sys
sys.path.append('..')
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QVBoxLayout,QLineEdit,QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QTimer
import random
from src.delsys2 import DataHandle
from scipy import signal
import pandas as pd



class RaderChartWindow(QWidget):


    def __init__(self,dh,ch_num,parent=None):
        super().__init__(parent)
        self.radius = 400
        self.dh = dh
        '''仮で最大値を1としているが、実際は最大値を取得するプログラムを下記に記載する'''
        self.maximum_emg = np.loadtxt('./max_emg_data/max_data.csv',delimiter=',').tolist()
        # print(self.maximum_emg)
        self.number = ch_num
        self.rcData = [0 for i in range(self.number)] 


    def updatePaintEvent(self,rawEMG):
        ## PaintEvent内で筋電位信号のデータを取得しself.dataを更新する
       

        '''EMGdataを整流平滑化するプログラムを下記に記載する'''
        rectifiedEMG = self.dh._get_notched_rectified_lpf_emg(rawEMG)
        """シミュレーション実験"""
        self.rcData =  np.mean(rectifiedEMG,axis=0)*self.radius/self.maximum_emg

        self.update()



    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # レンダリング時のアンチエイリアスの指定

        '''軸の描画'''
        # Penの生成
        pen = QtGui.QPen()
        # 軸色の設定
        pen.setColor(QtCore.Qt.black)
        # 軸の太さの設定
        pen.setWidth(3)
        painter.setPen(pen)
        # 座標中心の移動
        painter.translate(self.width() / 2, self.height() / 2)
        point_zero = QtCore.QPoint(0, 0)
        qpoints = [QtCore.QPointF(self.radius * np.cos(2. * np.pi / self.number * i),self.radius * np.sin(2. * np.pi / self.number * i)) for i in range(0, self.number)]
        poly = QtGui.QPolygonF(qpoints)
        painter.drawPolygon(poly)
        for i, v in enumerate(qpoints):
            painter.drawLine(point_zero, v)

        '''ラベルの描画'''
        qpoints_label = [QtCore.QPointF((self.radius+30) * np.cos(2. * np.pi / self.number * i),(self.radius+30) * np.sin(2. * np.pi / self.number * i)) for i in range(0, self.number)]
        font = QFont()
        font.setPointSize(20)
        painter.setFont(font) 
        for i in range(self.number):
            painter.drawText(qpoints_label[i], f'{i+1}')

       
        '''特徴量の描画'''
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)

      
        P = [QtCore.QPointF(self.rcData[i] * np.cos(2. * np.pi / self.number * i),self.rcData[i] * np.sin(2. * np.pi / self.number * i)) for i in
                  range(0, self.number)]

        poly2 = QtGui.QPolygonF(P)
        painter.drawPolygon(poly2)

        '''特徴量の塗りつぶし'''
        # QPainterPathオブジェクトを作成し、ポリゴンを追加
        path = QPainterPath()
        path.addPolygon(poly2)
        # ブラシを作成（ここでは赤色を使用）
        brush = QBrush(Qt.gray)
        # パスを塗りつぶす
        painter.fillPath(path, brush)
        # ポリゴンを描画
        painter.drawPolygon(poly2)
        painter.end()
        
