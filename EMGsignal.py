from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot,QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import pandas as pd
import sys
import numpy as np
import time


class EMGsignal(QObject):
    # カスタムシグナルを定義
    array_signal = pyqtSignal(np.ndarray)
    finished_class = pyqtSignal(bool)
    finished_all_trial = pyqtSignal()
    tick = pyqtSignal(float)

    def __init__(self,dh,trial_n,class_n,sec_break,sec_mes,parent=None):
        super().__init__(parent)
        """それぞれのtrialとclass、Flagを定義する"""
        self.trial_n = trial_n
        self.class_n = class_n
        self.dh = dh
        self.total_num = self.class_n*self.trial_n
        self.flag = False
        
        self.sec_break = sec_break
        self.sec_mes = sec_mes
        
        self.count = sec_break*2000/40
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.send_data)
        self.timer.start(0.01)

    def send_data(self):

        '''EMGデータの取得'''
        rawEMG = self.dh.get_emg(mode='raw')
        

        '''カウントデータの送信'''
        if self.count == 0:
            # 状態によってcountを変更する
            if self.flag == False:
                # すべての試行が終了した場合
                if self.total_num == 0:
                    self.finished_all_trial.emit()
                    self.stop_count()
                    return
                # 次のclassのカウントにセット
                self.count = self.sec_mes*2000/40
                self.total_num -= 1
            else:
                # 次のbreakのカウントにセット
                self.count = self.sec_break*2000/40
            # flagを逆にする
            self.flag = not self.flag
            # print(f'flag : {self.flag}')
            self.finished_class.emit(self.flag)
        else:
            # break以外の場合はデータを送信
            if self.flag:
                self.array_signal.emit(rawEMG)
        
            self.count = self.count -1
            '''カウントデータの送信'''
            self.tick.emit(self.count)

        
        
        
        
    

    def stop_count(self):
        self.timer.stop()
