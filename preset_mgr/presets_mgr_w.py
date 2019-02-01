#!/usr/bin/env python3

from aux.Qt import QtCore, QtGui, QtWidgets

from fwidgets.auxwidgets import BaseGridW
from preset_mgr import KickersPresetMgr

class PresetMgrW(BaseGridW):
    def __init__(self, parent=None):
        super(PresetMgrW, self).__init__(parent)

        self.preset_names = ['p0', 'p1', 'p2', 'p3']
        self.preset_bs = [QtWidgets.QPushButton('-->' + x) for x in self.preset_names]
        for ind in range(len(self.preset_bs)):
            self.grid.addWidget(self.preset_bs[ind], ind, 0)
            self.preset_bs[ind].clicked.connect(self.bs_proc)

        self.mgr = KickersPresetMgr()

    def bs_proc(self):
        ind = self.preset_bs.index(self.sender())
        self.mgr.copy(src='hw', dst=self.preset_names[ind])



app = QtWidgets.QApplication(['preset manager'])

w = PresetMgrW()
w.show()

app.exec_()
