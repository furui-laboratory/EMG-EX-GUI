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

class MainWindow(QWidget):

    """メインウィンドウ"""
    def __init__(self):
        super().__init__()
        self.ch = 3
        # 試行数とクラス数の数値を定義
        self.trial_n = 2
        self.class_n = 2
        self.dh = DataHandle(self.ch)
        self.dh.initialize_delsys()
        # ラベルの初期化
        self.trial_ = 0
        self.class_ = 0
        # 現在の試行数とクラス数を求めるための変数
        self.tmp = 0    
        self.EMGsinal_object = EMGsignal(self.dh,self.trial_n,self.class_n,3,7,self)
        self.initUI()
        # self.reader_chart.hide()
        self.EMGsinal_object.timer.start()
        # 初期はBreakからスタートする
        self.EMGsinal_object.tick.connect(self.progress.handleTimer)
        # self.EMGsinal_object.tick.connect(self.view)
        # レーダーチャートの更新
        self.EMGsinal_object.array_signal.connect(self.reader_chart.updatePaintEvent)
        # EMGデータの保存
        self.EMGsinal_object.array_signal.connect(self.save_emg)
        # EMGのプロット
        self.EMGsinal_object.array_signal.connect(self.plot_emg.update)
        # プログレスバーの更新
        self.EMGsinal_object.finished_class.connect(self.progress.update_display)
        # ラベルの更新
        self.EMGsinal_object.finished_class.connect(self.update_label)
        # 画像の更新
        self.EMGsinal_object.finished_class.connect(self.image.next_image)
        # EMGプロットのリセット
        self.EMGsinal_object.finished_class.connect(self.plot_emg.reset)

       
    
    def initUI(self):
        self.setWindowTitle("計測中")
        self.setGeometry(0,0,1920,1080)        
      

        # self.central_widget = QWidget(self)
        # self.setCentralWidget(self.central_widget)
        # self.reader_chart.setGeometry(100, 100, 200, 25)

        self.reader_chart = RaderChartWindow(3,self)
        self.progress = Progress(7,3,self)
        self.image = ImageSlider(self)
        self.plot_emg = PlotWindow(self)
        # self.widget1 = QWidget()
        # self.layout1 = QHBoxLayout()
        # self.layout1.addWidget(self.reader_chart,4)
        # self.layout1.addWidget(self.image,1)
        # self.widget1.setLayout(self.layout1)


        # self.layout = QVBoxLayout(self)
        # self.layout.addWidget(self.widget1,4)
        # self.layout.addWidget(self.progress,1)
        # self.setLayout(self.layout)
       

        self.progress.setGeometry(230, 900, 1500, 1000)
        self.reader_chart.setGeometry(150, 10, 900, 900)
        self.image.setGeometry(1200, 10, 100, 100)
        self.plot_emg.setGeometry(1200, 600, 900, 900)


       
        # self.layout = QVBoxLayout(self)
        # self.layout.addWidget(self.reader_chart,4)
        # self.layout.addWidget(self.progress,1)
        # self.layout.setAlignment(self.reader_chart, Qt.AlignCenter)
        # self.layout.setAlignment(self.progress, Qt.AlignCenter)
    
        # self.progress.setGeometry(160, 90, 300, 30)
        # self.progress.move(100, 100)  # 新しい位置
        #self.progress.resize(500, 500)
    
    # def change_widget(self,flag):
    #     if flag:
    #         self.reader_chart.show()
    #     else:
    #         self.reader_chart.hide()
        
    def save_emg(self,rawEMG):
        pd.DataFrame(rawEMG).to_csv(f'./data/raw/trial{self.trial_}class{self.class_}.csv', mode='a', index = False, header=False)
    
    def update_label(self,flag):
        if flag:
            self.class_ = ((self.tmp) % (self.class_n)) + 1
            self.trial_ = 1 + (self.tmp//self.class_n)
            self.tmp += 1

    # def view(self,count):
    #     print(f'count : {count}')


def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = MainWindow()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()