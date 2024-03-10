from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QWidget,QDialog,QVBoxLayout,QLineEdit,QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QTimer
import random
from src.delsys2 import DataHandle
import configparser
import pandas as pd


# Screen size (pixels)
# WIDTH = 1536
# HEIGHT = 960


class RaderChartMixUpWindow(QWidget):

    def __init__(self,ch,parent=None):
        super().__init__(parent)
        self.radius = 400
        self.number = ch
        self.maximum_emg = np.loadtxt('./max_emg_data/max_data.csv',delimiter=',').tolist()
        self.rcData = [0 for i in range(self.number)] 
        self.dh = DataHandle(self.number)
        self.dh.initialize_delsys()
        # self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePaintEvent)
        self.timer.start(1) 
        self.combined_data = [0 for i in range(self.number)]


    # def initUI(self):
    #     self.setGeometry(0,0,1920,1080)      


    def updatePaintEvent(self):
        ## PaintEvent内で筋電位信号のデータを取得しself.dataを更新する
       
        # rawRMG = self.dh.get_emg(mode='notch->rect->lpf')
        # self.rcData = np.mean(rawRMG,axis=0)*self.radius/self.maximum_emg
        '''EMGdataを整流平滑化するプログラムを下記に記載する'''
        rectifiedEMG = self.dh.get_emg(mode='notch->rect->lpf')
        pd.DataFrame(rectifiedEMG).to_csv(f'rectifiedEMG.csv', mode='a', index = False, header=False)

        """シミュレーション実験"""
        self.rcData =  np.mean(rectifiedEMG,axis=0)*self.radius/self.maximum_emg
        # print(f'rectifiedEMG : {self.rcData}')
        self.update()


    def get_motion1(self):
        self.motion1_data = self.rcData
        print(self.motion1_data)

    def get_motion2(self):
        self.motion2_data = self.rcData
        print(self.motion2_data)

    def display_combined_motion(self):
        self.combined_data = (self.motion1_data + self.motion2_data)/2
        self.update()


    def reset(self):
        self.motion1_data = None
        self.motion2_data = None
        self.combined_data = None


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # 描画開始(何よりもまず始める)
        # レンダリング時のアンチエイリアスの指定

        # Penの生成
        pen = QtGui.QPen()
        # 軸色の設定
        pen.setColor(QtCore.Qt.black)
        # 軸の太さの設定
        pen.setWidth(1)

        painter.setPen(pen)

        # 座標中心の移動
        painter.translate(self.width() / 2, self.height() / 2)
        
        point_zero = QtCore.QPoint(0, 0)


        qpoints = [QtCore.QPointF(self.radius * np.cos(2. * np.pi / self.number * i),self.radius * np.sin(2. * np.pi / self.number * i)) for i in range(0, self.number)]
        qpoints_label = [QtCore.QPointF((self.radius+30) * np.cos(2. * np.pi / self.number * i),(self.radius+30) * np.sin(2. * np.pi / self.number * i)) for i in range(0, self.number)]
        
        # print(qpoints_label)
        for i in range(self.number):
            painter.drawText(qpoints_label[i], f'{i+1}')

        
        
        poly = QtGui.QPolygonF(qpoints)
        painter.drawPolygon(poly)
        for i, v in enumerate(qpoints):
            painter.drawLine(point_zero, v)


        # 特徴量の描画
        # ------------
        # self.rcData_max = max(self.rcData)
        # self.rcData_normarized = [val/self.rcData_max for val in self.rcData]
       

        pen.setColor(QtCore.Qt.blue)
        pen.setWidth(5)
        painter.setPen(pen)

        # P = [QtCore.QPointF(self.rcData_normarized[i]*20 * np.cos(2. * np.pi / self.number * i),self.rcData_normarized[i]*20 * np.sin(2. * np.pi / self.number * i)) for i in
        #           range(0, self.number)]
        P = [QtCore.QPointF(self.rcData[i] * np.cos(2. * np.pi / self.number * i),self.rcData[i] * np.sin(2. * np.pi / self.number * i)) for i in
                  range(0, self.number)]

        poly2 = QtGui.QPolygonF(P)
        painter.drawPolygon(poly2)


        # drawing the combined data
        if np.sum(self.combined_data) != None:
            pen.setColor(QtCore.Qt.red)
            pen.setWidth(5)
            painter.setPen(pen)
            P_combined = [QtCore.QPointF(self.combined_data[i] * np.cos(2. * np.pi / self.number * i),self.combined_data[i] * np.sin(2. * np.pi / self.number * i)) for i in
                    range(0, self.number)]
            poly_combined = QtGui.QPolygonF(P_combined)
            painter.drawPolygon(poly_combined)
            # painter.end()

        painter.end()


class Mixupshow(QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)
        config = configparser.ConfigParser()
        config.read('./setting.ini')
        self.ch = config['settings'].getint('ch')
        self.acquisition_motion1 = QPushButton('Acquisition of motion 1',self)
        self.acquisition_motion2 = QPushButton('Acquisition of motion 2',self)
        self.display_combined_motion = QPushButton('Display combined motion',self)
        self.reset_button = QPushButton('Reset',self)
        self.button_back = QPushButton('Back',self)
        # self.chart_widget = RaderChartMixUpWindow(self.ch,self)
        # self.initUI()

    def start(self):
        self.chart_widget = RaderChartMixUpWindow(self.ch,self)
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0,0,1920,1080)

        font = QtGui.QFont()
        font.setPointSize(20)
        self.acquisition_motion1.setFont(font)
        self.acquisition_motion2.setFont(font)
        self.display_combined_motion.setFont(font)
        self.reset_button.setFont(font)
        self.button_back.setFont(font)
  
        # layout = QVBoxLayout()

        self.chart_widget.setGeometry(100,10,900,900)
        self.acquisition_motion1.setGeometry(1100,250,600,80)
        self.acquisition_motion2.setGeometry(1100,350,600,80)
        self.display_combined_motion.setGeometry(1100,450,600,80)
        self.reset_button.setGeometry(1100,550,600,80)
        self.button_back.setGeometry(1100,800,600,80)

        self.acquisition_motion1.clicked.connect(self.chart_widget.get_motion1)
        self.acquisition_motion2.clicked.connect(self.chart_widget.get_motion2)
        self.display_combined_motion.clicked.connect(self.chart_widget.display_combined_motion)
        self.reset_button.clicked.connect(self.chart_widget.reset)
        self.button_back.clicked.connect(self.close)
    
    # def close(self):
    #     self.hide()
    #     self.chart_widget.timer.stop()
    #     self.chart_widget.dh.stop_delsys()

        
      

# def main():
#     """メイン関数"""
#     app = QApplication(sys.argv)
#     mv = Mixupshow()
#     mv.set_parameter(3)
#     mv.show()
#     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()        

