import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel,QCheckBox,QButtonGroup
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
from PyQt5 import QtGui
import time
from EMGsignal import EMGsignal
from reader_chart import RaderChartWindow
from progress import Progress
from picture import ImageSlider
from src.delsys import DataHandle
import pandas as pd
from plot_emg import PlotWindow
from setting import Setting

class GetEMGSetting(QWidget):

    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)

        self.label_get_style = QLabel('取得方法',self)
        self.check_sequential = QCheckBox('全試行連続で取得',self)
        self.check_each = QCheckBox('各試行ごとに取得',self)
        self.lable_display_style = QLabel('表示項目',self)
        self.check_reader_chart = QCheckBox('レーダーチャートを表示する',self)
        self.check_emg_plot = QCheckBox('EMGプロットを表示する',self)
        self.button_start = QPushButton('計測開始',self)
        self.button_back = QPushButton('戻る',self)

        self.initUI()

    def set_parameter(self,ch,class_n,trial_n,sec_mes,sec_class_break,sec_trial_break):
        self.ch = ch
        self.class_n = class_n
        self.trial_n = trial_n
        self.sec_mes = sec_mes
        self.sec_class_break = sec_class_break
        self.sec_trial_break = sec_trial_break


       
    def initUI(self):
        self.setWindowTitle("menu")
        self.setGeometry(0,0,1920,1080)

        self.check_sequential.setChecked(True)
        self.check_reader_chart.setChecked(True)

        self.group_measurment = QButtonGroup()
        self.group_display = QButtonGroup()
        self.group_measurment.addButton(self.check_sequential)
        self.group_measurment.addButton(self.check_each)
        self.group_display.addButton(self.check_reader_chart)
        self.group_display.addButton(self.check_emg_plot)


        font = QtGui.QFont()
        font.setPointSize(20)
        self.check_sequential.setFont(font)
        self.check_each.setFont(font)
        self.check_reader_chart.setFont(font)
        self.check_emg_plot.setFont(font)
        self.button_start.setFont(font)
        self.button_back.setFont(font)
        self.label_get_style.setFont(font)
        self.lable_display_style.setFont(font)

        self.label_get_style.setGeometry(530,100,500,100)
        self.lable_display_style.setGeometry(530,400,500,100)
        self.check_sequential.setGeometry(530,200,500,100)
        self.check_each.setGeometry(1100,200,500,100)
        self.check_reader_chart.setGeometry(530,500,500,100)
        self.check_emg_plot.setGeometry(1100,500,500,100)
        self.button_start.setGeometry(880,700,250,80)
        self.button_back.setGeometry(880,800,250,80)

        # self.setLayout(vertical_layout)
        
      

def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = GetEMGSetting()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()