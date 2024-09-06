from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

class DataWorker(QThread):
    data_processed = pyqtSignal(object)  # Signal to emit processed data

    def __init__(self, dh, parent=None):
        super().__init__(parent)
        self.dh = dh
        self.running = True

    def run(self):
        while self.running:
            self.data = self.dh.get_emg()
            self.data = np.empty([])
            self.msleep(1)  # Sleep for 100 ms; adjust as needed

    def stop(self):
        self.running = False