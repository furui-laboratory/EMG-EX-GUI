from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot,QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import pandas as pd
import sys
import numpy as np
import time
# from src.delsys import DataHandle

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
        # self.datahandle = dh
        # self.datahandle.initialize_delsys()
        self.sec_break = sec_break
        self.sec_mes = sec_mes
        print(f'trial : {self.trial_n}')
        print(f'class : {self.class_n}')
        print(f'sec_mes:{sec_mes}')
        print(f'sec_break:{self.sec_break}')
        # 最初はbreakからスタートする
        self.count = sec_break*2000/40
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.send_data)
        self.timer.start(0.01)

    def send_data(self):

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
            print(f'flag : {self.flag}')
            self.finished_class.emit(self.flag)
        else:
            self.count = self.count -1
            '''EMGデータの送信'''
            rawEMG = self.dh.get_emg(mode='raw')
            self.tick.emit(self.count)
        
        
        # break以外の場合はデータを送信
        if self.flag:
            self.array_signal.emit(rawEMG)
        # rng = np.random.default_rng()
        # rawEMG = rng.random((40, 6)).tolist()
        # rawEMG = [[i for i in range(6)] for j in range(40)]
        
    

    def stop_count(self):
        # self.datahandle.stop_delsys()
        self.timer.stop()

    # def update_count(self):
    #     print(self.trial)
    #     print(self.class_num)

    #     if self.count == 0:
    #         self.finished.emit()
    #         return

    #     self.count = self.count -1
    #     self.tick.emit(self.count)
    #     """EMG の取得コードを書く"""
    #     """FlagがTureの場合はデータを保存、そうでない場合は捨てる"""
    #     rawEMG = self.datahandle.get_emg(mode='notch->rect->lpf')

    #     if self.flag == True:
    #         pd.DataFrame(rawEMG).to_csv(f'../data/raw/trial{self.trial}class{self.class_num}.csv', mode='a', index = False, header=False)
    #     else:
    #         pd.DataFrame(rawEMG).to_csv(f'../data/raw/Breakin{self.class_num}.csv', mode='a', index = False, header=False)

