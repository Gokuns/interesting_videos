import matplotlib
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

matplotlib.use('Qt5Agg')

from sklearn.manifold import TSNE

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import json
import config


class Ui_tsne_view(object):

    def pca_data(self, data):
        feature_vector_list = [video["features"] for video in data]
        features = StandardScaler().fit_transform(feature_vector_list)
        pca = PCA(n_components=50)
        principal_components = pca.fit_transform(features).tolist()
        for i in range(len(data)):
            data[i]["features"] = principal_components[i]
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        return data

    def load_data(self, path=config.argument_defaults['aggragation']):
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
            labels = [fil[i]['poc_result'] for i in range(len(fil))]
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
        # video_player_module.play_vid("scene-0003.mp4")

    def plot_tnse(self, x_vals, y_vals, z_vals, names, labels, mode):
        self.plotWidget.canvas.axes.clear()
        self.plotWidget.canvas.axes.patch.set_visible(False)

        if mode:
            for i in range(len(labels)):
                if labels[i] == 0:
                    labels[i] = 'black'
                else:
                    labels[i] = 'red'
            self.plotWidget.canvas.axes.scatter(x_vals, y_vals, z_vals, 'o', picker=5, c=labels)
        else:
            self.plotWidget.canvas.axes.scatter(x_vals, y_vals, z_vals, 'o', picker=5)
            # ax.annotate(names[i], (x_vals[i], y_vals[i]))
        cid = self.plotWidget.canvas.axes.figure.canvas.mpl_connect('pick_event',
                                                                    lambda event: self.onpick(event, names))
        self.plotWidget.canvas.draw()

    def refresh_plot(self):
        file = self.load_data()
        data = self.pca_data(file)  # uncomment this when needed
        # file = load_data('C:\\Users\\Goko\\Desktop\\data.json')
        features, names, labels = self.partition_data(data, config.argument_defaults["colored_graph"])
        x_vals, y_vals, z_vals = self.tsne(features, names, labels)
        self.plot_tnse(x_vals, y_vals, z_vals, names, labels, config.argument_defaults["colored_graph"])

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 720)
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
                                 "    font-size: 12px;\n"
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
                                 "QProgressBar::chunked\n"
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
                                 "\n"
                                 "")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plotWidget = MplWidget(self.centralwidget)
        self.plotWidget.setMinimumSize(QtCore.QSize(461, 401))
        self.plotWidget.setObjectName("plotWidget")
        self.horizontalLayout.addWidget(self.plotWidget)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.iterationsLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iterationsLabel.sizePolicy().hasHeightForWidth())
        self.iterationsLabel.setSizePolicy(sizePolicy)
        self.iterationsLabel.setObjectName("iterationsLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.iterationsLabel)
        self.iterationsSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iterationsSpinBox.sizePolicy().hasHeightForWidth())
        self.iterationsSpinBox.setSizePolicy(sizePolicy)
        self.iterationsSpinBox.setMinimum(250)
        self.iterationsSpinBox.setMaximum(10000)
        self.iterationsSpinBox.setSingleStep(5)
        self.iterationsSpinBox.setProperty("value", 1000)
        self.iterationsSpinBox.setDisplayIntegerBase(10)
        self.iterationsSpinBox.setObjectName("iterationsSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.iterationsSpinBox)
        self.perplexityLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.perplexityLabel.sizePolicy().hasHeightForWidth())
        self.perplexityLabel.setSizePolicy(sizePolicy)
        self.perplexityLabel.setObjectName("perplexityLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.perplexityLabel)
        self.perplexitySpinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.perplexitySpinBox.sizePolicy().hasHeightForWidth())
        self.perplexitySpinBox.setSizePolicy(sizePolicy)
        self.perplexitySpinBox.setMinimum(5)
        self.perplexitySpinBox.setMaximum(50)
        self.perplexitySpinBox.setProperty("value", 30)
        self.perplexitySpinBox.setObjectName("perplexitySpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.perplexitySpinBox)
        self.learningRateSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.learningRateSpinBox.sizePolicy().hasHeightForWidth())
        self.learningRateSpinBox.setSizePolicy(sizePolicy)
        self.learningRateSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.learningRateSpinBox.setMinimum(10)
        self.learningRateSpinBox.setMaximum(1000)
        self.learningRateSpinBox.setProperty("value", 200)
        self.learningRateSpinBox.setDisplayIntegerBase(10)
        self.learningRateSpinBox.setObjectName("learningRateSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.learningRateSpinBox)
        self.earlyExaggerationLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.earlyExaggerationLabel.sizePolicy().hasHeightForWidth())
        self.earlyExaggerationLabel.setSizePolicy(sizePolicy)
        self.earlyExaggerationLabel.setObjectName("earlyExaggerationLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.earlyExaggerationLabel)
        self.earlyExaggerationSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.earlyExaggerationSpinBox.sizePolicy().hasHeightForWidth())
        self.earlyExaggerationSpinBox.setSizePolicy(sizePolicy)
        self.earlyExaggerationSpinBox.setProperty("value", 12)
        self.earlyExaggerationSpinBox.setObjectName("earlyExaggerationSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.earlyExaggerationSpinBox)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        self.learningRateLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.learningRateLabel.sizePolicy().hasHeightForWidth())
        self.learningRateLabel.setSizePolicy(sizePolicy)
        self.learningRateLabel.setObjectName("learningRateLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.learningRateLabel)
        self.horizontalLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.pushButton.clicked.connect(self.refresh_plot)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.iterationsLabel.setText(_translate("MainWindow", "Iterations"))
        self.perplexityLabel.setText(_translate("MainWindow", "Perplexity"))
        self.earlyExaggerationLabel.setText(_translate("MainWindow", "Early Exaggeration"))
        self.pushButton.setText(_translate("MainWindow", "Refresh"))
        self.learningRateLabel.setText(_translate("MainWindow", "Learning Rate"))
        MainWindow.addToolBar(NavigationToolbar(self.plotWidget.canvas, MainWindow))


from visualizer.mplwidget import MplWidget

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_tsne_view()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
