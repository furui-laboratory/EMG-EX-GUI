import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar,QPushButton,QVBoxLayout,QWidget,QSizePolicy,QHBoxLayout,QLabel,QTextEdit,QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtTest
from PyQt5 import QtGui
import time
from EMGsignal import EMGsignal
from reader_chart import RaderChartWindow
from progress import Progress
from picture import ImageSlider
from src.delsys import DataHandle
import pandas as pd
from plot_emg import PlotWindow
# from menu import Menu
import configparser


class Setting(QWidget):

    """メインウィンドウ"""
    def __init__(self,parent=None):
        super().__init__(parent)
        config = configparser.ConfigParser()
        config.read('./setting.ini')

        self.label_electrode_num = QLabel('電極数')
        self.electrode_num = QTextEdit(self)
        self.electrode_num.setText(config['settings']['ch'])

        self.label_trial_num = QLabel('試行数')
        self.trial_num = QTextEdit(self)
        self.trial_num.setText(config['settings']['trial_n'])

        self.label_class_num = QLabel('動作数')
        self.class_num = QTextEdit(self)
        self.class_num.setText(config['settings']['class_n'])

        self.label_m_time = QLabel('計測時間')
        self.m_time = QTextEdit(self)
        self.m_time.setText(config['settings']['sec_mes'])

        self.label_rest_class = QLabel('クラス間Rest')
        self.rest_class = QTextEdit(self)
        self.rest_class.setText(config['settings']['sec_class_break'])

        self.label_rest_trial = QLabel('試行間Rest')
        self.rest_trial = QTextEdit(self)
        self.rest_trial.setText(config['settings']['sec_trial_break'])

        self.label_image_path = QLabel("画像フォルダのパス",self)
        self.image_path = QTextEdit(self)
        self.image_path.setText(config['settings']['image_path'])

        self.label_save_path = QLabel('保存フォルダのパス',self)
        self.save_path = QTextEdit(self)
        self.save_path.setText(config['settings']['save_path'])

        self.back_button = QPushButton('戻る',self)
        self.firstlabel = QWidget(self)
        self.firstwidget = QWidget(self)
        self.secondlabel = QWidget(self)
        self.secondwidget = QWidget(self)
        self.initUI()
        self.back_button.clicked.connect(self.send_data)

        

    def send_data(self):
        ch = int(self.electrode_num.toPlainText())
        class_n = int(self.class_num.toPlainText())
        trial_n = int(self.trial_num.toPlainText())
        sec_mes = int(self.m_time.toPlainText())
        sec_class_break = int(self.rest_class.toPlainText())
        sec_trial_break = int(self.rest_trial.toPlainText())
        # データをiniファイルに書き込む
        self.update_setting_ini('settings', 'ch', ch)
        self.update_setting_ini('settings', 'class_n', class_n)
        self.update_setting_ini('settings', 'trial_n', trial_n)
        self.update_setting_ini('settings', 'sec_mes', sec_mes)
        self.update_setting_ini('settings', 'sec_class_break', sec_class_break)
        self.update_setting_ini('settings', 'sec_trial_break', sec_trial_break)
        self.update_setting_ini('settings', 'image_path', self.image_path.toPlainText)
        

    def update_setting_ini(self, section, key, value, file_path='./setting.ini'):
        config = configparser.ConfigParser()
        config.read(file_path)

        if section not in config:
            config.add_section(section)
        if not isinstance(value, str):
            value = str(value)

        config[section][key] = value
        with open(file_path, 'w') as configfile:
            config.write(configfile)
        
       
    def initUI(self):
        self.setWindowTitle("menu")
        self.setGeometry(0,0,1920,1080)

        self.label_electrode_num.setAlignment(Qt.AlignCenter)
        self.label_class_num.setAlignment(Qt.AlignCenter)
        self.label_trial_num.setAlignment(Qt.AlignCenter)
        self.label_m_time.setAlignment(Qt.AlignCenter)
        self.label_rest_class.setAlignment(Qt.AlignCenter)
        self.label_rest_trial.setAlignment(Qt.AlignCenter)

        


        self.firstlabellayout = QHBoxLayout()
        self.firstlabellayout.addWidget(self.label_electrode_num)
        self.firstlabellayout.addWidget(self.label_class_num)
        self.firstlabellayout.addWidget(self.label_trial_num)
        self.firstlabel.setLayout(self.firstlabellayout)
        self.firstlabel.setGeometry(30,40,1850,80)
        

        self.firstwidgetlayout = QHBoxLayout()
        self.firstwidgetlayout.addWidget(self.electrode_num)
        self.firstwidgetlayout.addWidget(self.class_num)
        self.firstwidgetlayout.addWidget(self.trial_num)
        self.firstwidget.setLayout(self.firstwidgetlayout)
        self.firstwidget.setGeometry(65,100,1800,80)


        self.secondlabellayout = QHBoxLayout()
        self.secondlabellayout.addWidget(self.label_m_time)
        self.secondlabellayout.addWidget(self.label_rest_class)
        self.secondlabellayout.addWidget(self.label_rest_trial)
        self.secondlabel.setLayout(self.secondlabellayout)
        self.secondlabel.setGeometry(30,190,1850,80)

        self.secondwidgetlayout = QHBoxLayout()
        self.secondwidgetlayout.addWidget(self.m_time)
        self.secondwidgetlayout.addWidget(self.rest_class)
        self.secondwidgetlayout.addWidget(self.rest_trial)
        self.secondwidget.setLayout(self.secondwidgetlayout)
        self.secondwidget.setGeometry(65,250,1800,80)

        self.label_image_path.setGeometry(840,450,600,80)
        self.image_path.setGeometry(140,530,1650,50)
        self.label_save_path.setGeometry(840,630,600,80)
        self.save_path.setGeometry(140,710,1650,50)

        self.back_button.setGeometry(858,830,200,80)

  
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_electrode_num.setFont(font)
        self.label_class_num.setFont(font)
        self.label_trial_num.setFont(font)
        self.electrode_num.setFont(font)
        self.class_num.setFont(font)
        self.trial_num.setFont(font)
        self.label_m_time.setFont(font)
        self.label_rest_class.setFont(font)
        self.label_rest_trial.setFont(font)
        self.m_time.setFont(font)
        self.rest_class.setFont(font)
        self.rest_trial.setFont(font)
        self.image_path.setFont(font)
        self.save_path.setFont(font)
        self.label_image_path.setFont(font)
        self.label_save_path.setFont(font)
        self.back_button.setFont(font)
        


