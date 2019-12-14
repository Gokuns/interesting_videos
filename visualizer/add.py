# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
import cv2
import os
import _thread
import threading
import detectron2.demo.demo as demo

class Ui_Dialog(object):



    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 350)
        Dialog.setMaximumSize(QtCore.QSize(500, 350))
        Dialog.setMinimumSize(QtCore.QSize(500, 350))
        Dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog.setStyleSheet("QToolTip\n"
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
"    font:14px;\n"
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
"}\n"
"")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(0, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.stackedWidget = QtWidgets.QStackedWidget(Dialog)
        self.stackedWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(500, 350))
        self.stackedWidget.setMaximumSize(QtCore.QSize(530, 368))
        self.stackedWidget.setMouseTracking(False)
        self.stackedWidget.setToolTip("")
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.stackedWidget.setObjectName("stackedWidget")
        self.add_page = QtWidgets.QWidget()
        self.add_page.setObjectName("add_page")
        self.widget = QtWidgets.QWidget(self.add_page)
        self.widget.setGeometry(QtCore.QRect(1, 2, 491, 341))
        self.widget.setObjectName("widget")
        self.add_base_lay = QtWidgets.QVBoxLayout(self.widget)
        self.add_base_lay.setContentsMargins(2, 2, 0, 0)
        self.add_base_lay.setObjectName("add_base_lay")
        self.add_upper_lay = QtWidgets.QVBoxLayout()
        self.add_upper_lay.setObjectName("add_upper_lay")
        self.add_list_lay = QtWidgets.QHBoxLayout()
        self.add_list_lay.setContentsMargins(2, 2, -1, -1)
        self.add_list_lay.setObjectName("add_list_lay")
        self.list_view = QtWidgets.QListWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_view.sizePolicy().hasHeightForWidth())
        self.list_view.setSizePolicy(sizePolicy)
        self.list_view.setMinimumSize(QtCore.QSize(50, 0))
        self.list_view.setMaximumSize(QtCore.QSize(700, 500))
        self.list_view.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.list_view.setObjectName("list_view")
        self.add_list_lay.addWidget(self.list_view)
        self.add_buttons_lay = QtWidgets.QVBoxLayout()
        self.add_buttons_lay.setObjectName("add_buttons_lay")
        self.add_button = QtWidgets.QPushButton(self.widget)
        self.add_button.setMinimumSize(QtCore.QSize(52, 0))
        self.add_button.setMaximumSize(QtCore.QSize(85, 50))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon)
        self.add_button.setObjectName("add_button")
        self.add_buttons_lay.addWidget(self.add_button)
        self.remove_button = QtWidgets.QPushButton(self.widget)
        self.remove_button.setMinimumSize(QtCore.QSize(52, 0))
        self.remove_button.setMaximumSize(QtCore.QSize(85, 50))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_button.setIcon(icon1)
        self.remove_button.setObjectName("remove_button")
        self.add_buttons_lay.addWidget(self.remove_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.add_buttons_lay.addItem(spacerItem1)
        self.clear_button = QtWidgets.QPushButton(self.widget)
        self.clear_button.setMinimumSize(QtCore.QSize(52, 0))
        self.clear_button.setMaximumSize(QtCore.QSize(85, 50))
        self.clear_button.setObjectName("clear_button")
        self.add_buttons_lay.addWidget(self.clear_button)
        self.add_list_lay.addLayout(self.add_buttons_lay)
        self.add_upper_lay.addLayout(self.add_list_lay)


        #self.drag_drop = QtWidgets.QLabel(self.widget)
        #self.drag_drop.setAcceptDrops(True)
        self.drag_drop = self.Drag_label(self.widget,self.list_view)

        self.drag_drop.setMinimumSize(QtCore.QSize(0, 70))
        self.drag_drop.setFrameShape(QtWidgets.QFrame.Box)
        self.drag_drop.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.drag_drop.setLineWidth(1)
        self.drag_drop.setMidLineWidth(0)
        self.drag_drop.setTextFormat(QtCore.Qt.AutoText)
        self.drag_drop.setScaledContents(False)
        self.drag_drop.setAlignment(QtCore.Qt.AlignCenter)
        self.drag_drop.setWordWrap(False)
        self.drag_drop.setIndent(10)
        self.drag_drop.setOpenExternalLinks(False)
        self.drag_drop.setObjectName("drag_drop")
        self.add_upper_lay.addWidget(self.drag_drop)
        self.add_base_lay.addLayout(self.add_upper_lay)
        self.dialog_buttons = QtWidgets.QDialogButtonBox(self.widget)
        self.dialog_buttons.setOrientation(QtCore.Qt.Horizontal)
        self.dialog_buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialog_buttons.setObjectName("dialog_buttons")
        self.add_base_lay.addWidget(self.dialog_buttons)
        self.stackedWidget.addWidget(self.add_page)
        self.load_page = QtWidgets.QWidget()
        self.load_page.setObjectName("load_page")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.load_page)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.load_lay = QtWidgets.QVBoxLayout()
        self.load_lay.setContentsMargins(2, -1, -1, -1)
        self.load_lay.setObjectName("load_lay")
        self.load_upper_lay = QtWidgets.QVBoxLayout()
        self.load_upper_lay.setObjectName("load_upper_lay")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.load_upper_lay.addItem(spacerItem2)
        self.load_info_label = QtWidgets.QLabel(self.load_page)
        self.load_info_label.setMinimumSize(QtCore.QSize(0, 0))
        self.load_info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.load_info_label.setObjectName("load_info_label")
        self.load_upper_lay.addWidget(self.load_info_label)
        self.prog_bar = QtWidgets.QProgressBar(self.load_page)
        self.prog_bar.setProperty("value", 0)
        self.prog_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.prog_bar.setObjectName("prog_bar")
        self.load_upper_lay.addWidget(self.prog_bar)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.load_upper_lay.addItem(spacerItem3)
        self.load_lay.addLayout(self.load_upper_lay)
        self.load_button_box = QtWidgets.QDialogButtonBox(self.load_page)
        self.load_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Abort)
        self.load_button_box.setObjectName("load_button_box")
        self.load_lay.addWidget(self.load_button_box)
        self.horizontalLayout_4.addLayout(self.load_lay)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4.addLayout(self.horizontalLayout_6)
        self.stackedWidget.addWidget(self.load_page)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.widget1 = QtWidgets.QWidget(self.page_3)
        self.widget1.setGeometry(QtCore.QRect(10, 70, 491, 271))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.succ_info_label = QtWidgets.QLabel(self.widget1)
        self.succ_info_label.setAutoFillBackground(False)
        self.succ_info_label.setWordWrap(True)
        self.succ_info_label.setObjectName("succ_info_label")
        self.verticalLayout_5.addWidget(self.succ_info_label)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.finish_button = QtWidgets.QPushButton(self.widget1)
        self.finish_button.setObjectName("finish_button")
        self.horizontalLayout_3.addWidget(self.finish_button)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.stackedWidget.addWidget(self.page_3)
        self.horizontalLayout_5.addWidget(self.stackedWidget)
        spacerItem6 = QtWidgets.QSpacerItem(0, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)


        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.selected_item = None

        self.clear_button.clicked.connect(self.clear_items)
        self.remove_button.clicked.connect(self.remove_item)
        self.add_button.clicked.connect(self.open)
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.close_click)

        self.count = 0
        self.total_frame = 0



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add "))
        self.add_button.setText(_translate("Dialog", "Add"))
        self.remove_button.setText(_translate("Dialog", "Remove"))
        self.clear_button.setText(_translate("Dialog", "Clear"))
        self.drag_drop.setText(_translate("Dialog", "Drag and Drop Videos Here!"))
        self.load_info_label.setText(_translate("Dialog", "TextLabel"))
        self.succ_info_label.setText(_translate("Dialog", "Videos are added successfully."))
        self.finish_button.setText(_translate("Dialog", "Finish"))

    class Drag_label(QtWidgets.QLabel):

        def __init__(self,parent,listW):
            super().__init__(parent)
            self.listW = listW

            self.setAcceptDrops(True)

        def dragEnterEvent(self, event):
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()

        def dropEvent(self, event):
            files = [str(u.toLocalFile()) for u in event.mimeData().urls()]

            for vid in files:
                items = self.listW.findItems(vid, QtCore.Qt.MatchExactly)
                if len(items) > 0:
                    continue
                filename, file_extension = os.path.splitext(vid)
                if file_extension==".mp4":
                    self.listW.addItem(vid)


    def remove_item(self):
        self.list_view.takeItem(self.list_view.currentRow())

    def clear_items(self):
        self.list_view.clear()

    def open(self):
        fileName = QtWidgets.QFileDialog.getOpenFileNames(self.widget, 'OpenFile', '../', "Video Files (*.mp4)")
        if type(fileName[0]) == type([]):
            for vid in fileName[0]:
                items = self.list_view.findItems(vid, QtCore.Qt.MatchExactly)
                if len(items) > 0:
                    continue
                self.list_view.addItem(vid)

    def close_click(self):
        self.stackedWidget.close()

    def accept(self):
        for i in range(self.list_view.count()):
            vid = self.list_view.item(i)
            vid = str(vid.text())
            #print(vid)
            cap = cv2.VideoCapture(vid)
            self.total_frame += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #print(self.total_frame)
        if self.total_frame<=0:
            self.widget.close()
        #self.update_prog("asd", 2, 35, 232, 385,5)
        self.stackedWidget.setCurrentIndex(1)
        itemsTextList = [str(self.list_view.item(i).text()) for i in
                         range(self.list_view.count())]
        th1 = threading.Thread(target=demo.run(self,itemsTextList))
        th1.start()

    def prog_str(self, name, vid, curr_frame, vid_frame, frame_count,videos):
        result = ""
        result += "current video name: {}\n".format(name)
        result += "video: {}/{} \n".format(vid,videos)
        result += "frame: {}/{}\n".format(curr_frame,vid_frame)
        result += "total: {}/{} frames".format(frame_count,self.total_frame)

        return result

    def update_prog(self, name, vid, curr_frame, vid_frame, frame_count,videos):
        text = self.prog_str(name, vid, curr_frame, vid_frame,frame_count,videos)
        self.load_info_label.setText(text)
        progress = (frame_count/self.total_frame)*100
        print(progress)
        self.prog_bar.setValue(progress)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()


    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()

    #sys.exit(app.exec_())