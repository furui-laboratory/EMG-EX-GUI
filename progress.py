import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
import time
from reader_chart import RaderChartWindow

class Progress(QWidget):
    
    def __init__(self,sec_mes=7,sec_break=3,parent=None):
        super().__init__(parent)


        self.initial_count_mes = sec_mes*2000/40
        self.initial_count_break = sec_break*2000/40
        self.initial_count = self.initial_count_break
        self.pbar = QProgressBar(self)

        self.pbar.resize(1500, 50)
        self.pbar.setValue(0)


    def handleTimer(self,count):
        if count > 0:
            value = 100*(1-count/self.initial_count)
            self.pbar.setValue(value)
        else:
            pass

    
    '''プログレスバーの値をリセットする.EMgsignalからclassemitsignalが発生したときに呼び出される'''
    def update_display(self,flag):

        self.pbar.setValue(0)

        if flag==False:
            self.initial_count = self.initial_count_break
        else:
            self.initial_count = self.initial_count_mes
            

