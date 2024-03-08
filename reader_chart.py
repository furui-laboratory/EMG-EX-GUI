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
from src.delsys import DataHandle
from scipy import signal
# from src.delsys2 import DataHandle
# from get_emg_max import GetMaxEmg


class RaderChartWindow(QWidget):

    # def __init__(self,dh,number_electrode,maxemg):
    def __init__(self,ch_num,parent=None):
        super().__init__(parent)
        self.radius = 400
        '''仮で最大値を1としているが、実際は最大値を取得するプログラムを下記に記載する'''
        self.maximum_emg = [0.0001 for i in range(ch_num)]
        self.number = ch_num
        self.rcData = [0 for i in range(self.number)] 
        # self.initUI()
        # self.dh = dh
        # self.dh.initialize_delsys()
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.updatePaintEvent)
        # self.timer.start(1)

        # self.show()


    def updatePaintEvent(self,rawEMG):
        ## PaintEvent内で筋電位信号のデータを取得しself.dataを更新する
       
        # rawRMG = self.dh.get_emg(mode='notch->rect->lpf')
        # self.rcData = np.mean(rawRMG,axis=0)*self.radius/self.maximum_emg
        '''EMGdataを整流平滑化するプログラムを下記に記載する'''
        proceed = DataHandle(n_channels=self.number)
        rectifiedEMG = proceed._get_notched_rectified_lpf_emg(rawEMG)
        """シミュレーション実験"""
        self.rcData =  np.mean(rectifiedEMG,axis=0)*self.radius/self.maximum_emg
        # print(f'rectifiedEMG : {self.rcData}')
        self.update()

    # def get_motion1(self):

    #     self.motion1_data = self.rcData
    #     print(self.motion1_data)

    # def get_motion2(self):
    #     self.motion2_data = self.rcData
    #     print(self.motion2_data)

    # def display_combined_motion(self):
    
    #     self.combined_data = (self.motion1_data + self.motion2_data)/2
    #     self.update()

    # def reset(self):
    #     self.motion1_data = None
    #     self.motion2_data = None
    #     self.combined_data = None



    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # 描画開始(何よりもまず始める)
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
        # print(qpoints_label)
        for i in range(self.number):
            painter.drawText(qpoints_label[i], f'{i+1}')


        # 特徴量の描画
        # ------------
        # self.rcData_max = max(self.rcData)
        # self.rcData_normarized = [val/self.rcData_max for val in self.rcData]
       
        '''特徴量の描画'''
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)

        # P = [QtCore.QPointF(self.rcData_normarized[i]*20 * np.cos(2. * np.pi / self.number * i),self.rcData_normarized[i]*20 * np.sin(2. * np.pi / self.number * i)) for i in
        #           range(0, self.number)]
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
        

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = RaderChartWindow()
#     sys.exit(app.exec_())