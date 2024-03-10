import sys
sys.path.append('..')
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtTest
from PyQt5.QtGui import QFont
import pandas as pd
from EMGsignal import EMGsignal
from reader_chart import RaderChartWindow
from progress import Progress
from picture import ImageSlider
from src.delsys import DataHandle
import numpy as np
import os
import shutil
import configparser



class LearningWindow(QWidget):
    closed = pyqtSignal()
    """メインウィンドウ"""
    def __init__(self,ch,parent=None):
        super().__init__(parent)
        shutil.rmtree('./classification/train_data/')
        os.mkdir('./classification/train_data')
        
        config = configparser.ConfigParser()
        config.read('setting.ini')
        self.ch = config['settings'].getint('ch')
        # 試行数とクラス数の数値を定義
        self.trial_n = 1
        self.class_n = 3
        self.sec_mes = config['settings'].getint('sec_mes')
        self.sec_class_break = config['settings'].getint('sec_class_break')
        self.dh = DataHandle(self.ch)
        self.dh.initialize_delsys()
        # ラベルの初期化
        self.trial_ = 0
        self.class_ = 0
        # 現在の試行数とクラス数を求めるための変数
        self.tmp = 0
        self.image_path = [".\classification\images\motion1.png", ".\classification\images\motion2.png",".\classification\images\motion3.png"]
        self.EMGsinal_object = EMGsignal(self.dh,self.trial_n,self.class_n,self.sec_class_break,self.sec_mes)
        self.initUI()
        self.reader_chart.hide()
        self.EMGsinal_object.timer.start()
        # 初期はBreakからスタートする
        self.EMGsinal_object.tick.connect(self.progress.handleTimer)
        # self.EMGsinal_object.tick.connect(self.view)
        # レーダーチャートの更新
        self.EMGsinal_object.array_signal.connect(self.reader_chart.updatePaintEvent)
        # EMGデータの保存
        self.EMGsinal_object.array_signal.connect(self.save_emg)
        # プログレスバーの更新
        self.EMGsinal_object.finished_class.connect(self.progress.update_display)
        # ラベルの更新
        self.EMGsinal_object.finished_class.connect(self.update_label)
        # 画像の更新
        self.EMGsinal_object.finished_class.connect(self.image.next_image)
        # Breakの表示
        self.EMGsinal_object.finished_class.connect(self.display_break)
        # 全ての試行が終了したとき
        self.EMGsinal_object.finished_all_trial.connect(self.learning)
    
    # def start(self):
    #     self.dh = DataHandle(self.ch)
    #     self.dh.initialize_delsys()
    #     self.EMGsinal_object = EMGsignal(self.dh,self.trial_n,self.class_n,self.sec_class_break,self.sec_mes)
    #     self.initUI()

    def initUI(self):
        self.setWindowTitle("計測中")
        self.setGeometry(0,0,1920,1080)        


        self.reader_chart = RaderChartWindow(self.dh,self.ch,self)
        self.progress = Progress(self.sec_mes,self.sec_class_break,self)
        # 参照する画像を渡せるようにする
        self.image = ImageSlider(self.image_path,self)
        # self.plot_emg = PlotWindow(self.ch,self)
        self.Breaking_label = QLabel(self)
        self.Class_label = QLabel(self)
        self.display_break(False)
       

        self.progress.setGeometry(230, 900, 1500, 1000)
        self.Breaking_label.setGeometry(950, 300, 900, 300)
        self.Class_label.setGeometry(160, 70, 800, 200)
        self.reader_chart.setGeometry(780, 10, 900, 900)
        self.image.setGeometry(350, 10, 900, 900)
        
        
        
    def closeEvent(self, event):
        # ウィンドウが閉じられたときにシグナルを送信
        '''simulation'''
        self.EMGsinal_object.timer.stop()
        self.dh.stop_delsys()
        self.closed.emit()
        event.accept()
        
    def save_emg(self,rawEMG):
        pd.DataFrame(rawEMG).to_csv(f'./classification/train_data/trial{self.trial_}class{self.class_}.csv', mode='a', index = False, header=False)
    
    def update_label(self,flag):
        if flag:
            self.class_ = ((self.tmp) % (self.class_n)) + 1
            self.trial_ = 1 + (self.tmp//self.class_n)
            self.tmp += 1

            print(f'trial{self.trial_}')

    # def view(self,count):
    #     print(f'count : {count}')
    
    def display_break(self,flag):
        if flag == False:
            # self.plot_emg.hide()
            self.reader_chart.hide()
            self.Breaking_label.show()
            font_rest = QFont()
            font_image = QFont()
            font_rest.setPointSize(100)
            font_image.setPointSize(50)
            self.Breaking_label.setFont(font_rest)
            self.Class_label.setFont(font_image)
            self.Breaking_label.setText('Breaking')
            self.Class_label.setText('Next Motion')
            self.Class_label.setAlignment(Qt.AlignCenter)
        else:
            # self.plot_emg.show()
            self.reader_chart.show()
            self.Breaking_label.hide()
            font = QFont()
            font.setPointSize(50)
            self.Class_label.setFont(font)
            self.Class_label.setText(f'Class{self.class_}')

    def learning(self):
        # 取得したデータからパラメータを計算し,windowを閉じる
        self.EMGsinal_object.timer.stop()
        self.dh.stop_delsys()
        print(f'Training Start')
        mu = np.empty((self.class_n,self.ch))
        sigma = np.empty((self.class_n,self.ch,self.ch))
        # データの読み込み
        for c in range(self.class_n):
            data = np.loadtxt(f'./classification/train_data/trial1class{c+1}.csv',delimiter=',')
            # 生波形を整流平滑化する
            rectifiedEMG = self.dh._get_notched_rectified_lpf_emg(data)
            mu[c] = np.mean(rectifiedEMG,axis=0)
            mu[c] = np.sum(rectifiedEMG,axis=0).T/len(rectifiedEMG)
            centered_X = rectifiedEMG - mu[c]
            sigma[c] = np.dot(centered_X.T,centered_X)

        sigma_pool = np.sum(sigma,axis=0) / (len(rectifiedEMG)-1)
        np.savetxt('./classification/parameter/mu.csv',mu,delimiter=',')
        np.savetxt('./classification/parameter/sigma.csv',sigma_pool,delimiter=',')
        print('Done')
        self.close()


def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    window = LearningWindow(3)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
        