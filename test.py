import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal

class MainWindow(QMainWindow):
    closed = pyqtSignal()  # ウィンドウが閉じられたときのシグナル
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Close Event Example")
        self.resize(300, 200)
        
    def closeEvent(self, event):
        # ウィンドウが閉じられたときにシグナルを送信
        self.closed.emit()
        event.accept()

def on_window_closed():
    print("Window closed")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.closed.connect(on_window_closed)  # ウィンドウが閉じられたときのシグナルに接続
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
