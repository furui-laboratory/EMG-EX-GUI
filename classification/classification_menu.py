import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
from PyQt5 import QtGui
from learning_window import LearningWindow
from classification.probability_window import PredictionWindow

class Classification_Menu(QWidget):
    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)

        self.button_learning = QPushButton('学習',self)
        self.button_prediction = QPushButton('予測',self)

        self.learningWindow = LearningWindow(3)
        self.predictionWindow = PredictionWindow()

        self.initUI()

        # 学習ボタンが押された時の処理
        self.button_learning.clicked.connect(self.startwindow_learning)
        # # 分類ボタンが押された時の処理
        # self.button_prediction.clicked.connect(self.hidewindow_prediction)  

        # # 遷移先である学習ウィンドウの戻るボタンが押された時の処理
        # self.learningWindow.button_back.clicked.connect(self.showwindow_learning)
        # # 分類ウィンドウの戻るボタンが押された時の処理
        # self.predictionWindow.button_back.clicked.connect(self.showwindow_prediction)

    # まだ一回も学習していない場合，予測ボタンを押せないようにする
    # def check_learning(self):
        # self.parameter = np.loadtxt('./parameter')
        # if len(self.parameter) = 0:
            # self.predictionbuttonを押せないようにする
        
    def startwindow_learning(self):
        self.learningWindow.show()

    def hidewindow_learning(self):
        # 学習フェーズのウィンドウを表示させる
        self.learningWindow.show()
        self.hide()
    
    def hidewindow_prediction(self):
        # 分類フェーズのウィンドウを表示させる
        self.predictionWindow.show()
        self.hide()
    

    def showwindow_learning(self):
        # メニューウィンドウを表示させて遷移先のウィンドウを閉じる
        self.show()
        self.learningWindow.hide()
    
    def showwindow_prediction(self):
        # メニューウィンドウを表示させて遷移先のウィンドウを閉じる
        self.show()
        self.predictionWindow.hide()
    

   
    def initUI(self):
        self.setWindowTitle("Classification")
        self.setGeometry(0,0,1920,1080)


        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_learning.setFont(font)
        self.button_prediction.setFont(font)

        self.button_prediction.setGeometry(310,500,500,100)
        self.button_learning.setGeometry(610,500,500,100)


      
def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Classification_Menu()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()