#!/usr/bin/env python3
from cxwidgets.aQt.QtWidgets import QLabel, QApplication
from cxwidgets.aQt.QtCore import Qt
from cxwidgets.aQt import QtGui

from cxwidgets import CXSwitch, CXSpinBox, CXPushButton, CXEventLed, CXTextComboBox, CXLineEdit, CXProgressBar,\
    HLine, BaseGridW, CXIntComboBox, CXIntLabel, CXDevSwitch
from training_ctl_widget import TrainingCtlW

from acc_ctl.mode_defs import mode_colors
import os.path as op

script_path = op.dirname(op.realpath(__file__))


class InjExtCtl(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        grid = self.grid
        grid.addWidget(QLabel("injection/extraction control"), 0, 0, 1, 4, Qt.AlignHCenter)

        grid.addWidget(QLabel("linac run-mode"), 1, 0, 1, 1, Qt.AlignRight)
        self.linac_mode_cb = CXIntComboBox(cname='canhw:19.syn_ie4.mode', values={0: 'continuous', 1: 'counter'})
        grid.addWidget(self.linac_mode_cb, 1, 1)

        grid.addWidget(QLabel("beam switch"), 2, 0, 1, 1, Qt.AlignRight)
        grid.addWidget(CXDevSwitch(devname='beamswitch'), 2, 1)
        self.beam_swc_state = CXIntLabel(cname='beamswitch.state',
                                        values={
                                            -2: 'failed',
                                            -1: 'unknown',
                                            0:  'off',
                                            1:  'on',
                                            2: 'turning_off',
                                            3: 'turning_on',
                                           },
                                        colors={
                                            -2: '#000099',
                                            -1: '#FFFFFF',
                                            0: '#FF0000',
                                            1: '#00FF00',
                                            2: '#FFFF00',
                                            3: '#FFFF00',
                                                })
        self.beam_swc_state.setMinimumWidth(80)
        grid.addWidget(self.beam_swc_state, 2, 2)


        # turning magnet control
        grid.addWidget(QLabel("beam dump"), 3, 0, 1, 1, Qt.AlignRight)
        self.linac_dump_state = CXIntLabel(cname='canhw:21.rotmag.cur_direction',
                                           values={2: '->Dump', 1: '->Ring', 3: 'between'},
                                           colors={2: '#FF0000', 1: '#00FF00', 3: '#FFFF00'})
        grid.addWidget(self.linac_dump_state, 3, 1)

        self.dump_close_btn = CXPushButton('toDump', cname='canhw:21.rotmag.go_dump_max')
        grid.addWidget(self.dump_close_btn, 3, 2)
        self.dump_open_btn = CXPushButton('toRing', cname='canhw:21.rotmag.go_ring_max')
        grid.addWidget(self.dump_open_btn, 3, 3)

        grid.addWidget(QLabel("e-shots"), 4, 0, 1, 1, Qt.AlignRight)
        self.sb_eshots = CXSpinBox(cname='ddm.eshots')
        grid.addWidget(self.sb_eshots, 4, 1)

        grid.addWidget(QLabel("p-shots"), 4, 2, 1, 1, Qt.AlignRight)
        self.sb_eshots = CXSpinBox(cname='ddm.pshots')
        grid.addWidget(self.sb_eshots, 4, 3)

        grid.addWidget(QLabel("particles"), 5, 0, 1, 1, Qt.AlignRight)
        self.cb_particles = CXTextComboBox(cname='ddm.particles', values=['e', 'p'],
                                           icons=[script_path + '/img/electron.png', script_path + '/img/positron.png'])
        grid.addWidget(self.cb_particles, 5, 1)

        self.b_inject = CXPushButton('Inject', cname='ddm.inject')
        grid.addWidget(self.b_inject, 5, 2)

        self.b_extract = CXPushButton('Extract', cname='ddm.extract')
        grid.addWidget(self.b_extract, 5, 3)

        self.b_round = CXPushButton('Round', cname='ddm.nround')
        grid.addWidget(self.b_round, 6, 0)

        self.b_auto = CXPushButton('Auto', cname='ddm.autorun')
        grid.addWidget(self.b_auto, 6, 1)

        self.b_stop = CXPushButton('Stop', cname='ddm.stop')
        grid.addWidget(self.b_stop, 6, 2)


class InjExtState(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("Machne state"), 0, 0, 1, 4, Qt.AlignHCenter)

        self.grid.addWidget(QLabel("shots left"), 1, 0)
        self.sb_nshots = CXSpinBox(cname='ddm.shots_left')
        self.grid.addWidget(self.sb_nshots, 1, 1)

        self.grid.addWidget(QLabel("injected"), 1, 2, Qt.AlignRight)
        self.inj_led = CXEventLed(cname='ddm.injected')
        self.grid.addWidget(self.inj_led, 1, 3, Qt.AlignLeft)

        self.grid.addWidget(QLabel("extracted"), 2, 2, Qt.AlignRight)
        self.ext_led = CXEventLed(cname='ddm.extracted')
        self.grid.addWidget(self.ext_led, 2, 3, Qt.AlignLeft)

        self.grid.addWidget(QLabel("state"), 3, 0)
        self.state_line = CXLineEdit(cname='ddm.state', readonly=True, max_len=100)
        self.grid.addWidget(self.state_line, 3, 1)

        self.grid.addWidget(QLabel("runmode"), 4, 0)
        self.runmode_line = CXLineEdit(cname='ddm.icrunmode', readonly=True, max_len=100)
        self.grid.addWidget(self.runmode_line, 4, 1)


class K500State(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("K500 mode"), 0, 0, 1, 4, Qt.AlignHCenter)

        self.grid.addWidget(QLabel("mode"), 1, 0)
        vals = ['e2v2', 'p2v2', 'e2v4', 'p2v4']
        self.cb_particles = CXTextComboBox(cname='k500.modet', values=vals,
                                           colors=[mode_colors[x] for x in vals])
        self.grid.addWidget(self.cb_particles, 1, 1)

class PUSwitch(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("Particles&users switching"), 0, 0, 1, 2, Qt.AlignHCenter)

        # self.l_v34 = QLabel()
        # self.l_v34.setPixmap(QtGui.QPixmap(f"{script_path}/img/VEPP4logo_small.gif"))
        # self.grid.addWidget(self.l_v34, 1, 0, 1, 1, Qt.AlignHCenter)
        #
        # self.l_v2k = QLabel()
        # self.l_v2k.setPixmap(QtGui.QPixmap(f"{script_path}/img/v2k_logo_blue.png"))
        # self.grid.addWidget(self.l_v2k, 1, 1, 1, 1, Qt.AlignHCenter)

        self.b_e2v4 = CXPushButton('-->e2v4', cname='ddm.e2v4')
        self.grid.addWidget(self.b_e2v4, 2, 0)
        self.b_e2v4.setStyleSheet(f"background-color: {mode_colors['e2v4']};")

        self.b_p2v4 = CXPushButton('-->p2v4', cname='ddm.p2v4')
        self.grid.addWidget(self.b_p2v4, 3, 0)
        self.b_p2v4.setStyleSheet(f"background-color: {mode_colors['p2v4']};")

        self.b_e2v2 = CXPushButton('-->e2v2', cname='ddm.e2v2')
        self.grid.addWidget(self.b_e2v2, 2, 1)
        self.b_e2v2.setStyleSheet(f"background-color: {mode_colors['e2v2']};")

        self.b_p2v2 = CXPushButton('-->p2v2', cname='ddm.p2v2')
        self.grid.addWidget(self.b_p2v2, 3, 1)
        self.b_p2v2.setStyleSheet(f"background-color: {mode_colors['p2v2']};")

        self.grid.addWidget(QLabel("current state"), 4, 0, 1, 2, Qt.AlignHCenter)

        #self.grid.addWidget(QLabel("switching"), 5, 0, 1, 2, Qt.AlignHCenter)
        self.sw_progress = CXProgressBar(cname='k500.mode_progress')
        self.grid.addWidget(self.sw_progress, 5, 0, 1, 2)

        self.grid.addWidget(QLabel("allow vepp2k automatics"), 6, 0)
        self.auto_v2k_ctl = CXSwitch(cname='ddm.v2k_auto')
        self.grid.addWidget(self.auto_v2k_ctl, 6, 1)

        self.grid.addWidget(QLabel("allow vepp3/4 automatics"), 7, 0)
        self.auto_v4_ctl = CXSwitch(cname='ddm.vepp4_auto')
        self.grid.addWidget(self.auto_v4_ctl, 7, 1)


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
