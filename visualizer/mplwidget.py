# Imports
from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure
import matplotlib
# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

# Matplotlib canvas class to create figure
# class MplCanvas(Canvas):
#     def __init__(self):
#         self.fig = Figure()
#         self.ax = self.fig.add_subplot(111, projection='3d')
#         Canvas.__init__(self, self.fig)
#         Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
#         Canvas.updateGeometry(self)

# Matplotlib widget
class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111, projection = '3d')
        self.canvas.figure.patch.set_visible(False)
        self.canvas.axes.patch.set_visible(False)

        self.setLayout(vertical_layout)
