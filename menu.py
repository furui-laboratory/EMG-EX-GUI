import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
import time
from EMGsignal import EMGsignal
from reader_chart import RaderChartWindow
from progress import Progress
from picture import ImageSlider
from src.delsys import DataHandle
import pandas as pd
from plot_emg import PlotWindow

class Menu(QWidget):

    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()

        
       
    def initUI(self):
        self.setWindowTitle("menu")
        self.setGeometry(0,0,1920,1080)

        self.button_setting = QPushButton('設定',self)
        self.button_online_emgplot = QPushButton('リアルタイム生波形表示',self)
        self.button_emgmax = QPushButton('最大値EMG取得',self)
        self.button_readerchart = QPushButton('レーダーチャート',self)
        self.button_get_emg = QPushButton('EMG取得',self)

        # self.button_style = self.pushButtonWidgetStyle(height = '100px', width = '90px', color = 'red', font = '30px',borderColor = 'gray',
        #                                        borderRadius = '6px')
        # self.button_setting.setStyleSheet(self.button_style)

        self.button_setting.setStyleSheet('QPushButton {background-color: gray; \
                                        height: 150px; \
                                        color: black; \
                                        font: 50px; \
                                        border-radius: 30px;} \
                                        QPushButton:pressed {background: blue;}')
        self.button_online_emgplot.setStyleSheet('QPushButton {background-color: gray; \
                                        height: 150px; \
                                        color: black; \
                                        font: 50px; \
                                        border-radius: 30px;} \
                                        QPushButton:pressed {background: blue;}')
        self.button_emgmax.setStyleSheet('QPushButton {background-color: gray; \
                                        height: 150px; \
                                        color: black; \
                                        font: 50px; \
                                        border-radius: 30px;} \
                                        QPushButton:pressed {background: blue;}')
        self.button_readerchart.setStyleSheet('QPushButton {background-color: gray; \
                                        height: 150px; \
                                        color: black; \
                                        font: 50px; \
                                        border-radius: 30px;} \
                                        QPushButton:pressed {background: blue;}')
        self.button_get_emg.setStyleSheet('QPushButton {background-color: gray; \
                                        height: 150px; \
                                        color: black; \
                                        font: 50px; \
                                        border-radius: 30px;} \
                                        QPushButton:pressed {background: blue;}')
       

        vertical_layout = QVBoxLayout()
    
        vertical_layout.addWidget(self.button_setting)
        vertical_layout.addWidget(self.button_online_emgplot)
        vertical_layout.addWidget(self.button_emgmax)
        vertical_layout.addWidget(self.button_readerchart)
        vertical_layout.addWidget(self.button_get_emg)

        self.setLayout(vertical_layout)
        
      

def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Menu()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()