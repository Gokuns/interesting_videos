# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mega_deneme.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


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
from config import argument_defaults as ad
matplotlib.use('Qt5Agg')
import threading
import matplotlib.colors as c

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
        return labels.tolist()

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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
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
        self.perplexitySpinBox.setSizePolicy(sizePolicy)
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
        self.numberOfClustersSpinBox.setSizePolicy(sizePolicy)
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
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.widget_3 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_6.addWidget(self.widget_3)
        self.widget_4 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_6.addWidget(self.widget_4)
        self.widget_5 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_6.addWidget(self.widget_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget_6 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_7.addWidget(self.widget_6)
        self.widget_7 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_7.addWidget(self.widget_7)
        self.widget_8 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.widget_8.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_7.addWidget(self.widget_8)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.widget_15 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_15.sizePolicy().hasHeightForWidth())
        self.widget_15.setSizePolicy(sizePolicy)
        self.widget_15.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_15.setObjectName("widget_15")
        self.horizontalLayout_10.addWidget(self.widget_15)
        self.widget_16 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_16.sizePolicy().hasHeightForWidth())
        self.widget_16.setSizePolicy(sizePolicy)
        self.widget_16.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_16.setObjectName("widget_16")
        self.horizontalLayout_10.addWidget(self.widget_16)
        self.widget_17 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_17.sizePolicy().hasHeightForWidth())
        self.widget_17.setSizePolicy(sizePolicy)
        self.widget_17.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_17.setObjectName("widget_17")
        self.horizontalLayout_10.addWidget(self.widget_17)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.widget_9 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy)
        self.widget_9.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_8.addWidget(self.widget_9)
        self.widget_10 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy)
        self.widget_10.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_10.setObjectName("widget_10")
        self.horizontalLayout_8.addWidget(self.widget_10)
        self.widget_11 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy)
        self.widget_11.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_8.addWidget(self.widget_11)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.widget_12 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_12.sizePolicy().hasHeightForWidth())
        self.widget_12.setSizePolicy(sizePolicy)
        self.widget_12.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_9.addWidget(self.widget_12)
        self.widget_13 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_13.sizePolicy().hasHeightForWidth())
        self.widget_13.setSizePolicy(sizePolicy)
        self.widget_13.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_13.setObjectName("widget_13")
        self.horizontalLayout_9.addWidget(self.widget_13)
        self.widget_14 = QVideoWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_14.sizePolicy().hasHeightForWidth())
        self.widget_14.setSizePolicy(sizePolicy)
        self.widget_14.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_9.addWidget(self.widget_14)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_5.addWidget(self.scrollArea)
        self.stackedWidget.addWidget(self.clusterViewPage)
        self.singleViewPage = QtWidgets.QWidget()
        self.singleViewPage.setObjectName("singleViewPage")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.singleViewPage)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        originalVideoWidget = QVideoWidget(self.singleViewPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(originalVideoWidget.sizePolicy().hasHeightForWidth())
        originalVideoWidget.setSizePolicy(sizePolicy)
        originalVideoWidget.setMinimumSize(QtCore.QSize(300, 300))
        originalVideoWidget.setObjectName("originalVideoWidget")
        self.verticalLayout_6.addWidget(originalVideoWidget)
        self.line_6 = QtWidgets.QFrame(self.singleViewPage)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_6.addWidget(self.line_6)
        panopticVideoWidget = QVideoWidget(self.singleViewPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(panopticVideoWidget.sizePolicy().hasHeightForWidth())
        panopticVideoWidget.setSizePolicy(sizePolicy)
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
        self.mediaPlayerPanoptic.setVideoOutput(panopticVideoWidget)
        self.mediaPlayerOriginal.positionChanged.connect(self.positionChanged)
        self.mediaPlayerOriginal.durationChanged.connect(self.durationChanged)

        self.adderWin = QtWidgets.QMainWindow()
        self.adder = Ui_Dialog()
        self.addvideoButton.clicked.connect(self.openAdder)


        self.clusterViewButton.clicked.connect(self.setUpClusterView)
        self.singleViewButton.clicked.connect(self.setUpSingleView)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.ind = -1
        self.old_ind = -1
        self.color = ['red', 'blue', 'green', 'purple', 'yellow', 'pink', 'cyan',
                 'black']
        self.names = []

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

        fileName= config.argument_defaults['export_path']+'/'+text
        panopticFilename = config.argument_defaults['output_path']+'/'+text

        if fileName != config.argument_defaults['export_path']+'/'+'Select video...':
            self.mediaPlayerOriginal.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.mediaPlayerPanoptic.setMedia(
                QMediaContent(QUrl.fromLocalFile(panopticFilename)))
            self.playButton.setEnabled(True)
            0

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
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "TextLabel"))
        self.setUpSingleView()
from visualizer.mplwidget import MplWidget

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    th2 = threading.Thread(target=main())
    th2.start()
    ad['threads'].append(th2)
    for a in ad['threads']:
        a.join()