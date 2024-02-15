import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel,QTextEdit,QGridLayout
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

class Setting(QWidget):

    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)
        self.sub_num = QPushButton('被験者数',self)
        self.electrode_num = QPushButton('電極数',self)
        self.trial_num = QPushButton('試行数',self)
        self.time = QPushButton('動作数',self)
        self.m_time = QPushButton('計測時間',self)
        self.rest_time = QPushButton('休憩時間',self)
        self.back = QPushButton('戻る',self)
        self.initUI()


        
       
    def initUI(self):
        self.setWindowTitle("menu")
        self.setGeometry(0,0,1920,1080)


        self.sub_num.setFixedSize(900, 80)
        self.electrode_num.setFixedSize(900, 80)
        self.trial_num.setFixedSize(900, 80)
        self.time.setFixedSize(900, 80)
        self.m_time.setFixedSize(900, 80)
        self.rest_time.setFixedSize(900, 80)
        self.back.setFixedSize(900, 80)


        self.image_path = QTextEdit(self)
        self.image_path.setFixedSize(1800, 40)
        self.image_path.setPlaceholderText("表示する動作画像フォルダのパスを入力")
        self.save_path = QTextEdit(self)
        self.save_path.setFixedSize(1800, 40)

        self.save_path.setPlaceholderText("取得データを保存するフォルダのパスを入力")


        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.sub_num, 0, 0)
        self.grid_layout.addWidget(self.electrode_num, 0, 1)
        self.grid_layout.addWidget(self.trial_num, 1, 0)
        self.grid_layout.addWidget(self.time, 1, 1)
        self.grid_layout.addWidget(self.m_time, 2, 0)
        self.grid_layout.addWidget(self.rest_time, 2, 1)

       
        


        # self.vertical_layout = QVBoxLayout()
        # self.vertical_layout.addWidget(self.image_path,)
        # self.vertical_layout.addWidget(self.save_path,)
        # self.vertical_layout.addWidget(self.back)

        self.image_path.setGeometry(10,10,100,100)


    

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.grid_layout)
        # self.main_layout.addLayout(self.vertical_layout)

        self.setLayout(self.main_layout)

        
      

def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Setting()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()