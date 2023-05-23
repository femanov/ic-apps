#!/usr/bin/env python3
from cxwidgets.aQt.QtWidgets import QLabel, QApplication, QSpacerItem
from cxwidgets import CXEventLed, HLine, BaseGridW, CXIntLabel, CXStrLabel
from cxwidgets import CXScrollPlotDataItem, TimeAxisItem, AgeAxisItem, CXScrollAgePlotDataItem
import pyqtgraph as pg
import os.path as op
import pycx4.qcda as cda

script_path = op.dirname(op.realpath(__file__))

class V2kInfo(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('QLabel{font-size:20pt; color:#009900}')

        self.grid.addWidget(QLabel("VEPP2k:"), 0, 0)
        self.v2k_particles_lab = CXIntLabel(cname='cxout:1.v2k.regime',
                                            pics={1: f'{script_path}/img/electron.png',
                                                  2: f'{script_path}/img/electron.png',
                                                  3: f'{script_path}/img/positron.png',
                                                  4: f'{script_path}/img/positron.png',
                                                  }
                                            )
        self.grid.addWidget(self.v2k_particles_lab, 0, 1)

        self.v2k_auto_l = CXStrLabel(cname='cxout:1.bep.injection.state',
                                     pics={'ON': f'{script_path}/img/auto_on.png',
                                           'SUSPENDED': f'{script_path}/img/auto_suspended.png',
                                           'UNKNOWN': f'{script_path}/img/auto_unknown.png',
                                           }
                                     )
        self.grid.addWidget(self.v2k_auto_l, 0, 2)

        self.bep_state_l = CXStrLabel(cname='cxout:1.bep.state',
                                     pics={'1': f'{script_path}/img/store.png',
                                           '1->2': f'{script_path}/img/ramp.png',
                                           '2': f'{script_path}/img/transfer.png',
                                           '3': f'{script_path}/img/store.png',
                                           '3->4': f'{script_path}/img/ramp.png',
                                           '4': f'{script_path}/img/transfer.png',
                                           'Remagn-3': f'{script_path}/img/cycle.png',
                                           'Remagn-1': f'{script_path}/img/cycle.png',
                                           '2->1': f'{script_path}/img/cycle.png',
                                           '4->3': f'{script_path}/img/cycle.png',
                                           '3->1': f'{script_path}/img/cycle.png',
                                           '1->3': f'{script_path}/img/cycle.png',
                                           }
                                     )
        self.grid.addWidget(self.bep_state_l, 0, 3)

        self.bep_inflector_l = CXIntLabel(cname='cxout:1.bep.inflector',
                                          pics={0: f'{script_path}/img/inflector_off.png',
                                                1: f'{script_path}/img/inflector_on.png',
                                                }
                                         )
        self.grid.addWidget(self.bep_inflector_l, 0, 4)

        self.bep_rfbypass_l = CXIntLabel(cname='cxout:1.bep.probros',
                                         pics={0: f'{script_path}/img/empty.png',
                                               1: f'{script_path}/img/rfbypass_on.png',
                                              }
                                        )
        self.grid.addWidget(self.bep_rfbypass_l, 0, 5)

        self.grid.addItem(QSpacerItem(10, 10), 0, 6)
        self.grid.setColumnStretch(6, 1)

class V34Info(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('QLabel{font-size:20pt; color:#009900;}')

        self.grid.addWidget(QLabel("VEPP3:"), 0, 0)

        self.particles_lab = CXStrLabel(cname='cxout:2.vepp3.tPolarity',
                                            pics={'e-': f'{script_path}/img/electron.png',
                                                  'e+': f'{script_path}/img/positron.png',
                                                  }
                                            )
        self.grid.addWidget(self.particles_lab, 0, 1)

        self.vepp3_status_l = CXStrLabel(cname='cxout:2.vepp3.tstatus',
                                     pics={'Injection': f'{script_path}/img/store.png',
                                           'Acceleration': f'{script_path}/img/ramp.png',
                                           'Extraction': f'{script_path}/img/transfer.png',
                                           'Cycle': f'{script_path}/img/cycle.png',
                                           'Experiment': f'{script_path}/img/experiment.png',
                                           }
                                     )
        self.grid.addWidget(self.vepp3_status_l, 0, 3)

        self.grid.addItem(QSpacerItem(10, 10), 0, 5)
        self.grid.setColumnStretch(5, 1)


        self.grid.addWidget(QLabel("VEPP4:"), 0, 6)
        self.vepp4_status_l = CXStrLabel(cname='cxout:2.vepp4.tstatus',
                                     pics={'Injection': f'{script_path}/img/store.png',
                                           'Acceleration': f'{script_path}/img/ramp.png',
                                           'Extraction': f'{script_path}/img/transfer.png',
                                           'Cycle': f'{script_path}/img/cycle.png',
                                           'Experiment': f'{script_path}/img/experiment.png',
                                           }
                                     )
        self.grid.addWidget(self.vepp4_status_l, 0, 7)

        #self.grid.addItem(QSpacerItem(10, 10), 0, 6)
        #self.grid.setColumnStretch(6, 1)

class FireBoardWidget(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background: #404040;'
                           '')

        self.grid.addWidget(V2kInfo(), 0, 0)
        self.grid.addWidget(V34Info(), 0, 1)

        self.graph_bep = pg.GraphicsLayoutWidget(parent=self)
        self.grid.addWidget(self.graph_bep, 1, 0)

        self.graph_v2k = pg.GraphicsLayoutWidget(parent=self)
        self.grid.addWidget(self.graph_v2k, 2, 0)

        self.graph_vepp3 = pg.GraphicsLayoutWidget(parent=self)
        self.grid.addWidget(self.graph_vepp3, 1, 1)

        self.graph_vepp4 = pg.GraphicsLayoutWidget(parent=self)
        self.grid.addWidget(self.graph_vepp4, 2, 1)

        self.line_w = 5

        self.plt_bep = self.graph_bep.addPlot(labels={'left': ('BEP current', 'mA'), 'bottom': ('Age', 's')})
        self.plt_bep.setXRange(0, 900, padding=0.02)
        self.plt_bep.invertX(True)
        self.pen_e = pg.mkPen(0, 255, 0, width=self.line_w)
        self.pen_p = pg.mkPen(255, 0, 0, width=self.line_w)
        self.curv_bep = None

        plt_v2k = self.graph_v2k.addPlot(labels={'left': ('V2k current', 'mA'), 'bottom': ('Age', 's')})
        plt_v2k.setXRange(0, 900, padding=0.02)
        plt_v2k.invertX(True)

        curv_v2k_p = CXScrollAgePlotDataItem(cname='cxout:1.v2k.current.p', pen=self.pen_p, length=900, utime=1000)
        plt_v2k.addItem(curv_v2k_p)

        curv_v2k_e = CXScrollAgePlotDataItem(cname='cxout:1.v2k.current.e', pen=self.pen_e, length=900, utime=1000)
        plt_v2k.addItem(curv_v2k_e)

        self.regime_c = cda.IChan('cxout:1.v2k.regime')
        self.regime_c.valueChanged.connect(self.regime_proc)
        self.v2k_particles = None

        #------ VEPP-3/4 plots
        plt_vepp3 = self.graph_vepp3.addPlot(labels={'left': ('VEPP3 current', 'mA'), 'bottom': ('Age', 's')})
        plt_vepp3.setXRange(0, 900, padding=0.02)
        plt_vepp3.invertX(True)

        curv_v3_cur = CXScrollAgePlotDataItem(cname='cxout:2.vepp3.currentTotal', pen=self.pen_e, length=900, utime=1000)
        plt_vepp3.addItem(curv_v3_cur)


        plt_vepp4 = self.graph_vepp4.addPlot(labels={'left': ('VEPP4 current', 'mA'), 'bottom': ('Age', 's')})
        plt_vepp4.setXRange(0, 900, padding=0.02)
        plt_vepp4.invertX(True)

        curv_v4_cur_e1 = CXScrollAgePlotDataItem(cname='cxout:2.vepp4.currentE1', pen=self.pen_e, length=900, utime=1000)
        plt_vepp4.addItem(curv_v4_cur_e1)
        curv_v4_cur_e2 = CXScrollAgePlotDataItem(cname='cxout:2.vepp4.currentE2', pen=self.pen_e, length=900, utime=1000)
        plt_vepp4.addItem(curv_v4_cur_e2)
        curv_v4_cur_p1 = CXScrollAgePlotDataItem(cname='cxout:2.vepp4.currentP1', pen=self.pen_p, length=900, utime=1000)
        plt_vepp4.addItem(curv_v4_cur_p1)
        curv_v4_cur_p2 = CXScrollAgePlotDataItem(cname='cxout:2.vepp4.currentP2', pen=self.pen_p, length=900, utime=1000)
        plt_vepp4.addItem(curv_v4_cur_p2)



    def regime_proc(self, chan):
        if chan.val in (1, 2):
            if self.v2k_particles == 'e-':
                return
            else:
                self.v2k_particles = 'e-'
        elif chan.val in (3, 4):
            if self.v2k_particles == 'e+':
                return
            else:
                self.v2k_particles = 'e+'
        if self.curv_bep is not None:
            self.plt_bep.removeItem(self.curv_bep)
        if self.v2k_particles == 'e+':
            self.curv_bep = CXScrollAgePlotDataItem(cname='cxout:1.bep.current.p', pen=self.pen_p,
                                                    symbolBrush=(255, 0, 0), symbolPen='w',
                                                    length=900, utime=1000)
        elif self.v2k_particles == 'e-':
            self.curv_bep = CXScrollAgePlotDataItem(cname='cxout:1.bep.current.e', pen=self.pen_e,
                                                    symbolBrush=(0, 255, 0), symbolPen='w',
                                                    length=900, utime=1000)
        self.plt_bep.addItem(self.curv_bep)



app = QApplication(['Fire dash-board'])

w = FireBoardWidget()
w.resize(1600, 600)
w.show()

app.exec_()


