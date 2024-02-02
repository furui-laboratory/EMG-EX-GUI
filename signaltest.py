from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import sys

class ArraySignalEmitter(QObject):
    # カスタムシグナルを定義
    array_signal = pyqtSignal(list)

    def send_array(self, data):
        # シグナルを発信
        self.array_signal.emit(data)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.button = QPushButton('Send Array', self)
        self.layout.addWidget(self.button)

        self.array_signal_emitter = ArraySignalEmitter()

        self.button.clicked.connect(self.send_array_slot)
        # カスタムシグナルを処理するスロットを接続
        self.array_signal_emitter.array_signal.connect(self.receive_array_slot)

    # @pyqtSlot()
    def send_array_slot(self):
        # 配列を送信
        data = [[1, 2, 3, 4, 5],[1,2,4,3,5]]
        self.array_signal_emitter.send_array(data)

    # @pyqtSlot(list)
    def receive_array_slot(self, data):
        # 受信した配列を処理
        print("Received Array:", data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
