import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImageReader, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class ImageSlider(QWidget):
    def __init__(self):
        super().__init__()

        self.image_paths = [".\images\motion1.png", ".\images\motion2.png", ".\images\motion3.png"]  # 画像ファイルのパスを適切に設定してください
        self.current_index = 0

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Slider')
        # self.setGeometry(100, 100, 400, 300)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(QSize(300, 200))  # 画像表示領域のサイズを設定

        self.load_image()

        # next_button = QPushButton('Next', self)
        # next_button.clicked.connect(self.next_image)

        # prev_button = QPushButton('Previous', self)
        # prev_button.clicked.connect(self.previous_image)

        # layout = QVBoxLayout()
        # layout.addWidget(self.image_label)
        # layout.addWidget(next_button)
        # layout.addWidget(prev_button)

        # self.setLayout(layout)

    def load_image(self):
        image_path = self.image_paths[self.current_index]
        image_reader = QImageReader(image_path)
        image_reader.setAutoTransform(True)

        image = image_reader.read()
        pixmap = QPixmap.fromImage(image)
        scaled_image = image.scaled(QSize(300, 200), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap = QPixmap.fromImage(scaled_image)


        self.image_label.setPixmap(pixmap)

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.load_image()

    def previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self.load_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSlider()
    window.show()
    sys.exit(app.exec_())
