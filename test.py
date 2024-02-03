import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget

class FullScreenApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Full Screen App')

        # フルスクリーンモードに設定
        self.setGeometry(0,0,1920,1080)

        # ディスプレイのサイズを取得
        desktop = QDesktopWidget()
        screen_rect = desktop.screenGeometry()

        # フルスクリーン時の幅と高さを表示
        print(f"Fullscreen Width: {screen_rect.width()}, Height: {screen_rect.height()}")

        # ウィジェットの作成と配置
        widget1 = QLabel('Widget 1', self)
        widget1.setGeometry(50, 50, 200, 100)

        widget2 = QLabel('Widget 2', self)
        widget2.setGeometry(50, 200, 200, 100)

        widget3 = QLabel('Widget 3', self)
        widget3.setGeometry(50, 350, 200, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = FullScreenApp()
    mainWindow.show()
    sys.exit(app.exec_())
