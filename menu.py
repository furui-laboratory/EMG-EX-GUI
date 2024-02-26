import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
from PyQt5 import QtGui
import time
from EMGsignal import EMGsignal
from progress import Progress
from picture import ImageSlider
from src.delsys import DataHandle
import pandas as pd
from plot_emg import PlotWindow
from setting import Setting
from getemg_setting import GetEMGSetting
from raderchart_mixup import Mixupshow

class Menu(QWidget):

    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)

        self.button_setting = QPushButton('設定',self)
        self.button_online_emgplot = QPushButton('リアルタイム生波形表示',self)
        self.button_emgmax = QPushButton('最大値EMG取得',self)
        self.button_readerchart = QPushButton('レーダーチャート',self)
        self.button_get_emg = QPushButton('EMG取得',self)

        self.initUI()

        self.settingWindow = Setting()
        self.saveemg_setting = GetEMGSetting()
        self.rader_chartwindow = Mixupshow()

        # 設定ボタンが押された時の処理
        self.button_setting.clicked.connect(self.hidewindow_setting)
        self.settingWindow.back_button.clicked.connect(self.showwindow_setting)
        
        # 取得ボタンが押された時の処理
        self.button_get_emg.clicked.connect(self.hidewindow_getemg)
        # 遷移先である取得準備画面の戻るボタンが押された時の処理
        self.saveemg_setting.button_back.clicked.connect(self.showwindow_getemg)

        # レーダーチャートボタンが押された時の処理
        self.button_readerchart.clicked.connect(self.hidewindow_readerchart)
        self.rader_chartwindow.button_back.clicked.connect(self.showwindow_readerchart)
        

    # 取得準備画面を表示
    def hidewindow_getemg(self):
        # 設定画面からデータを取得する
        ch,class_n,trial_n,sec_mes,sec_class_break,sec_trial_break = self.settingWindow.send_data()
        self.saveemg_setting.set_parameter(ch,class_n,trial_n,sec_mes,sec_class_break,sec_trial_break)
        self.saveemg_setting.show()
        self.hide()


    def hidewindow_setting(self):
        self.settingWindow.show()
        self.hide()

    def hidewindow_readerchart(self):
        ch,_,_,_,_,_ = self.settingWindow.send_data()
        self.rader_chartwindow.set_parameter(ch)
        self.rader_chartwindow.show()
        self.hide()

    def showwindow_setting(self):
        self.show()
        ch,class_n,trial_n,sec_mes,sec_class_break,sec_trial_break = self.settingWindow.send_data()
        print(ch,class_n,trial_n,sec_mes,sec_class_break,sec_trial_break)
        self.settingWindow.hide()
    
    def showwindow_getemg(self):
        self.show()
        self.saveemg_setting.hide()
    
    def showwindow_readerchart(self):
        self.show()
        self.rader_chartwindow.hide()

       
    def initUI(self):
        self.setWindowTitle("menu")
        self.setGeometry(0,0,1920,1080)


        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_setting.setFont(font)
        self.button_online_emgplot.setFont(font)
        self.button_emgmax.setFont(font)
        self.button_readerchart.setFont(font)
        self.button_get_emg.setFont(font)

        # self.button_setting.setFixedSize(500,100)
        # self.button_online_emgplot.setFixedSize(500,100)
        # self.button_emgmax.setFixedSize(500,100)
        # self.button_readerchart.setFixedSize(500,100)
        # self.button_get_emg.setFixedSize(500,100)

       

        # vertical_layout = QVBoxLayout()
    
        # vertical_layout.addWidget(self.button_setting)
        # vertical_layout.addWidget(self.button_online_emgplot)
        # vertical_layout.addWidget(self.button_emgmax)
        # vertical_layout.addWidget(self.button_readerchart)
        # vertical_layout.addWidget(self.button_get_emg)

        # self.button_setting.setFixedSize(500,100)
        # self.button_online_emgplot.setFixedSize(500,100)
        # self.button_emgmax.setFixedSize(500,100)
        # self.button_readerchart.setFixedSize(500,100)
        # self.button_get_emg.setFixedSize(500,100)

        self.button_setting.setGeometry(710,200,500,100)
        self.button_online_emgplot.setGeometry(710,350,500,100)
        self.button_emgmax.setGeometry(710,500,500,100)
        self.button_readerchart.setGeometry(710,650,500,100)
        self.button_get_emg.setGeometry(710,800,500,100)

        # self.setLayout(vertical_layout)
        
      

def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Menu()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()