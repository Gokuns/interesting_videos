# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mega_deneme.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QDir, Qt, QUrl, QRect
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QComboBox, QAction)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QProgressBar
from PyQt5.QtGui import QIcon
import sys
import Dataset
import config
import ntpath
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib
from visualizer.add import Ui_Dialog
from visualizer.help import Ui_HelperDialog

from config import argument_defaults as ad
matplotlib.use('Qt5Agg')
import threading
import matplotlib.colors as c
from options import Ui_SettingsDialog
import numpy as np

from sklearn.manifold import TSNE

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from visualizer.video_player_module import play_vid, VideoWindow
import json
import config
import numpy as np




from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):


    def pca_data(self, data):
        feature_vector_list = [video["features"] for video in data]
        features = StandardScaler().fit_transform(feature_vector_list)
        pca = PCA(n_components=self.numberOfComponentsSpinBox.value())
        principal_components = pca.fit_transform(features).tolist()
        for i in range(len(data)):
            data[i]["features"] = principal_components[i]
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        return data

    def load_data(self, path=config.argument_defaults['aggregation'] + "/max_pool.json"):
        # load and create a list
        f = open(path)
        fil = json.load(f)
        # features = np.asarray(fil)
        return fil

    def partition_data(self, fil, mode):
        features = [fil[i]['features'] for i in range(len(fil))]
        names = [fil[i]['video'] for i in range(len(fil))]
        labels = None
        if mode:
            pass
            #labels = [fil[i]['poc_result'] for i in range(len(fil))]
        self.names = names
        return features, names, labels

    def tsne(self, features, names, labels):
        per = self.perplexitySpinBox.value()
        learning_rate = self.learningRateSpinBox.value()
        early_exaggeration = self.earlyExaggerationSpinBox.value()
        n_iter = self.iterationsSpinBox.value()

        X_embedded = TSNE(n_components=3, perplexity=per,
                          learning_rate=learning_rate,
                          early_exaggeration=early_exaggeration,
                          n_iter=n_iter).fit_transform(features)
        x_vals = [X_embedded[i][0] for i in range(len(X_embedded))]
        y_vals = [X_embedded[i][1] for i in range(len(X_embedded))]
        z_vals = [X_embedded[i][2] for i in range(len(X_embedded))]

        return x_vals, y_vals, z_vals

    def onpick(self, event, names):
        thisline = event.artist
        ind = event.ind
        # points = tuple(zip(xdata[ind], ydata[ind]))
        scene_name = names[ind[0]]

        config.argument_defaults['selected_scene'] = scene_name
        print(config.argument_defaults['selected_scene'])
        self.sceneComboBox.setCurrentText(config.argument_defaults['selected_scene'])
        self.openVideo(config.argument_defaults['selected_scene'])
        self.play()


    def plot_tnse(self, x_vals, y_vals, z_vals, names, labels, mode):
        self.plotWidget.canvas.axes.clear()
        self.plotWidget.canvas.axes.patch.set_visible(False)


            #labels = [color[i] if labels[j]==i else 'black' for j in labels]

        if mode:
            uniq = np.unique(labels)
            for i in range(len(uniq)):
                labels = [self.color[i] if j == i else j for j in labels]
        #     for i in range(len(labels)):
        #         if labels[i] == 0:
        #             labels[i] = 'black'
        #         elif labels[i] == 1:
        #             labels[i] = 'red'
        #         elif labels[i] == 2:
        #             labels[i] = 'green'
        #         else:
        #             labels[i] = 'blue'
            self.plotWidget.canvas.axes.scatter(x_vals, y_vals, z_vals, 'o', picker=5, c=labels)
        else:
            self.plotWidget.canvas.axes.scatter(x_vals, y_vals, z_vals, 'o', picker=5)
            # ax.annotate(names[i], (x_vals[i], y_vals[i]))
        cid = self.plotWidget.canvas.axes.figure.canvas.mpl_connect('pick_event',
                                                                    lambda event: self.onpick(event, names))
        self.labels = labels
        self.plotWidget.canvas.draw()

    def cluster_data(self,features,names,num_clusters):
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=num_clusters, random_state=0, max_iter=1000, init='random', n_init=100).fit(features)
        labels = kmeans.labels_
        labels = labels.tolist()
        uniq = np.unique(labels)

        for i in range(num_clusters):
            self.cluster_lst[i] = list(np.where(np.array(labels)==i))
        return labels

    def refresh_plot(self):
        # print(int(self.coloringMode.isChecked()))

        file = self.load_data()
        data = self.pca_data(file)  # uncomment this when needed
        # file = load_data('C:\\Users\\Goko\\Desktop\\data.json')
        features, names, labels = self.partition_data(data, int(self.coloringMode.isChecked()))
        labels = self.cluster_data(features,names,self.numberOfClustersSpinBox.value())
        x_vals, y_vals, z_vals = self.tsne(features, names, labels)
        self.plot_tnse(x_vals, y_vals, z_vals, names, labels, int(self.coloringMode.isChecked()))


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 900)
        MainWindow.setStyleSheet("QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #ffa02f;\n"
"     padding: 1px;\n"
"     border-radius: 3px;\n"
"     opacity: 100;\n"
"}\n"
"\n"
"QWidget\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    font-family: \"Lucida Sans Unicode\", \"Lucida Grande\", sans-serif;\n"
"    font:16px;\n"
"\n"
"}\n"
"\n"
"QTreeView, QListView\n"
"{\n"
"    background-color: silver;\n"
"    margin-left: 5px;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background: transparent;\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #212121,\n"
"        stop:0.4 #343434/*,\n"
"        stop:0.2 #343434,\n"
"        stop:0.1 #ffaa00*/\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #808080;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"}\n"
"\n"
"QWidget:focus\n"
"{\n"
"    /*border: 1px solid darkgray;*/\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #1e1e1e;\n"
"    border-style: solid;\n"
"    border-radius: 6;\n"
"    padding: 3px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    min-width: 40px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    selection-background-color: #ffaa00;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:/dark_orange/img/down_arrow.png);\n"
"}\n"
"\n"
"QGroupBox\n"
"{\n"
"    border: 1px solid darkgray;\n"
"    margin-top: 10px;\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"    border: 1px solid darkgray;\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 1px solid darkgray;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"QCheckBox:disabled\n"
"{\n"
"color: #414141;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #242424;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the tool bar */\n"
"     background: url(:/dark_orange/img/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #d7801a;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #ffaa00;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"}\n"
"\n"
"QCheckBox::indicator{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
"{\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    image:url(:/dark_orange/img/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #444;\n"
"}\n"
"\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #3A3939;\n"
"    height: 8px;\n"
"    background: #201F1F;\n"
"    margin: 2px 0;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,\n"
"      stop: 0.0 silver, stop: 0.2 #a8a8a8, stop: 1 #727272);\n"
"    border: 1px solid #3A3939;\n"
"    width: 14px;\n"
"    height: 14px;\n"
"    margin: -4px 0;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border: 1px solid #3A3939;\n"
"    width: 8px;\n"
"    background: #201F1F;\n"
"    margin: 0 0px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 silver,\n"
"      stop: 0.2 #a8a8a8, stop: 1 #727272);\n"
"    border: 1px solid #3A3939;\n"
"    width: 14px;\n"
"    height: 14px;\n"
"    margin: 0 -4px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QAbstractSpinBox {\n"
"    padding-top: 2px;\n"
"    padding-bottom: 2px;\n"
"    border: 1px solid darkgray;\n"
"\n"
"    border-radius: 2px;\n"
"    min-width: 50px;\n"
"}")
        dataset = Dataset.Dataset(name='', json_path=config.argument_defaults['video_data_path']
                                  .format(config.argument_defaults['poc_mode']))
        self.mediaPlayerOriginal = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c1v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c1v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c1v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c2v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c2v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c2v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c3v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c3v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c3v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c4v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c4v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c4v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c5v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c5v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c5v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c6v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c6v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c6v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c7v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c7v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c7v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c8v1MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c8v2MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.c8v3MediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.mediaPlayerPanoptic = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.pause_icon = MainWindow.style().standardIcon(QStyle.SP_MediaPause)
        self.play_icon = MainWindow.style().standardIcon(QStyle.SP_MediaPlay)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.toolboxLayout = QtWidgets.QHBoxLayout()
        self.toolboxLayout.setObjectName("toolboxLayout")
        self.addvideoButton = QtWidgets.QPushButton(self.centralwidget)
        self.addvideoButton.setObjectName("addvideoButton")
        self.toolboxLayout.addWidget(self.addvideoButton)
        self.savePlotButton = QtWidgets.QPushButton(self.centralwidget)
        self.savePlotButton.setObjectName("savePlotButton")
        self.toolboxLayout.addWidget(self.savePlotButton)
        self.singleViewButton = QtWidgets.QPushButton(self.centralwidget)
        self.singleViewButton.setObjectName("singleViewButton")
        self.toolboxLayout.addWidget(self.singleViewButton)
        self.clusterViewButton = QtWidgets.QPushButton(self.centralwidget)
        self.clusterViewButton.setObjectName("clusterViewButton")
        self.toolboxLayout.addWidget(self.clusterViewButton)
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setObjectName("settingsButton")
        self.toolboxLayout.addWidget(self.settingsButton)
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setObjectName("helpButton")
        self.toolboxLayout.addWidget(self.helpButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.toolboxLayout.addItem(spacerItem)
        self.sceneComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.sceneComboBox.setObjectName("sceneComboBox")
        self.sceneComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.sceneComboBox.setMinimumContentsLength(20)


        self.sceneComboBox.addItem("")
        self.sceneComboBox.addItems(sorted(ntpath.basename(videoData.video_path) for videoData in dataset.videos))
        self.sceneComboBox.currentTextChanged.connect(self.openVideo)

        self.toolboxLayout.addWidget(self.sceneComboBox)
        self.verticalLayout_5.addLayout(self.toolboxLayout)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_5.addWidget(self.line_5)
        self.mainScreenLayout = QtWidgets.QHBoxLayout()
        self.mainScreenLayout.setObjectName("mainScreenLayout")
        self.plotAreaLayout = QtWidgets.QVBoxLayout()
        self.plotAreaLayout.setObjectName("plotAreaLayout")
        self.plotWidget = MplWidget(self.centralwidget)
        sizePolicyPlot = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicyPlot.setHorizontalStretch(0)
        sizePolicyPlot.setVerticalStretch(0)
        sizePolicyPlot.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicyPlot)
        self.plotWidget.setMinimumSize(QtCore.QSize(300, 300))
        self.plotWidget.setMaximumSize(QtCore.QSize(600, 600))
        self.plotWidget.setObjectName("plotWidget")
        self.plotAreaLayout.addWidget(self.plotWidget)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.plotAreaLayout.addWidget(self.line_3)
        self.formAreaLayout = QtWidgets.QHBoxLayout()
        self.formAreaLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.formAreaLayout.setObjectName("formAreaLayout")
        self.tsneParamForm = QtWidgets.QFormLayout()
        self.tsneParamForm.setObjectName("tsneParamForm")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Unicode,Lucida Grande,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tsneParamForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.iterationsLabel = QtWidgets.QLabel(self.centralwidget)
        self.iterationsLabel.setObjectName("iterationsLabel")
        self.tsneParamForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.iterationsLabel)
        self.iterationsSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.iterationsSpinBox.setMinimum(250)
        self.iterationsSpinBox.setMaximum(10000)
        self.iterationsSpinBox.setSingleStep(5)
        self.iterationsSpinBox.setProperty("value", 1000)
        self.iterationsSpinBox.setDisplayIntegerBase(10)
        self.iterationsSpinBox.setObjectName("iterationsSpinBox")
        self.tsneParamForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.iterationsSpinBox)
        self.perplexityLabel = QtWidgets.QLabel(self.centralwidget)
        self.perplexityLabel.setObjectName("perplexityLabel")
        self.tsneParamForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.perplexityLabel)
        self.perplexitySpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.perplexitySpinBox.setSizePolicy(sizePolicyPlot)
        self.perplexitySpinBox.setMinimum(2)
        self.perplexitySpinBox.setMaximum(50)
        self.perplexitySpinBox.setProperty("value", 30)
        self.perplexitySpinBox.setObjectName("perplexitySpinBox")

        self.tsneParamForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.perplexitySpinBox)
        self.earlyExaggerationLabel = QtWidgets.QLabel(self.centralwidget)
        self.earlyExaggerationLabel.setObjectName("earlyExaggerationLabel")
        self.tsneParamForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.earlyExaggerationLabel)
        self.earlyExaggerationSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.earlyExaggerationSpinBox.setProperty("value", 5)

        self.earlyExaggerationSpinBox.setObjectName("earlyExaggerationSpinBox")
        self.tsneParamForm.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.earlyExaggerationSpinBox)
        self.learningRateLabel = QtWidgets.QLabel(self.centralwidget)
        self.learningRateLabel.setObjectName("learningRateLabel")
        self.tsneParamForm.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.learningRateLabel)
        self.learningRateSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.learningRateSpinBox.setMinimum(10)
        self.learningRateSpinBox.setMaximum(1000)
        self.learningRateSpinBox.setProperty("value", 20)
        self.learningRateSpinBox.setDisplayIntegerBase(10)
        self.learningRateSpinBox.setObjectName("learningRateSpinBox")
        self.tsneParamForm.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.learningRateSpinBox)
        self.formAreaLayout.addLayout(self.tsneParamForm)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.formAreaLayout.addWidget(self.line_4)
        self.clusteringParamForm = QtWidgets.QFormLayout()
        self.clusteringParamForm.setObjectName("clusteringParamForm")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Unicode,Lucida Grande,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.clusteringParamForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.numberOfComponentsLabel = QtWidgets.QLabel(self.centralwidget)
        self.numberOfComponentsLabel.setObjectName("numberOfComponentsLabel")
        self.clusteringParamForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.numberOfComponentsLabel)
        self.numberOfComponentsSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.numberOfComponentsSpinBox.setMinimum(10)
        self.numberOfComponentsSpinBox.setMaximum(50)
        self.numberOfComponentsSpinBox.setProperty("value", 30)
        self.numberOfComponentsSpinBox.setObjectName("numberOfComponentsSpinBox")
        self.clusteringParamForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.numberOfComponentsSpinBox)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.clusteringParamForm.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.line_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Unicode,Lucida Grande,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.clusteringParamForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.numberOfClustersLabel = QtWidgets.QLabel(self.centralwidget)
        self.numberOfClustersLabel.setObjectName("numberOfClustersLabel")
        self.clusteringParamForm.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.numberOfClustersLabel)
        self.numberOfClustersSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.numberOfClustersSpinBox.setSizePolicy(sizePolicyPlot)
        self.numberOfClustersSpinBox.setMinimum(2)
        self.numberOfClustersSpinBox.setMaximum(8)
        self.numberOfClustersSpinBox.setProperty("value", 3)
        self.numberOfClustersSpinBox.setObjectName("numberOfClustersSpinBox")
        self.clusteringParamForm.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.numberOfClustersSpinBox)
        self.coloringModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.coloringModeLabel.setObjectName("coloringModeLabel")
        self.clusteringParamForm.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.coloringModeLabel)
        self.coloringMode = QtWidgets.QRadioButton(self.centralwidget)
        self.coloringMode.setObjectName("coloringMode")
        self.clusteringParamForm.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.coloringMode)
        self.formAreaLayout.addLayout(self.clusteringParamForm)
        self.plotAreaLayout.addLayout(self.formAreaLayout)
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setObjectName("refreshButton")
        self.plotAreaLayout.addWidget(self.refreshButton)
        self.mainScreenLayout.addLayout(self.plotAreaLayout)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.mainScreenLayout.addWidget(self.line_7)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.clusterViewPage = QtWidgets.QWidget()
        self.clusterViewPage.setObjectName("clusterViewPage")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.clusterViewPage)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.clusterViewPage)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 638, 1168))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.randomSampleButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.randomSampleButton.setObjectName("randomSampleButton")

        self.panopticOptionRadio = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
        self.panopticOptionRadio.setObjectName("panopticOptionRadio")

        self.controlsHorizontal = QtWidgets.QHBoxLayout()
        self.controlsHorizontal.setObjectName("controlsHorizontal")
        self.controlsHorizontal.addWidget(self.panopticOptionRadio)

        self.controlsHorizontal.addWidget(self.randomSampleButton)
        self.verticalLayout_7.addLayout(self.controlsHorizontal)
        self.cluster1_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster1_label.setObjectName("cluster1_label")
        self.verticalLayout_7.addWidget(self.cluster1_label)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cluster1video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster1video1.sizePolicy().hasHeightForWidth())
        self.cluster1video1.setSizePolicy(sizePolicy)
        self.cluster1video1.setMinimumSize(QtCore.QSize(290, 200))
        self.cluster1video1.setObjectName("widget_3")
        self.horizontalLayout_6.addWidget(self.cluster1video1)
        self.cluster1video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster1video2.sizePolicy().hasHeightForWidth())
        self.cluster1video2.setSizePolicy(sizePolicy)
        self.cluster1video2.setMinimumSize(QtCore.QSize(290, 200))
        self.cluster1video2.setObjectName("widget_4")
        self.horizontalLayout_6.addWidget(self.cluster1video2)
        self.cluster1video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster1video3.sizePolicy().hasHeightForWidth())
        self.cluster1video3.setSizePolicy(sizePolicy)
        self.cluster1video3.setMinimumSize(QtCore.QSize(290, 200))
        self.cluster1video3.setObjectName("widget_5")
        self.horizontalLayout_6.addWidget(self.cluster1video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.cluster2_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster2_label.setObjectName("cluster2_label")
        self.verticalLayout_7.addWidget(self.cluster2_label)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cluster2video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster2video1.sizePolicy().hasHeightForWidth())
        self.cluster2video1.setSizePolicy(sizePolicy)
        self.cluster2video1.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster2video1.setObjectName("widget_6")
        self.horizontalLayout_7.addWidget(self.cluster2video1)
        self.cluster2video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster2video2.sizePolicy().hasHeightForWidth())
        self.cluster2video2.setSizePolicy(sizePolicy)
        self.cluster2video2.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster2video2.setObjectName("widget_7")
        self.horizontalLayout_7.addWidget(self.cluster2video2)
        self.cluster2video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster2video3.sizePolicy().hasHeightForWidth())
        self.cluster2video3.setSizePolicy(sizePolicy)
        self.cluster2video3.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster2video3.setObjectName("widget_8")
        self.horizontalLayout_7.addWidget(self.cluster2video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.cluster3_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster3_label.setObjectName("cluster3_label")
        self.verticalLayout_7.addWidget(self.cluster3_label)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.cluster3video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster3video1.sizePolicy().hasHeightForWidth())
        self.cluster3video1.setSizePolicy(sizePolicy)
        self.cluster3video1.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster3video1.setObjectName("widget_15")
        self.horizontalLayout_10.addWidget(self.cluster3video1)
        self.cluster3video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster3video2.sizePolicy().hasHeightForWidth())
        self.cluster3video2.setSizePolicy(sizePolicy)
        self.cluster3video2.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster3video2.setObjectName("widget_16")
        self.horizontalLayout_10.addWidget(self.cluster3video2)
        self.cluster3video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster3video3.sizePolicy().hasHeightForWidth())
        self.cluster3video3.setSizePolicy(sizePolicy)
        self.cluster3video3.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster3video3.setObjectName("widget_17")
        self.horizontalLayout_10.addWidget(self.cluster3video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.cluster4_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster4_label.setObjectName("cluster4_label")
        self.verticalLayout_7.addWidget(self.cluster4_label)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cluster4video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster4video1.sizePolicy().hasHeightForWidth())
        self.cluster4video1.setSizePolicy(sizePolicy)
        self.cluster4video1.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster4video1.setObjectName("widget_9")
        self.horizontalLayout_8.addWidget(self.cluster4video1)
        self.cluster4video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster4video2.sizePolicy().hasHeightForWidth())
        self.cluster4video2.setSizePolicy(sizePolicy)
        self.cluster4video2.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster4video2.setObjectName("widget_10")
        self.horizontalLayout_8.addWidget(self.cluster4video2)
        self.cluster4video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster4video3.sizePolicy().hasHeightForWidth())
        self.cluster4video3.setSizePolicy(sizePolicy)
        self.cluster4video3.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster4video3.setObjectName("widget_11")
        self.horizontalLayout_8.addWidget(self.cluster4video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.cluster5_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster5_label.setObjectName("cluster5_label")
        self.verticalLayout_7.addWidget(self.cluster5_label)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.cluster5video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster5video1.sizePolicy().hasHeightForWidth())
        self.cluster5video1.setSizePolicy(sizePolicy)
        self.cluster5video1.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster5video1.setObjectName("widget_12")
        self.horizontalLayout_9.addWidget(self.cluster5video1)
        self.cluster5video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster5video2.sizePolicy().hasHeightForWidth())
        self.cluster5video2.setSizePolicy(sizePolicy)
        self.cluster5video2.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster5video2.setObjectName("widget_13")
        self.horizontalLayout_9.addWidget(self.cluster5video2)
        self.cluster5video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster5video3.sizePolicy().hasHeightForWidth())
        self.cluster5video3.setSizePolicy(sizePolicy)
        self.cluster5video3.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster5video3.setObjectName("widget_14")
        self.horizontalLayout_9.addWidget(self.cluster5video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.cluster6_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster6_label.setObjectName("cluster6_label")
        self.verticalLayout_7.addWidget(self.cluster6_label)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.cluster6video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster6video1.sizePolicy().hasHeightForWidth())
        self.cluster6video1.setSizePolicy(sizePolicy)
        self.cluster6video1.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster6video1.setObjectName("cluster6video1")
        self.horizontalLayout_11.addWidget(self.cluster6video1)
        self.cluster6video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster6video2.sizePolicy().hasHeightForWidth())
        self.cluster6video2.setSizePolicy(sizePolicy)
        self.cluster6video2.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster6video2.setObjectName("cluster6video2")
        self.horizontalLayout_11.addWidget(self.cluster6video2)
        self.cluster6video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster6video3.sizePolicy().hasHeightForWidth())
        self.cluster6video3.setSizePolicy(sizePolicy)
        self.cluster6video3.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster6video3.setObjectName("widget_17")
        self.horizontalLayout_11.addWidget(self.cluster6video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)

        self.cluster7_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster7_label.setObjectName("label_10")
        self.verticalLayout_7.addWidget(self.cluster7_label)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.cluster7video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster7video1.sizePolicy().hasHeightForWidth())
        self.cluster7video1.setSizePolicy(sizePolicy)
        self.cluster7video1.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster7video1.setObjectName("cluster7video1")
        self.horizontalLayout_12.addWidget(self.cluster7video1)
        self.cluster7video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster7video2.sizePolicy().hasHeightForWidth())
        self.cluster7video2.setSizePolicy(sizePolicy)
        self.cluster7video2.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster7video2.setObjectName("cluster7video2")
        self.horizontalLayout_12.addWidget(self.cluster7video2)
        self.cluster7video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster7video3.sizePolicy().hasHeightForWidth())
        self.cluster7video3.setSizePolicy(sizePolicy)
        self.cluster7video3.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster7video3.setObjectName("widget_17")
        self.horizontalLayout_12.addWidget(self.cluster7video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.cluster8_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cluster8_label.setObjectName("label_11")
        self.verticalLayout_7.addWidget(self.cluster8_label)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.cluster8video1 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster8video1.sizePolicy().hasHeightForWidth())
        self.cluster8video1.setSizePolicy(sizePolicy)
        self.cluster8video1.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster8video1.setObjectName("cluster8video1")
        self.horizontalLayout_13.addWidget(self.cluster8video1)
        self.cluster8video2 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster8video2.sizePolicy().hasHeightForWidth())
        self.cluster8video2.setSizePolicy(sizePolicy)
        self.cluster8video2.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster8video2.setObjectName("cluster8video2")
        self.horizontalLayout_13.addWidget(self.cluster8video2)
        self.cluster8video3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cluster8video3.sizePolicy().hasHeightForWidth())
        self.cluster8video3.setSizePolicy(sizePolicy)
        self.cluster8video3.setMinimumSize(QtCore.QSize(280, 200))
        self.cluster8video3.setObjectName("widget_17")
        self.horizontalLayout_13.addWidget(self.cluster8video3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_13)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_5.addWidget(self.scrollArea)
        self.stackedWidget.addWidget(self.clusterViewPage)
        self.singleViewPage = QtWidgets.QWidget()
        self.singleViewPage.setObjectName("singleViewPage")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.singleViewPage)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        originalVideoWidget = QVideoWidget(self.singleViewPage)
        sizePolicyOriginal = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicyOriginal.setHorizontalStretch(0)
        sizePolicyOriginal.setVerticalStretch(0)
        sizePolicyOriginal.setHeightForWidth(originalVideoWidget.sizePolicy().hasHeightForWidth())
        originalVideoWidget.setSizePolicy(sizePolicyOriginal)
        originalVideoWidget.setMinimumSize(QtCore.QSize(300, 300))
        originalVideoWidget.setObjectName("originalVideoWidget")
        self.verticalLayout_6.addWidget(originalVideoWidget)
        self.line_6 = QtWidgets.QFrame(self.singleViewPage)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_6.addWidget(self.line_6)
        panopticVideoWidget = QVideoWidget(self.singleViewPage)
        sizePolicyPanoptic = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicyPanoptic.setHorizontalStretch(0)
        sizePolicyPanoptic.setVerticalStretch(0)
        sizePolicyPanoptic.setHeightForWidth(panopticVideoWidget.sizePolicy().hasHeightForWidth())
        panopticVideoWidget.setSizePolicy(sizePolicyPanoptic)
        panopticVideoWidget.setMinimumSize(QtCore.QSize(300, 300))
        panopticVideoWidget.setObjectName("panopticVideoWidget")
        self.verticalLayout_6.addWidget(panopticVideoWidget)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.playButton = QtWidgets.QPushButton(self.singleViewPage)
        self.playButton.setText("")
        self.playButton.setObjectName("playButton")
        self.playButton.setEnabled(False)
        self.playButton.setIcon(MainWindow.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.horizontalLayout_4.addWidget(self.playButton)
        self.progressBar = QSlider(self.singleViewPage)
        self.progressBar.setRange(0, 0)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.sliderMoved.connect(self.setPosition)
        self.refreshButton.clicked.connect(self.refresh_plot)

        self.horizontalLayout_4.addWidget(self.progressBar)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.stackedWidget.addWidget(self.singleViewPage)
        self.mainScreenLayout.addWidget(self.stackedWidget)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.mainScreenLayout.addWidget(self.line)
        self.verticalLayout_5.addLayout(self.mainScreenLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        self.mediaPlayerOriginal.setVideoOutput(originalVideoWidget)

        self.c1v1MediaPlayer.setVideoOutput(self.cluster1video1)
        self.c1v2MediaPlayer.setVideoOutput(self.cluster1video2)
        self.c1v3MediaPlayer.setVideoOutput(self.cluster1video3)

        self.c1row = []
        self.c1row.append(self.c1v1MediaPlayer)
        self.c1row.append(self.c1v2MediaPlayer)
        self.c1row.append(self.c1v3MediaPlayer)

        self.cluster1videoWidgets = []
        self.cluster1videoWidgets.append(self.cluster1video1)
        self.cluster1videoWidgets.append(self.cluster1video2)
        self.cluster1videoWidgets.append(self.cluster1video3)


        self.c2v1MediaPlayer.setVideoOutput(self.cluster2video1)
        self.c2v2MediaPlayer.setVideoOutput(self.cluster2video2)
        self.c2v3MediaPlayer.setVideoOutput(self.cluster2video3)

        self.c2row = []
        self.c2row.append(self.c2v1MediaPlayer)
        self.c2row.append(self.c2v2MediaPlayer)
        self.c2row.append(self.c2v3MediaPlayer)

        self.cluster2videoWidgets = []
        self.cluster2videoWidgets.append(self.cluster2video1)
        self.cluster2videoWidgets.append(self.cluster2video2)
        self.cluster2videoWidgets.append(self.cluster2video3)

        self.c3v1MediaPlayer.setVideoOutput(self.cluster3video1)
        self.c3v2MediaPlayer.setVideoOutput(self.cluster3video2)
        self.c3v3MediaPlayer.setVideoOutput(self.cluster3video3)

        self.c3row = []
        self.c3row.append(self.c3v1MediaPlayer)
        self.c3row.append(self.c3v2MediaPlayer)
        self.c3row.append(self.c3v3MediaPlayer)

        self.cluster3videoWidgets = []
        self.cluster3videoWidgets.append(self.cluster3video1)
        self.cluster3videoWidgets.append(self.cluster3video2)
        self.cluster3videoWidgets.append(self.cluster3video3)

        self.c4v1MediaPlayer.setVideoOutput(self.cluster4video1)
        self.c4v2MediaPlayer.setVideoOutput(self.cluster4video2)
        self.c4v3MediaPlayer.setVideoOutput(self.cluster4video3)

        self.c4row = []
        self.c4row.append(self.c4v1MediaPlayer)
        self.c4row.append(self.c4v2MediaPlayer)
        self.c4row.append(self.c4v3MediaPlayer)

        self.cluster4videoWidgets = []
        self.cluster4videoWidgets.append(self.cluster4video1)
        self.cluster4videoWidgets.append(self.cluster4video2)
        self.cluster4videoWidgets.append(self.cluster4video3)



        self.c5v1MediaPlayer.setVideoOutput(self.cluster5video1)
        self.c5v2MediaPlayer.setVideoOutput(self.cluster5video2)
        self.c5v3MediaPlayer.setVideoOutput(self.cluster5video3)

        self.c5row = []
        self.c5row.append(self.c5v1MediaPlayer)
        self.c5row.append(self.c5v2MediaPlayer)
        self.c5row.append(self.c5v3MediaPlayer)

        self.cluster5videoWidgets = []
        self.cluster5videoWidgets.append(self.cluster5video1)
        self.cluster5videoWidgets.append(self.cluster5video2)
        self.cluster5videoWidgets.append(self.cluster5video3)

        self.c6v1MediaPlayer.setVideoOutput(self.cluster6video1)
        self.c6v2MediaPlayer.setVideoOutput(self.cluster6video2)
        self.c6v3MediaPlayer.setVideoOutput(self.cluster6video3)

        self.c6row = []
        self.c6row.append(self.c6v1MediaPlayer)
        self.c6row.append(self.c6v2MediaPlayer)
        self.c6row.append(self.c6v3MediaPlayer)

        self.cluster6videoWidgets = []
        self.cluster6videoWidgets.append(self.cluster6video1)
        self.cluster6videoWidgets.append(self.cluster6video2)
        self.cluster6videoWidgets.append(self.cluster6video3)

        self.c7v1MediaPlayer.setVideoOutput(self.cluster7video1)
        self.c7v2MediaPlayer.setVideoOutput(self.cluster7video2)
        self.c7v3MediaPlayer.setVideoOutput(self.cluster7video3)

        self.c7row = []
        self.c7row.append(self.c7v1MediaPlayer)
        self.c7row.append(self.c7v2MediaPlayer)
        self.c7row.append(self.c7v3MediaPlayer)

        self.cluster7videoWidgets = []
        self.cluster7videoWidgets.append(self.cluster7video1)
        self.cluster7videoWidgets.append(self.cluster7video2)
        self.cluster7videoWidgets.append(self.cluster7video3)


        self.c8v1MediaPlayer.setVideoOutput(self.cluster8video1)
        self.c8v2MediaPlayer.setVideoOutput(self.cluster8video2)
        self.c8v3MediaPlayer.setVideoOutput(self.cluster8video3)

        self.c8row = []
        self.c8row.append(self.c8v1MediaPlayer)
        self.c8row.append(self.c8v2MediaPlayer)
        self.c8row.append(self.c8v3MediaPlayer)

        self.cluster8videoWidgets = []
        self.cluster8videoWidgets.append(self.cluster8video1)
        self.cluster8videoWidgets.append(self.cluster8video2)
        self.cluster8videoWidgets.append(self.cluster8video3)


        self.cvplayers = []

        self.cvplayers.append(self.c1row)
        self.cvplayers.append(self.c2row)
        self.cvplayers.append(self.c3row)
        self.cvplayers.append(self.c4row)
        self.cvplayers.append(self.c5row)
        self.cvplayers.append(self.c6row)
        self.cvplayers.append(self.c7row)
        self.cvplayers.append(self.c8row)

        self.videoWidgets = []

        self.videoWidgets.append(self.cluster1videoWidgets)
        self.videoWidgets.append(self.cluster2videoWidgets)
        self.videoWidgets.append(self.cluster3videoWidgets)
        self.videoWidgets.append(self.cluster4videoWidgets)
        self.videoWidgets.append(self.cluster5videoWidgets)
        self.videoWidgets.append(self.cluster6videoWidgets)
        self.videoWidgets.append(self.cluster7videoWidgets)
        self.videoWidgets.append(self.cluster8videoWidgets)

        self.mediaPlayerPanoptic.setVideoOutput(panopticVideoWidget)
        self.mediaPlayerOriginal.positionChanged.connect(self.positionChanged)
        self.mediaPlayerOriginal.durationChanged.connect(self.durationChanged)
        self.randomSampleButton.clicked.connect(self.showClusterVideos)

        self.adderWin = QtWidgets.QMainWindow()
        self.adder = Ui_Dialog()
        self.addvideoButton.clicked.connect(self.openAdder)


        self.helpButton.clicked.connect(self.openHelper)



        self.clusterViewButton.clicked.connect(self.setUpClusterView)
        self.singleViewButton.clicked.connect(self.setUpSingleView)
        self.savePlotButton.clicked.connect(self.savePlot)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.ind = -1
        self.old_ind = -1
        self.color = ['red', 'blue', 'green', 'purple', 'yellow', 'magenta', 'cyan',
                 'black']
        self.names = []

        self.cluster1= []
        self.cluster2= []
        self.cluster3= []
        self.cluster4= []
        self.cluster5= []
        self.cluster6= []
        self.cluster7= []
        self.cluster8= []


        self.cluster_lst = []
        self.cluster_lst.append(self.cluster1)
        self.cluster_lst.append(self.cluster2)
        self.cluster_lst.append(self.cluster3)
        self.cluster_lst.append(self.cluster4)
        self.cluster_lst.append(self.cluster5)
        self.cluster_lst.append(self.cluster6)
        self.cluster_lst.append(self.cluster7)
        self.cluster_lst.append(self.cluster8)

        self.cluster_label_list = []
        self.cluster_label_list.append(self.cluster1_label)
        self.cluster_label_list.append(self.cluster2_label)
        self.cluster_label_list.append(self.cluster3_label)
        self.cluster_label_list.append(self.cluster4_label)
        self.cluster_label_list.append(self.cluster5_label)
        self.cluster_label_list.append(self.cluster6_label)
        self.cluster_label_list.append(self.cluster7_label)
        self.cluster_label_list.append(self.cluster8_label)




    def play(self):
        if self.mediaPlayerOriginal.state() == QMediaPlayer.PlayingState:
            self.mediaPlayerOriginal.pause()
            self.playButton.setIcon(self.play_icon)

            self.mediaPlayerPanoptic.pause()
        else:
            self.mediaPlayerOriginal.play()
            self.playButton.setIcon(self.pause_icon)

            self.mediaPlayerPanoptic.play()


    def positionChanged(self, position):
        self.progressBar.setValue(position)

    def durationChanged(self, duration):
        self.progressBar.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayerPanoptic.setPosition(position)
        self.mediaPlayerOriginal.setPosition(position)

    def openAdder(self):

        self.adder.setupUi(self.adderWin)
        self.adderWin.show()

    def adder_t(self):
        th3 = threading.Thread(target=self.openAdder)
        ad['threads'].append(th3)
        th3.start()

    def openHelper(self):
        self.helperWin = QtWidgets.QDialog()
        self.helper = Ui_HelperDialog()
        self.helper.setupUi(self.helperWin)
        self.helperWin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.helperWin.show()

    def helper_t(self):
        th4 = threading.Thread(target=self.openHelper())
        ad['threads'].append(th4)
        th4.start()

    def openSettings(self):
        self.settingsWin = QtWidgets.QDialog()
        self.settings = Ui_SettingsDialog(config.argument_defaults)
        self.helper.setupUi(self.helperWin)
        self.helperWin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.helperWin.show()


    def openVideo(self, text):
        if self.plotWidget.canvas.axes.collections:
            if self.ind>=0:
                col = c.to_rgba(self.labels[self.ind])
                self.plotWidget.canvas.axes.collections[0]._facecolor3d[
                self.ind, :] = col
                self.plotWidget.canvas.axes.collections[0]._edgecolor3d[
                self.ind, :] = col
            print("figure is on")
            self.ind = self.names.index(text)
            self.plotWidget.canvas.axes.collections[0]._facecolor3d[self.ind,:] = (1, 1, 1, 1)
            self.plotWidget.canvas.axes.collections[0]._edgecolor3d[self.ind,:] = (1, 1, 1, 1)
            self.plotWidget.canvas.draw()

        else:
            print("no figure there son")

        fileName = config.argument_defaults['export_path'] + '/' + text
        panopticFilename = config.argument_defaults[
                               'output_path'] + '/' + text

        if fileName != config.argument_defaults[
            'export_path'] + '/' + 'Select video...':
            self.mediaPlayerOriginal.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.mediaPlayerPanoptic.setMedia(
                QMediaContent(QUrl.fromLocalFile(panopticFilename)))
            self.playButton.setEnabled(True)



    def showClusterVideos(self):
        fileName= 'C:/Users/Asli/Desktop/videolar'+'/'+'scene-0001.mp4'
        source = config.argument_defaults['output_path'] if self.panopticOptionRadio.isChecked() else config.argument_defaults['export_path']


        num_cluster = self.numberOfClustersSpinBox.value()
        import random
        seqs = []
        for i in range(num_cluster):
            seq = random.sample(list(self.cluster_lst[i][0]),3)
            #TODO: output and export must bechangable near the generate sample buttton
            self.cvplayers[i][0].setMedia(QMediaContent(QUrl.fromLocalFile(source+'/'+self.names[seq[0]])))
            self.cvplayers[i][1].setMedia(QMediaContent(QUrl.fromLocalFile(source+'/'+self.names[seq[1]])))
            self.cvplayers[i][2].setMedia(QMediaContent(QUrl.fromLocalFile(source+'/'+self.names[seq[2]])))


        for i in range(8-num_cluster):
            self.cluster_label_list[7-i].setVisible(False)
            self.videoWidgets[7-i][0].setVisible(False)
            self.videoWidgets[7-i][1].setVisible(False)
            self.videoWidgets[7-i][2].setVisible(False)

        for i in range(num_cluster):
            self.cluster_label_list[i].setVisible(True)
            self.cluster_label_list[i].setStyleSheet('color: '+self.color[i])
            self.videoWidgets[i][0].setVisible(True)
            self.videoWidgets[i][1].setVisible(True)
            self.videoWidgets[i][2].setVisible(True)

        self.c1v1MediaPlayer.play()
        self.c1v2MediaPlayer.play()
        self.c1v3MediaPlayer.play()
        self.c2v1MediaPlayer.play()
        self.c2v2MediaPlayer.play()
        self.c2v3MediaPlayer.play()
        self.c3v1MediaPlayer.play()
        self.c3v2MediaPlayer.play()
        self.c3v3MediaPlayer.play()
        self.c4v1MediaPlayer.play()
        self.c4v2MediaPlayer.play()
        self.c4v3MediaPlayer.play()
        self.c5v1MediaPlayer.play()
        self.c5v2MediaPlayer.play()
        self.c5v3MediaPlayer.play()
        self.c6v1MediaPlayer.play()
        self.c6v2MediaPlayer.play()
        self.c6v3MediaPlayer.play()
        self.c7v1MediaPlayer.play()
        self.c7v2MediaPlayer.play()
        self.c7v3MediaPlayer.play()
        self.c8v1MediaPlayer.play()
        self.c8v2MediaPlayer.play()
        self.c8v3MediaPlayer.play()

    def savePlot(self):
        dateTimeObj = datetime.now()
        plot_name = config.argument_defaults['plot_output']+'/'+dateTimeObj.strftime("plot_%d_%b_%Y_%H_%M_%S.png")
        parameters_name = config.argument_defaults['plot_output']+'/'+ dateTimeObj.strftime("/parameters_%d_%b_%Y_%H_%M_%S.txt")
        metadata = {}
        metadata['Number Of Clusters'] = self.numberOfClustersSpinBox.value()
        metadata['Number of Iterations (t-SNE)'] = self.iterationsSpinBox.value()
        metadata['Perplexity (t-SNE)'] = self.perplexitySpinBox.value()
        metadata['Early Exaggeration (t-SNE)'] = self.earlyExaggerationSpinBox.value()
        metadata['Learning Rate (t-SNE)'] = self.learningRateSpinBox.value()
        metadata['Number Of PCA Components'] = self.numberOfComponentsSpinBox.value()

        fo = open(parameters_name, "w")

        for k, v in metadata.items():
            fo.write(str(k) + ': ' + str(v) + '\n')

        fo.close()
        self.plotWidget.canvas.figure.patch.set_visible(True)
        self.plotWidget.canvas.axes.patch.set_visible(True)
        self.plotWidget.canvas.figure.savefig(plot_name, transparent=False)
        self.plotWidget.canvas.figure.patch.set_visible(False)
        self.plotWidget.canvas.axes.patch.set_visible(False)
        self.plotWidget.canvas.draw()




    def setUpClusterView(self):
        self.sceneComboBox.setEnabled(False)
        self.stackedWidget.setCurrentIndex(0)
        self.clusterViewButton.setEnabled(False)
        self.singleViewButton.setEnabled(True)

    def setUpSingleView(self):
        self.sceneComboBox.setEnabled(True)
        self.stackedWidget.setCurrentIndex(1)
        self.clusterViewButton.setEnabled(True)
        self.singleViewButton.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addvideoButton.setText(_translate("MainWindow", "Add Video"))
        self.savePlotButton.setText(_translate("MainWindow", "Save Plot"))
        self.singleViewButton.setText(_translate("MainWindow", "Single View"))
        self.clusterViewButton.setText(_translate("MainWindow", "Cluster View"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))
        self.helpButton.setText(_translate("MainWindow", "Help"))
        self.sceneComboBox.setItemText(0, _translate("MainWindow", "Select scene.."))
        self.label.setText(_translate("MainWindow", "t-SNE Parameters"))
        self.iterationsLabel.setText(_translate("MainWindow", "Iterations"))
        self.perplexityLabel.setText(_translate("MainWindow", "Perplexity"))
        self.earlyExaggerationLabel.setText(_translate("MainWindow", "Early Exaggeration"))
        self.learningRateLabel.setText(_translate("MainWindow", "Learning Rate"))
        self.label_2.setText(_translate("MainWindow", "PCA Parameters"))
        self.numberOfComponentsLabel.setText(_translate("MainWindow", "Number of Components"))
        self.label_3.setText(_translate("MainWindow", "Clustering Parameters"))
        self.numberOfClustersLabel.setText(_translate("MainWindow", "Number of Clusters"))
        self.coloringModeLabel.setText(_translate("MainWindow", "Coloring mode"))
        self.refreshButton.setText(_translate("MainWindow", "Generate Plot"))
        self.cluster1_label.setText(_translate("MainWindow", "Cluster 1"))
        self.cluster2_label.setText(_translate("MainWindow", "Cluster 2"))
        self.cluster3_label.setText(_translate("MainWindow", "Cluster 3"))
        self.cluster4_label.setText(_translate("MainWindow", "Cluster 4"))
        self.cluster5_label.setText(_translate("MainWindow", "Cluster 5"))
        self.cluster6_label.setText(_translate("MainWindow", "Cluster 6"))
        self.cluster7_label.setText(_translate("MainWindow", "Cluster 7"))
        self.cluster8_label.setText(_translate("MainWindow", "Cluster 8"))
        self.randomSampleButton.setText(_translate("MainWindow", "Show Random Samples"))
        self.panopticOptionRadio.setText(_translate("MainWindow", "Show Segmented Versions"))

        self.setUpSingleView()
from visualizer.mplwidget import MplWidget

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    QApplication.processEvents()
    sys.exit(app.exec_())


if __name__ == "__main__":
    th2 = threading.Thread(target=main)
    th2.start()
    ad['threads'].append(th2)
    # for a in ad['threads']:
    #     a.join()
