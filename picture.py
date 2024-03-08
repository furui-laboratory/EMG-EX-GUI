import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImageReader, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class ImageSlider(QWidget):
    def __init__(self,image_path,parent=None):
        super().__init__(parent)

        # 画像ファイルのパスを適切に設定してください
        self.image_paths = image_path
        # self.image_paths = [".\images\motion1.png", ".\images\motion2.png"] 
        self.current_index = 0
        self.idx = 0

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Slider')
        # self.setGeometry(100, 100, 400, 300)

        self.image_label = QLabel(self)
        self.image_label.move(self.width() // 2, self.height() // 2)
        # self.image_label.setAlignment(Qt.AlignCenter)
        # self.image_label.setFixedSize(QSize(500, 900))  # 画像表示領域のサイズを設定

        self.load_image()

        # next_button = QPushButton('Next', self)
        # next_button.clicked.connect(self.next_image)

        # prev_button = QPushButton('Previous', self)
        # prev_button.clicked.connect(self.previous_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        # layout.addWidget(next_button)
        # layout.addWidget(prev_button)

        self.setLayout(layout)

    def load_image(self):
        image_path = self.image_paths[self.current_index]
        image_reader = QImageReader(image_path)
        image_reader.setAutoTransform(True)

        image = image_reader.read()
        pixmap = QPixmap.fromImage(image)
        # scaled_image = image.scaled(QSize(500, 900), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        scaled_image = image.scaled(400, 700, Qt.KeepAspectRatio)
        pixmap = QPixmap.fromImage(scaled_image)


        self.image_label.setPixmap(pixmap)

    def next_image(self):
        if self.idx % 2 == 1:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.load_image()
        self.idx += 1
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSlider()
    window.show()
    sys.exit(app.exec_())
