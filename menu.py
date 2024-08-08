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
from menu_emgonlineplot import WindowPlotOnlineEMG
from get_max_emg import GetMaxEMG
from classification.classification_menu import Classification_Menu

class Menu(QWidget):

    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)

        self.button_setting = QPushButton('設定',self)
        self.button_online_emgplot = QPushButton('リアルタイム生波形表示',self)
        self.button_emgmax = QPushButton('最大値EMG取得',self)
        self.button_readerchart = QPushButton('レーダーチャート',self)
        self.button_get_emg = QPushButton('EMG取得',self)
        self.button_demo = QPushButton('機械学習デモ',self)

        self.initUI()

        self.settingWindow = Setting()
        self.settingWindow.send_data()

        self.saveemg_setting = GetEMGSetting()
        self.rader_chartwindow = Mixupshow()
        self.plot_window = WindowPlotOnlineEMG()
        self.savemaxemgWindow = GetMaxEMG()
        self.classification_menu = Classification_Menu()

        

        # 設定ボタンが押された時の処理
        self.button_setting.clicked.connect(self.hidewindow_setting)
        # 遷移先である設定画面の戻るボタンが押された時の処理
        self.settingWindow.back_button.clicked.connect(self.showwindow_setting)
        
        # 取得ボタンが押された時の処理
        self.button_get_emg.clicked.connect(self.hidewindow_getemg)
        # 遷移先である取得準備画面の戻るボタンが押された時の処理
        self.saveemg_setting.button_back.clicked.connect(self.showwindow_getemg)

        # レーダーチャートボタンが押された時の処理
        self.button_readerchart.clicked.connect(self.hidewindow_readerchart)
        # 遷移先であるレーダーチャートの戻るボタンが押された時の処理
        self.rader_chartwindow.button_back.clicked.connect(self.showwindow_readerchart)
        
        # リアルタイム生波形表示ボタンが押された時の処理
        self.button_online_emgplot.clicked.connect(self.hidewindow_plot_emg)
        # 遷移先であるリアルタイム生波形表示の戻るボタンが押された時の処理
        self.plot_window.button_back.clicked.connect(self.showwindow_plot_emg)

        # 最大値EMG取得ボタンが押された時の処理
        self.button_emgmax.clicked.connect(self.hidewindow_emgmax)
        # 遷移先である最大値EMG取得の戻るボタンが押された時の処理
        self.savemaxemgWindow.back_button.clicked.connect(self.showwindow_emgmax)

        # 機械学習デモボタンが押された時の処理
        self.button_demo.clicked.connect(self.hidewindow_classification)
        # 遷移先である機械学習デモの戻るボタンが押された時の処理
        self.classification_menu.button_back.clicked.connect(self.showwindow_classification)


    def hidewindow_plot_emg(self):
        # ch,_,_,_,_,_ = self.settingWindow.send_data()
        # self.plot_window.set_parameter(ch)
        self.plot_window.start()
        self.plot_window.show()
        self.hide()

    # 取得準備画面を表示
    def hidewindow_getemg(self):
        self.saveemg_setting.show()
        self.hide()

    # 現在表示されているメニュー画面を非表示にして、設定画面を表示
    def hidewindow_setting(self):
        self.settingWindow.show()
        self.hide()

    def hidewindow_readerchart(self):
        # ch,_,_,_,_,_ = self.settingWindow.send_data()
        # self.rader_chartwindow.set_parameter(ch)
        self.rader_chartwindow.start()
        self.rader_chartwindow.show()
        self.hide()

    def hidewindow_emgmax(self):
        self.savemaxemgWindow.start()
        self.savemaxemgWindow.show()
        self.hide()

    def hidewindow_classification(self):
        self.classification_menu.show()
        self.hide()
    
    # 設定画面を表示させて、メニュー画面を非表示にする
    def showwindow_setting(self):
        self.show()
        self.settingWindow.close()
    
    def showwindow_getemg(self):
        self.show()
        self.saveemg_setting.close()
    
    def showwindow_readerchart(self):
        self.show()
        self.rader_chartwindow.close()
 

    def showwindow_plot_emg(self):
        self.show()
        # self.plot_window.hide()
        self.plot_window.close()
    
    def showwindow_emgmax(self):
        self.show()
        self.savemaxemgWindow.close()

    def showwindow_classification(self):
        self.show()
        self.classification_menu.close()

       
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
        self.button_demo.setFont(font)


        self.button_setting.setGeometry(710,100,500,100)
        self.button_online_emgplot.setGeometry(710,250,500,100)
        self.button_emgmax.setGeometry(710,400,500,100)
        self.button_readerchart.setGeometry(710,550,500,100)
        self.button_get_emg.setGeometry(710,700,500,100)
        self.button_demo.setGeometry(710,850,500,100)

        # self.setLayout(vertical_layout)
        
      

def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Menu()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()