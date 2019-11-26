
from aux.Qt import QtCore, QtWidgets
from cxwidgets import CXSpinBox, CXCheckBox


class TrainingCtlW(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super(TrainingCtlW, self).__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        self.grid.addWidget(QtWidgets.QLabel("Training shots control"), 0, 0, 1, 4, QtCore.Qt.AlignHCenter)

        self.grid.addWidget(QtWidgets.QLabel("Interval,s"), 1, 0)

        self.sb_interval = CXSpinBox(cname='cxhw:0.ddm.extr_train_interval')
        self.grid.addWidget(self.sb_interval, 1, 1)

        self.grid.addWidget(QtWidgets.QLabel("run"), 1, 2)

        self.cb_run = CXCheckBox(cname='cxhw:0.ddm.extr_train')
        self.grid.addWidget(self.cb_run, 1, 3)

