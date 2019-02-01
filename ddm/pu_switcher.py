from aQt.QtCore import QObject, pyqtSignal, QTimer
from acc_ctl.mode_defs import *
import numpy as np
import time
import pycx4.qcda as cda

from acc_ctl.mode_ser import ModesClient
from acc_ctl.k500modes import K500Director


mode_subsys = {
    'linac': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
              19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
              32, 33, 34, 35, 36, 37, 38, 39],
    'ring': [40, 41, 42, 43, 44, 45, 46, 47],
    'syn.transfer': [49],
    'K500.e-ext': [50, 51, 52, 53],
    'K500.p-ext': [54, 55, 56, 57],
    'K500.com': [58, 59, 60, 61, 62, 63],
    'K500.cVEPP3': [64, 65, 66, 67],
    'K500.cBEP': [68, 69, 70, 71],
}

remag_subsys = [59, 60]

bline_parts = {
    'e2v2': ['linac', 'ring', 'syn.transfer', 'K500.e-ext', 'K500.com', 'K500.cBEP'],
    'p2v2': ['linac', 'ring', 'syn.transfer', 'K500.p-ext', 'K500.com', 'K500.cBEP'],
    'e2v4': ['linac', 'ring', 'syn.transfer', 'K500.e-ext', 'K500.com', 'K500.cVEPP3'],
    'p2v4': ['linac', 'ring', 'syn.transfer', 'K500.p-ext', 'K500.com', 'K500.cVEPP3'],
}


class PUSwitcher(QObject):
    switching_done = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(PUSwitcher, self).__init__(*args)

        self.mode_ctl = kwargs.get('mode_ctl', ModesClient())
        self.k500ctl = kwargs.get('k500ctl', K500Director())

        self.c_k500mode = cda.StrChan('cxhw:0.k500.modet')
        self.c_mode_progress = cda.IChan('cxhw:0.k500.mode_progress')
        self.c_k500_mag_state = cda.StrChan('cxhw:0.k500.mag_state')

        self.k500ctl.progressing.connect(self.c_mode_progress.setValue)
        #self.k500ctl.modeCurUpdate.connect(self.update_cur_mode)
        self.k500ctl.done.connect(self.switched)

        self.req_mode = None
        self.all_mode = None

        self.modes = {
            'linac': None,
            'ring': None,
            'syn.transfer': None,
            'K500.e-ext': None,
            'K500.p-ext': None,
            'K500.com': None,
            'K500.cBEP': None,
            'K500.cVEPP3': None,
        }

        self.wait_remag = False
        self.timer = QTimer()

    def switched(self):
        self.set_mode(self.req_mode)
        self.req_mode = None
        self.switching_done.emit()

    def what2switch(self, mode):
        bline = bline_parts[mode]
        return [bline[ind] for ind in range(len(bline)) if mode != self.modes[bline[ind]]]

    def set_mode(self, mode):
        self.all_mode = mode
        self.c_k500mode.setValue(mode)
        sw = self.what2switch(mode)
        for x in sw:
            self.modes[x] = mode

    def switch_mode(self, mode):
        print('switching mode to: ', mode)
        self.req_mode = mode
        sw = self.what2switch(mode)
        sys2sw = []
        for k in sw:
            sys2sw += mode_subsys[k]
        need_remag = False
        for x in remag_subsys:
            if x in sys2sw:
                need_remag = True
                sys2sw.remove(x)
        if need_remag:
            self.k500ctl.set_mode(mode_map[mode])
            pass

        print('mode request: ', mode_map[mode], sys2sw)
        self.mode_ctl.load_marked(mode_map[mode], sys2sw)
        if not need_remag:
            self.timer.singleShot(500, self.switched)




