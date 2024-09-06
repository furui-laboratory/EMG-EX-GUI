import sys
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel,QInputDialog,QMessageBox,QMenu,QAction
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
from PyQt5 import QtGui
import time
from EMGsignal import EMGsignal
from progress import Progress
from picture import ImageSlider
from src.delsys import DataHandle
import pandas as pd
from plot_emg import PlotWindow
from setting import Setting
from getemg_setting import GetEMGSetting
from raderchart_mixup import Mixupshow
from menu_emgonlineplot import WindowPlotOnlineEMG
from get_max_emg import GetMaxEMG
from classification.classification_menu import Classification_Menu
import configparser
import numpy as np
from data_worker import DataWorker

class Menu(QWidget):
    _instance = None

    @staticmethod
    def get_instance():
        if Menu._instance is None:
            Menu._instance = Menu()
        return Menu._instance

    """メインウィンドウ"""
    def __init__(self,parent=None):
        if Menu._instance is not None:
            raise Exception("This class is a singleton!")
        super().__init__(parent)

        self.button_setting = QPushButton('設定',self)
        self.button_online_emgplot = QPushButton('リアルタイム生波形表示',self)
        self.button_emgmax = QPushButton('最大値EMG取得',self)
        self.button_readerchart = QPushButton('レーダーチャート',self)
        self.button_get_emg = QPushButton('EMG取得',self)
        self.button_demo = QPushButton('機械学習デモ',self)
        self.button_create = QPushButton('新規被験者の追加',self) #フォルダの作成
        self.button_select = QPushButton('既存被験者の選択',self) #フォルダパスの選択
        self.button_connecting = QPushButton('センサを接続',self) 
        self.button_disconnect = QPushButton('センサを切断',self)


        # フォルダの数を管理する変数
        self.folder_count = 0
        self.directory_path = 'data' # ファルダをカウントするディレクトリ
        self.status_label = QLabel("Sensor status: Disconnected", self)

        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.trush_data)

        self.initUI()

        self.settingWindow = Setting()
        self.settingWindow.send_data()

        # 設定ボタンが押された時の処理
        self.button_setting.clicked.connect(self.hidewindow_setting)
        # 設定画面の戻るボタンが押された時の処理
        self.settingWindow.back_button.clicked.connect(self.showwindow_setting)

        # 取得ボタンが押された時の処理
        self.button_get_emg.clicked.connect(self.hidewindow_getemg)

        # レーダーチャートボタンが押された時の処理
        self.button_readerchart.clicked.connect(self.hidewindow_readerchart)
    
        # リアルタイム生波形表示ボタンが押された時の処理
        self.button_online_emgplot.clicked.connect(self.hidewindow_plot_emg)

        # 最大値EMG取得ボタンが押された時の処理
        self.button_emgmax.clicked.connect(self.hidewindow_emgmax)

        # 機械学習デモボタンが押された時の処理
        self.button_demo.clicked.connect(self.hidewindow_classification)

        # 新規被験者追加ボタンが押された時の処理
        self.button_create.clicked.connect(self.create_folder)

        # 既存被験者追加ボタンが押された時の処理
        self.button_select.clicked.connect(self.select_tester)

        # センサを接続する処理
        self.button_connecting.clicked.connect(self.connect_sensor)
        self.button_disconnect.clicked.connect(self.disconnect_sensor)

        # フォルダの数をカウント
        self.update_folder_count()
        self.dh = None
        self.running = False
        

    # リアルタイム生波形表示画面を表示
    def hidewindow_plot_emg(self):
        if self.dh is None:
            QMessageBox.warning(self, 'Error', 'Sensor is not connected.')
            return
        self.data = self.dh.get_emg()
        self.data = np.empty([])
        self.stop_worker()
        self.plot_window = WindowPlotOnlineEMG(dh=self.dh)  # DataHandleインスタンスを渡す
        self.plot_window.start()
        self.plot_window.show()
        self.hide()
        self.plot_window.closed.connect(self.window_closed)
    
    def window_closed(self):
        #self.timer.start(1)
        self.worker = DataWorker(self.dh)
        self.worker.data_processed.connect(self.handle_data)
        self.worker.start()
        self.show()

    # 取得準備画面を表示
    def hidewindow_getemg(self):
        if self.dh is None:
            QMessageBox.warning(self, 'Error', 'Sensor is not connected.')
            return
        self.data = self.dh.get_emg()
        self.data = np.empty([])
        self.stop_worker()
        self.saveemg_setting = GetEMGSetting(dh=self.dh)
        self.saveemg_setting.show()
        self.hide()
        self.saveemg_setting.closed.connect(self.window_closed)

    # 現在表示されているメニュー画面を非表示にして、設定画面を表示
    def hidewindow_setting(self):
        self.settingWindow.show()
        self.hide()
    # 設定画面を表示させて、メニュー画面を非表示にする
    def showwindow_setting(self):
        self.show()
        self.settingWindow.close()

    # レーダーチャート画面を表示
    def hidewindow_readerchart(self):
        if self.dh is None:
            QMessageBox.warning(self, 'Error', 'Sensor is not connected.')
            return
        self.data = self.dh.get_emg()
        self.data = np.empty([])
        self.stop_worker()
        self.rader_chartwindow = Mixupshow(dh=self.dh)
        self.rader_chartwindow.start()
        self.rader_chartwindow.show()
        self.hide()
        self.rader_chartwindow.closed.connect(self.window_closed)

    # 最大値EMG取得画面を表示
    def hidewindow_emgmax(self):
        if self.dh is None:
            QMessageBox.warning(self, 'Error', 'Sensor is not connected.')
            return
        self.data = self.dh.get_emg()
        self.data = np.empty([])
        self.stop_worker()
        self.savemaxemgWindow = GetMaxEMG(dh=self.dh)
        self.savemaxemgWindow.start()
        self.savemaxemgWindow.show()
        self.hide()
        self.savemaxemgWindow.closed.connect(self.window_closed)

    # 機械学習デモ画面を表示
    def hidewindow_classification(self):
        self.classification_menu = Classification_Menu()
        self.classification_menu.show()
        self.hide()
        self.classification_menu.closed.connect(self.show)
    
    # 新規フォルダを作成
    def create_folder(self):
        folder_name, ok = QInputDialog.getText(self, 'フォルダ名の入力', '新しいフォルダ名を入力してください')

        if ok and folder_name:
            current_dir = os.getcwd() # 現在作業中のディレクトリを取得
            new_folder_path = os.path.join(current_dir, self.directory_path, folder_name) # 新しいフォルダパスを生成

            try:
                os.makedirs(new_folder_path)
                c_task_path = os.path.join(new_folder_path, 'c_task') # 連続試行のフォルダ
                s_task_path = os.path.join(new_folder_path, 's_task') # 単一試行のフォルダ
                os.makedirs(c_task_path)
                os.makedirs(s_task_path)
                self.update_folder_count()
            except FileExistsError:
                QMessageBox.warning(self, 'エラー', 'フォルダは既に存在します')
            # .imiファイルへ書き込み
            self.update_setting_ini('settings', 'tester_name', folder_name)
            self.update_setting_ini('settings', 'save_path', new_folder_path)

    def update_setting_ini(self, section, key, value, file_path='./setting.ini'):
        config = configparser.ConfigParser()
        config.read(file_path)

        if section not in config:
            config.add_section(section)
        config[section][key] = value
        with open(file_path, 'w') as configfile:
            config.write(configfile)
    
    # フォルダ数のカウント
    def update_folder_count(self):
        if os.path.exists(self.directory_path):
            self.folder_count = len([d for d in os.listdir(self.directory_path) if os.path.isdir(os.path.join(self.directory_path, d))])
        else:
            self.folder_count = 0        

    # フォルダの選択
    def select_tester(self):
        menu = QMenu(self)

        if os.path.exists(self.directory_path):
            folders = [d for d in os.listdir(self.directory_path) if os.path.isdir(os.path.join(self.directory_path, d))]

            for folder_name in folders:
                action = QAction(folder_name, self)
                action.triggered.connect(lambda checked, name=folder_name: self.show_selection(name))
                menu.addAction(action)
        menu.exec_(self.button_select.mapToGlobal(self.button_select.rect().bottomLeft()))

    def show_selection(self, folder_name):
        current_dir = os.getcwd()
        select_folder_path = os.path.join(current_dir, self.directory_path, folder_name)

        # .imiファイルへ書き込み
        self.update_setting_ini('settings', 'tester_name', folder_name)
        self.update_setting_ini('settings', 'save_path', select_folder_path)

    def connect_sensor(self):
        config = configparser.ConfigParser()
        config.read('./setting.ini')
        self.ch = config.get('settings', 'ch')
        self.ch = int(self.ch)
        if not self.dh:
            self.dh = DataHandle(self.ch)
            self.dh.initialize_delsys()
        
        if self.dh and not self.running:
            self.running = True
            self.update_status_label()
            self.worker = DataWorker(self.dh)
            self.worker.data_processed.connect(self.handle_data)
            self.worker.start()
        #self.timer.start(1)
    
    def disconnect_sensor(self):
        self.running = False
        #self.timer.stop()
        self.stop_worker()
        try:
            self.dh.stop_delsys()
            self.dh = None
            self.update_status_label()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to disconnect sensor: {str(e)}')
    
    # 接続状況を表示するメソッド
    def update_status_label(self):
        if self.running:
            self.status_label.setText("Sensor status: Connected")
        else:
            self.status_label.setText("Sensor status: Disconnected")

    #def trush_data(self):
        #self.trush_data = self.dh.get_emg()
        #self.trush_data = np.empty([])
        
   
    def handle_data(self, data):
        # Process EMG data here
        pass

    def stop_worker(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()  # Wait until the worker thread finishes


    def initUI(self):
        self.setWindowTitle("menu")
        self.setGeometry(0,0,1920,1080)

        font = QtGui.QFont()
        font.setPointSize(20)
        self.button_setting.setFont(font)
        self.button_online_emgplot.setFont(font)
        self.button_emgmax.setFont(font)
        self.button_readerchart.setFont(font)
        self.button_get_emg.setFont(font)
        self.button_demo.setFont(font)
        self.button_create.setFont(font)
        self.button_select.setFont(font)
        self.button_connecting.setFont(font)
        self.button_disconnect.setFont(font)

        self.button_setting.setGeometry(710,100,500,100)
        self.button_online_emgplot.setGeometry(710,250,500,100)
        self.button_emgmax.setGeometry(710,400,500,100)
        self.button_readerchart.setGeometry(710,550,500,100)
        self.button_get_emg.setGeometry(710,700,500,100)
        self.button_demo.setGeometry(710,850,500,100)
        self.button_create.setGeometry(10,10,500,100)
        self.button_select.setGeometry(10,120,500,100)
        self.button_connecting.setGeometry(1310,10,500,100)
        self.button_disconnect.setGeometry(1310,120,500,100)
        self.status_label.setFont(font)
        self.status_label.setAlignment(Qt.AlignCenter)  # 中央揃え
        self.status_label.setGeometry(1310, 230, 500, 100)  # 任意の位置とサイズに設定


def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    mv = Menu()
    mv.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()