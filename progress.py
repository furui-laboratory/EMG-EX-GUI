import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
import time
from reader_chart import RaderChartWindow

class Progress(QWidget):
    
    def __init__(self,sec_mes=7,sec_break=3):
        super().__init__()

        # self.freq = 2000
        # self.timing = 40
        # self.count = self.motion_sec*self.freq/self.timing
        # self.kote =  self.motion_sec*self.freq/self.timing

        self.initial_count_mes = sec_mes*2000/40
        self.initial_count_break = sec_break*2000/40
        self.initial_count = self.initial_count_break
        self.pbar = QProgressBar(self)
        # self.pbar.setGeometry(0, 0, 300, 50)
        self.pbar.setValue(0)
        layout = QVBoxLayout()
        layout.addWidget(self.pbar)
        self.setLayout(layout)
        
        # self.setWindowTitle("QT Progressbar Example")
        # self.setGeometry(0,0,500,500)
        # self.showFullScreen()
        # self.resize(1000,500)


        # self.reset_button = QPushButton('Reset',self)
        # self.reset_button.clicked.connect(self.close)
        # self.reset_button.setGeometry(0,100,200,50)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.get_emg)
        # self.timer.start(1)

        # layout = QVBoxLayout()
        # layout.addWidget(self.pbar)
        # layout.addWidget(self.reset_button)
        # self.setLayout(layout)

        # self.show()

    def handleTimer(self,count):
        value = self.pbar.value()
        if count > 0:
            # print(count)
            value = 100*(1-count/self.initial_count)+1
            self.pbar.setValue(value)
        else:
            pass

    
    '''プログレスバーの値をリセットする.EMgsignalからclassemitsignalが発生したときに呼び出される'''
    def update_display(self,flag):
        if flag:
            self.initial_count = self.initial_count_mes
        else:
            self.initial_count = self.initial_count_break

        self.pbar.setValue(0)

    # def get_emg(self):
    #     time.sleep(0.02)
    #     self.handleTimer()
        
        
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Progress()
#     sys.exit(app.exec_())