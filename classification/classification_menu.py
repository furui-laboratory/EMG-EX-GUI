import os
import sys
sys.path.append('..')
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtTest
from PyQt5 import QtGui
from classification.learning_window import LearningWindow
from classification.prediction_window import PredictionWindow
import configparser


class Classification_Menu(QWidget):
    closed = pyqtSignal()
    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)

        self.button_learning = QPushButton('学習',self)
        self.button_prediction = QPushButton('予測',self)
        self.button_back = QPushButton('戻る',self)
        self.config = configparser.ConfigParser()
        self.config.read('setting.ini')
        self.ch = self.config['settings'].getint('ch')
        self.learningWindow = LearningWindow()
        self.button_back.clicked.connect(self.close)

        # self.learningWindow = LearningWindow(self.ch)
        # self.predictionWindow = PredictionWindow(self.ch,3)

        # 学習ボタンが押された時の処理
        self.button_learning.clicked.connect(self.show_learning_window)
        # 分類ボタンが押された時の処理
        self.button_prediction.clicked.connect(self.show_prediction_window)
        # self.button_learning.closed(self.show)
        # self.learningWindow.closed.connect(self.show)


        self.initUI()


    # まだ一回も学習していない場合，予測ボタンを押せないようにする
    # def check_learning(self):
        # self.parameter = np.loadtxt('./parameter')
        # if len(self.parameter) = 0:
            # self.predictionbuttonを押せないようにする
        
    def show_learning_window(self):
        # self.hide()
        self.learningWindow = LearningWindow()
        # self.learningWindow.show()
        self.learningWindow.start()
        self.learningWindow.show()
        # self.learningWindow.show()
        self.hide()
        self.learningWindow.closed.connect(self.show)

    def show_prediction_window(self):
        self.predictionWindow = PredictionWindow(self.ch,3)
        self.predictionWindow.start()
        self.predictionWindow.show()
        self.hide()
        self.predictionWindow.closed.connect(self.show)

    


   
    def initUI(self):
        self.setWindowTitle("Classification")
        self.setGeometry(0,0,1920,1080)


        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_learning.setFont(font)
        self.button_prediction.setFont(font)
        self.button_back.setFont(font)

        self.button_learning.setGeometry(710,300,500,100)
        self.button_prediction.setGeometry(710,500,500,100)
        self.button_back.setGeometry(710,700,500,100)

        # self.learningWindow.closed.connect(self.show)
    def closeEvent(self, event):
        print('before closed')
        self.closed.emit()
        event.accept()
        print('after close')# ウィンドウが閉じられたときにシグナルを送信




      
def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Classification_Menu()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()