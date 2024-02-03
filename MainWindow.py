import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
import time
from EMGsignal import EMGsignal
from reader_chart import RaderChartWindow
from progress import Progress
from picture import ImageSlider

class MainWindow(QWidget):

    """メインウィンドウ"""
    def __init__(self):
        super().__init__()
        self.EMGsinal_object = EMGsignal(2,2)
        self.initUI()
        # self.reader_chart.hide()
        self.EMGsinal_object.timer.start()
        # 初期はBreakからスタートする
        self.EMGsinal_object.tick.connect(self.progress.handleTimer)
        self.EMGsinal_object.array_signal.connect(self.reader_chart.updatePaintEvent)
        self.EMGsinal_object.finished_class.connect(self.progress.update_display)
        self.EMGsinal_object.finished_class.connect(self.image.next_image)
       
    
    def initUI(self):
        self.setWindowTitle("計測中")
        self.resize(1024, 640)          

        # self.central_widget = QWidget(self)
        # self.setCentralWidget(self.central_widget)
        # self.reader_chart.setGeometry(100, 100, 200, 25)

        self.reader_chart = RaderChartWindow(6)
        self.progress = Progress()
        self.image = ImageSlider()

        self.widget1 = QWidget()
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.reader_chart,4)
        self.layout1.addWidget(self.image,1)
        self.widget1.setLayout(self.layout1)


        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.widget1,4)
        self.layout.addWidget(self.progress,1)
        self.setLayout(self.layout)
        self.showFullScreen()

       
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

 



def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = MainWindow()
    mv.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()