import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class CustomWidget1(QWidget):
    def __init__(self, value=3,parent=None):
        super().__init__(parent)

        label = QLabel('Custom Widget 1', self)
        button = QPushButton('Button in Custom Widget 1', self)
        self.value = value
        print(self.value)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(button)

class CustomWidget2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        label = QLabel('Custom Widget 2', self)
        button = QPushButton('Button in Custom Widget 2', self)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(button)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.custom_widget_1 = CustomWidget1(12,self)
        self.custom_widget_2 = CustomWidget2(self)

        # main_layout = QVBoxLayout(self)
        # main_layout.addWidget(custom_widget_1)
        # main_layout.addWidget(custom_widget_2)
        self.custom_widget_1.setGeometry(960, 270, 200, 100)
        self.custom_widget_2.setGeometry(960, 540, 200, 100)

class FullScreenApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Full Screen App')
        self.setGeometry(0,0,1920,1080)   
      


        main_widget = MainWidget()
        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = FullScreenApp()
    mainWindow.show()
    sys.exit(app.exec_())
