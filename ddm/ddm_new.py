#!/usr/bin/env python3

from cxwidgets.aQt.QtWidgets import QLabel, QApplication
from cxwidgets.aQt.QtCore import Qt
from cxwidgets.aQt import QtGui

from cxwidgets import CXSwitch, CXSpinBox, CXPushButton, CXEventLed, CXTextComboBox, CXLineEdit, CXProgressBar, HLine, BaseGridW
from training_ctl_widget import TrainingCtlW

from acc_ctl.mode_defs import mode_colors
import os.path as op

script_path = op.dirname(op.realpath(__file__))


class InjExtCtl(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        grid = self.grid
        grid.addWidget(QLabel("injection/extraction control"), 0, 0, 1, 4, Qt.AlignHCenter)

        grid.addWidget(QLabel("e-shots"), 1, 0)
        self.sb_eshots = CXSpinBox(cname='cxhw:0.ddm.eshots')
        grid.addWidget(self.sb_eshots, 1, 1)

        grid.addWidget(QLabel("p-shots"), 1, 2)
        self.sb_eshots = CXSpinBox(cname='cxhw:0.ddm.pshots')
        grid.addWidget(self.sb_eshots, 1, 3)

        grid.addWidget(QLabel("particles"), 2, 0)
        self.cb_particles = CXTextComboBox(cname='cxhw:0.ddm.particles', values=['e', 'p'],
                                           icons=[script_path + '/img/electron.png', script_path + '/img/positron.png'])
        grid.addWidget(self.cb_particles, 2, 1)

        self.b_inject = CXPushButton('Inject', cname='cxhw:0.ddm.inject')
        grid.addWidget(self.b_inject, 2, 2)

        self.b_extract = CXPushButton('Extract', cname='cxhw:0.ddm.extract')
        grid.addWidget(self.b_extract, 2, 3)

        self.b_round = CXPushButton('Round', cname='cxhw:0.ddm.nround')
        grid.addWidget(self.b_round, 3, 0)

        self.b_auto = CXPushButton('Auto', cname='cxhw:0.ddm.autorun')
        grid.addWidget(self.b_auto, 3, 1)

        self.b_stop = CXPushButton('Stop', cname='cxhw:0.ddm.stop')
        grid.addWidget(self.b_stop, 3, 2)


class InjExtState(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("Machne state"), 0, 0, 1, 4, Qt.AlignHCenter)

        self.grid.addWidget(QLabel("shots left"), 1, 0)
        self.sb_nshots = CXSpinBox(cname='canhw:19.syn_ie4.ie_bum')
        self.grid.addWidget(self.sb_nshots, 1, 1)

        self.grid.addWidget(QLabel("injected"), 1, 2, Qt.AlignRight)
        self.inj_led = CXEventLed(cname='cxhw:0.ddm.injected')
        self.grid.addWidget(self.inj_led, 1, 3, Qt.AlignLeft)

        self.grid.addWidget(QLabel("extracted"), 2, 2, Qt.AlignRight)
        self.ext_led = CXEventLed(cname='cxhw:0.ddm.extracted')
        self.grid.addWidget(self.ext_led, 2, 3, Qt.AlignLeft)

        self.grid.addWidget(QLabel("state"), 3, 0)
        self.state_line = CXLineEdit(cname='cxhw:0.ddm.state', readonly=True, max_len=100)
        self.grid.addWidget(self.state_line, 3, 1)

        self.grid.addWidget(QLabel("runmode"), 4, 0)
        self.runmode_line = CXLineEdit(cname='cxhw:0.ddm.icrunmode', readonly=True, max_len=100)
        self.grid.addWidget(self.runmode_line, 4, 1)


class K500State(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("K500 mode"), 0, 0, 1, 4, Qt.AlignHCenter)

        self.grid.addWidget(QLabel("mode"), 1, 0)
        vals = ['e2v2', 'p2v2', 'e2v4', 'p2v4']
        self.cb_particles = CXTextComboBox(cname='cxhw:0.k500.modet', values=vals,
                                           colors=[mode_colors[x] for x in vals])
        self.grid.addWidget(self.cb_particles, 1, 1)

class PUSwitch(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("Particles&users switching"), 0, 0, 1, 2, Qt.AlignHCenter)

        self.l_v34 = QLabel()
        self.l_v34.setPixmap(QtGui.QPixmap(script_path + "/img/VEPP4logo_small.gif"))
        self.grid.addWidget(self.l_v34, 1, 0, 1, 1, Qt.AlignHCenter)

        self.l_v2k = QLabel()
        self.l_v2k.setPixmap(QtGui.QPixmap(script_path + "/img/v2k_logo_blue.png"))
        self.grid.addWidget(self.l_v2k, 1, 1, 1, 1, Qt.AlignHCenter)

        self.b_e2v4 = CXPushButton('-->e2v4', cname='cxhw:0.ddm.e2v4')
        self.grid.addWidget(self.b_e2v4, 2, 0)
        self.b_e2v4.setStyleSheet('background-color:' + mode_colors['e2v4'] + ';')

        self.b_p2v4 = CXPushButton('-->p2v4', cname='cxhw:0.ddm.p2v4')
        self.grid.addWidget(self.b_p2v4, 3, 0)
        self.b_p2v4.setStyleSheet('background-color:' + mode_colors['p2v4'] + ';')

        self.b_e2v2 = CXPushButton('-->e2v2', cname='cxhw:0.ddm.e2v2')
        self.grid.addWidget(self.b_e2v2, 2, 1)
        self.b_e2v2.setStyleSheet('background-color:' + mode_colors['e2v2'] + ';')

        self.b_p2v2 = CXPushButton('-->p2v2', cname='cxhw:0.ddm.p2v2')
        self.grid.addWidget(self.b_p2v2, 3, 1)
        self.b_p2v2.setStyleSheet('background-color:' + mode_colors['p2v2'] + ';')

        self.grid.addWidget(QLabel("current state"), 4, 0, 1, 2, Qt.AlignHCenter)

        #self.grid.addWidget(QLabel("switching"), 5, 0, 1, 2, Qt.AlignHCenter)
        self.sw_progress = CXProgressBar(cname='cxhw:0.k500.mode_progress')
        self.grid.addWidget(self.sw_progress, 5, 0, 1, 2)

        self.grid.addWidget(QLabel("allow vepp2k automatics"), 6, 0)
        self.auto_v2k_ctl = CXSwitch(cname='cxhw:0.ddm.v2k_auto')
        self.grid.addWidget(self.auto_v2k_ctl, 6, 1)


class DDMWidget(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.extr_trainer = TrainingCtlW()
        self.grid.addWidget(self.extr_trainer, 0, 0)

        self.grid.addWidget(HLine(), 1, 0)
        self.inj_ext = InjExtCtl()
        self.grid.addWidget(self.inj_ext, 2, 0)

        self.grid.addWidget(HLine(), 3, 0)
        self.inj_ext_st = InjExtState()
        self.grid.addWidget(self.inj_ext_st, 4, 0)

        self.grid.addWidget(HLine(), 5, 0)

        self.k500_st = K500State()
        self.grid.addWidget(self.k500_st, 6, 0)

        self.grid.addWidget(HLine(), 7, 0)

        self.pu_sw = PUSwitch()
        self.grid.addWidget(self.pu_sw, 8, 0)

        #self.grid.addWidget(QLabel("Automatic Injection/extraction control"), 2, 0, 1, 4, Qt.AlignHCenter)


app = QApplication(['Doom\'s day machine'])

w = DDMWidget()
w.show()

app.exec_()
