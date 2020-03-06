#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
from cxwidgets import BaseGridW, HLine
import pycx4.qcda as cda
from cxwidgets import CXSwitch, CXSpinBox, CXPushButton, CXIntComboBox, CXCheckBox


srv = 'cxhw:15'
cmap = {
    'adc250_8e': {'line0': 's1_in', 'line1': 's1_out', 'line2': 's2_in', 'line3': 's2_out'},
    'adc250_90': {'line0': 's3_in', 'line1': 's3_out', 'line2': 's4_in', 'line3': 's4_out'},
    'adc250_92': {'line0': 's5_in', 'line1': 's5_out', 'line2': 's6_in', 'line3': 's6_out'},
    'adc250_94': {'line0': 's7_in', 'line1': 's7_out', 'line2': 's8_in', 'line3': 's8_out'},
    'adc250_96': {'line0': 's9_in', 'line1': 's9_out', 'line2': 's10_in', 'line3': 's10_out'},
    'adc250_98': {'line0': 's11_in_ref', 'line1': 's11_out', 'line2': 's12_in_ref', 'line3': 's12_out'},
    'adc250_9a': {'line0': 's13_in_ref', 'line1': 's13_out_ref', 'line2': 's14_in_ref', 'line3': 's14_out_ref'},
    'adc250_9c': {'line0': 'grp_in', 'line1': '', 'line2': 'gun_hv', 'line3': 'beam'},
}

c_sign = {'s4_in', 's6_in', 's8_in', 's10_out'}


class ADC4x250_settings(BaseGridW):
    def __init__(self, scope_dev):
        super().__init__()

        self.grid.addWidget(QLabel('scope: ' + scope_dev))

        grid1 = QGridLayout()
        self.grid.addLayout(grid1, 1, 0)
        grid1.addWidget(QLabel('numpts'), 0, 0)
        grid1.addWidget(CXSpinBox(cname=scope_dev + '.numpts'), 0, 1)
        grid1.addWidget(QLabel('@'), 0, 2)
        grid1.addWidget(CXSpinBox(cname=scope_dev + '.ptsofs'), 0, 3)

        grid2 = QGridLayout()
        self.grid.addLayout(grid2, 2, 0)
        grid2.addWidget(QLabel('clock'), 0, 0)
        grid2.addWidget(CXIntComboBox(cname=scope_dev + '.timing',
                                      values={0: 'Int 50 MHz',
                                              1: 'FrontPanel',
                                              2: 'Backplane'}),
                        0, 1)
        grid2.addWidget(QLabel('trigger'), 0, 2)
        grid2.addWidget(CXIntComboBox(cname=scope_dev + '.trig_type',
                                      values={0: 'Disable',
                                              1: 'Internal',
                                              2: 'Front',
                                              3: 'Backplane',
                                              4: 'Back+sync'}),
                        0, 3)
        grid2.addWidget(CXIntComboBox(cname=scope_dev + '.trig_input',
                                      values={0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7'}),
                        0, 4)

        grid3 = QGridLayout()
        self.grid.addLayout(grid3, 3, 0)
        grid3.addWidget(CXPushButton('Calibrate', cname=scope_dev + '.calibrate'), 0, 0)
        grid3.addWidget(CXPushButton('Calibr.rst', cname=scope_dev + '.fgt_clb'), 0, 1)
        grid3.addWidget(CXPushButton('shot', cname=scope_dev + '.shot'), 0, 2)
        grid3.addWidget(CXPushButton('stop', cname=scope_dev + '.shot'), 0, 3)

        grid4 = QGridLayout()
        self.grid.addLayout(grid4, 4, 0)
        for x in range(4):
            grid4.addWidget(CXIntComboBox(cname=scope_dev + '.range' + str(x),
                                          values={0: '0.5 V', 1: '1 V', 2: '2 V', 3: '4 V'}
                                          ), 0, x)


class ScopeSettings(BaseGridW):
    def __init__(self):
        super().__init__()

        c_count, r_count = 0, 0
        for k in cmap:
            self.grid.addWidget(ADC4x250_settings(srv + '.' + k), r_count, c_count)
            c_count += 1
            if c_count == 2:
                self.grid.addWidget(HLine(), r_count + 1, 0, 1, 2)
                c_count = 0
                r_count += 2


class ScopesTools(BaseGridW):
    def __init__(self):
        super().__init__()

        self.btn_resize = QPushButton('fit size')
        self.grid.addWidget(self.btn_resize, 0, 0)

        self.btn_settings = QPushButton('settings')
        self.grid.addWidget(self.btn_settings, 0, 1)
        self.btn_settings.clicked.connect(self.show_settings)

        self.grid.addItem(QSpacerItem(1500, 50, hPolicy=QSizePolicy.Maximum), 0, 2)

    def show_settings(self):
        self.sw = ScopeSettings()
        self.sw.show()


class Scope(BaseGridW):
    def __init__(self):
        super().__init__()

        self.tool_bar = ScopesTools()
        self.grid.addWidget(self.tool_bar, 0, 0)
        self.tool_bar.btn_resize.clicked.connect(self.rerange)

        self.pens = [(255, 0, 0), (0, 255, 0), (255, 0, 255), (255, 255, 0)]
        graph = pg.GraphicsLayoutWidget(parent=self)
        plts = {}
        chans = {}
        curvs = {}
        c_count = 0
        for dk in cmap:
            plts[dk] = graph.addPlot(title=dk, autoDownsample=True)
            plts[dk].disableAutoRange()
            g_count = 0
            for ck in cmap[dk]:
                n = '.'.join([srv, dk, ck])
                csign = True if cmap[dk][ck] in c_sign else False
                c = cda.VChan(n, dtype=cda.CXDTYPE_SINGLE, max_nelems=783155, change_sign=csign)
                c.valueMeasured.connect(self.update_plot)
                curvs[n] = plts[dk].plot(c.val, pen=self.pens[g_count])
                chans[n] = c
                g_count += 1

            c_count += 1
            if c_count == 2:
                graph.nextRow()
                c_count = 0

        self.graph, self.plts, self.curvs, self.chans = graph, plts, curvs, chans
        # put in grid
        self.grid.addWidget(graph, 1, 0)

    def update_plot(self, chan):
        self.curvs[chan.name].setData(chan.val)

    def rerange(self):
        print('updating ranges')
        for dk in cmap:
            g_ymax, g_ymin = None, None
            for ck in cmap[dk]:
                n = '.'.join([srv, dk, ck])
                ymax = np.max(self.chans[n].val)
                if g_ymax is None:
                    g_ymax = ymax
                else:
                    if ymax > g_ymax:
                        g_ymax = ymax
                ymin = np.min(self.chans[n].val)
                if g_ymin is None:
                    g_ymin = ymin
                else:
                    if ymin < g_ymin:
                        g_ymin = ymin
            self.plts[dk].setYRange(g_ymin, g_ymax, padding=0.05)
            self.plts[dk].setXRange(0, self.chans[n].nelems)

    # def add_curve(self, name):
    #     pass


if __name__ == '__main__':
    from sys import argv, exit
    app = QApplication(argv)
    win = Scope()
    win.resize(1980, 1200)
    win.show()
    exit(app.exec_())
