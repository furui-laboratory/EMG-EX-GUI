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

        # 設定ボタンが押された時の処理
        self.button_setting.clicked.connect(self.hidewindow_setting)
        # 設定画面の戻るボタンが押された時の処理
        self.settingWindow.back_button.clicked.connect(self.showwindow_setting)

        # 取得ボタンが押された時の処理
        self.button_get_emg.clicked.connect(self.hidewindow_getemg)

        # レーダーチャートボタンが押された時の処理
        self.button_readerchart.clicked.connect(self.hidewindow_readerchart)
    
        # リアルタイム生波形表示ボタンが押された時の処理
        self.button_online_emgplot.clicked.connect(self.hidewindow_plot_emg)

        # 最大値EMG取得ボタンが押された時の処理
        self.button_emgmax.clicked.connect(self.hidewindow_emgmax)

        # 機械学習デモボタンが押された時の処理
        self.button_demo.clicked.connect(self.hidewindow_classification)

    # リアルタイム生波形表示画面を表示
    def hidewindow_plot_emg(self):
        self.plot_window = WindowPlotOnlineEMG()
        self.plot_window.start()
        self.plot_window.show()
        self.hide()
        self.plot_window.closed.connect(self.show)

    # 取得準備画面を表示
    def hidewindow_getemg(self):
        self.saveemg_setting = GetEMGSetting()
        self.saveemg_setting.show()
        self.hide()
        self.saveemg_setting.closed.connect(self.show)

    # 現在表示されているメニュー画面を非表示にして、設定画面を表示
    def hidewindow_setting(self):
        self.settingWindow.show()
        self.hide()
    # 設定画面を表示させて、メニュー画面を非表示にする
    def showwindow_setting(self):
        self.show()
        self.settingWindow.close()

    # レーダーチャート画面を表示
    def hidewindow_readerchart(self):
        self.rader_chartwindow = Mixupshow()
        self.rader_chartwindow.start()
        self.rader_chartwindow.show()
        self.hide()
        self.rader_chartwindow.closed.connect(self.show)

    # 最大値EMG取得画面を表示
    def hidewindow_emgmax(self):
        self.savemaxemgWindow = GetMaxEMG()
        self.savemaxemgWindow.start()
        self.savemaxemgWindow.show()
        self.hide()
        self.savemaxemgWindow.closed.connect(self.show)

    # 機械学習デモ画面を表示
    def hidewindow_classification(self):
        self.classification_menu = Classification_Menu()
        self.classification_menu.show()
        self.hide()
        self.classification_menu.closed.connect(self.show)
    
   
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


def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Menu()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()