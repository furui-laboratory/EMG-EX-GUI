import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImageReader, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class ImageSlider(QWidget):
    def __init__(self,image_path,parent=None):
        super().__init__(parent)

        # 画像ファイルのパスを適切に設定してください
        self.image_paths = image_path
        self.current_index = 0
        self.idx = 0

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Slider')

        self.image_label = QLabel(self)
        self.image_label.move(self.width() // 2, self.height() // 2)

        self.load_image()


        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def load_image(self):
        image_path = self.image_paths[self.current_index]
        image_reader = QImageReader(image_path)
        image_reader.setAutoTransform(True)

        image = image_reader.read()
        pixmap = QPixmap.fromImage(image)
        scaled_image = image.scaled(400, 700, Qt.KeepAspectRatio)
        pixmap = QPixmap.fromImage(scaled_image)


        self.image_label.setPixmap(pixmap)

    def next_image(self):
        if self.idx % 2 == 1:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.load_image()
        self.idx += 1
    
    
