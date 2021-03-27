#!/usr/bin/env python3

from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
from cxwidgets import BaseGridW, HLine, VLine
import pycx4.qcda as cda
from cxwidgets import CXSwitch, CXSpinBox, CXPushButton, CXIntComboBox, CXCheckBox
import json
import time

from scopes_map import srv, cmap, c_sign

f = open('rf_power_calibr.json')
rf_pwr_clb = json.load(f)
f.close()


class ScopesChansContainer:
    def __init__(self):
        self.signals = {}
        self.chans = {}
        self.chans_map = {}

        for dk in cmap:
            lines = {}
            for ck in cmap[dk]:
                n = '.'.join([srv, dk, ck])
                csign = True if cmap[dk][ck] in c_sign else False
                c = cda.VPChan(n, dtype=cda.DTYPE_SINGLE, max_nelems=783155, change_sign=csign)
                lines[ck] = c
                self.signals[cmap[dk][ck]] = c
                self.chans[n] = c
            self.chans_map[dk] = lines


class ADC4x250_settings(BaseGridW):
    def __init__(self, scope_dev, lines):
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
            grid4.addWidget(QLabel(lines['line' + str(x)]), 1, x)


class ScopeSettings(BaseGridW):
    def __init__(self):
        super().__init__()

        c_count, r_count = 0, 0
        for k in cmap:
            self.grid.addWidget(ADC4x250_settings(srv + '.' + k, cmap[k]), r_count, c_count)
            c_count += 1
            if c_count == 2:
                self.grid.addWidget(HLine(), r_count + 1, 0, 1, 2)
                c_count = 0
                r_count += 2


class ScopesDataTools(BaseGridW):
    def __init__(self):
        super().__init__()
        self.btn_get_json = QPushButton('get as json')
        self.grid.addWidget(self.btn_get_json, 0, 0)
        self.btn_get_json.clicked.connect(self.save_data_json)

        self.btn_get_bg = QPushButton('get background')
        self.grid.addWidget(self.btn_get_bg, 1, 0)
        self.btn_get_bg.clicked.connect(self.get_background)

        self.btn_show_sig = QPushButton('show signals')
        self.grid.addWidget(self.btn_show_sig, 2, 0)
        self.btn_show_sig.clicked.connect(self.show_signals)

        self.grid.addWidget(QLabel('Signals input'), 0, 1)

        lc = 1
        self.sig_checkbs = {}
        for ks in scope_chans.signals:
            scb = QCheckBox(ks)
            self.grid.addWidget(scb, lc, 1)
            self.sig_checkbs[ks] = scb
            lc += 1

        self.sws = {}

    def save_data_json(self):
        data = {k: scope_chans.signals[k].val.tolist() for k in self.sig_checkbs if self.sig_checkbs[k].isChecked()}
        f = open("rf_sc_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".json", 'w')
        json.dump(data, f)
        f.close()

    def get_background(self):
        for k in self.sig_checkbs:
            if self.sig_checkbs[k].isChecked():
                scope_chans.signals[k].getBg(100)

    def show_signals(self):
        for k in self.sig_checkbs:
            if self.sig_checkbs[k].isChecked():
                self.sws[k] = SignalW(scope_chans.signals[k], k)
                self.sws[k].show()



class ScopesTools(BaseGridW):
    def __init__(self):
        super().__init__()

        self.btn_resize = QPushButton('fit size')
        self.grid.addWidget(self.btn_resize, 0, 0)

        self.btn_settings = QPushButton('settings')
        self.grid.addWidget(self.btn_settings, 0, 1)
        self.btn_settings.clicked.connect(self.show_settings)

        self.btn_data = QPushButton('data')
        self.grid.addWidget(self.btn_data, 0, 2)
        self.btn_data.clicked.connect(self.show_data_tools)

        self.legends_cb = QCheckBox('showLegends')
        self.legends_cb.setChecked(True)
        self.grid.addWidget(self.legends_cb, 0, 3)

        self.grid.addItem(QSpacerItem(1500, 20, hPolicy=QSizePolicy.Maximum), 0, 4)

    def show_settings(self):
        self.sw = ScopeSettings()
        self.sw.show()

    def show_data_tools(self):
        self.data_tk = ScopesDataTools()
        self.data_tk.show()


class Scope(BaseGridW):
    def __init__(self, scope_cs):
        super().__init__()

        self.tool_bar = ScopesTools()
        self.grid.addWidget(self.tool_bar, 0, 0)
        self.tool_bar.btn_resize.clicked.connect(self.rerange)
        self.tool_bar.legends_cb.stateChanged.connect(self.setLegendsVisible)

        self.pens = [(255, 0, 0), (0, 255, 0), (255, 0, 255), (255, 255, 0)]
        graph = pg.GraphicsLayoutWidget(parent=self)
        chans_map = scope_cs.chans_map
        plts = {}
        curvs = {}
        legends = {}
        c_count = 0
        for dk in cmap:
            plts[dk] = graph.addPlot() #(title=dk, autoDownsample=True)
            plts[dk].disableAutoRange()
            plts[dk].showGrid(x=True, y=True)
            legends[dk] = plts[dk].addLegend(offset=(1, 1), rowCount=1, colCount=4, horSpacing=18)
            g_count = 0
            for ck in cmap[dk]:
                c = chans_map[dk][ck]
                c.valueMeasured.connect(self.update_plot)
                curvs[c.name] = plts[dk].plot(c.val, pen=self.pens[g_count], name=cmap[dk][ck])
                g_count += 1

            c_count += 1
            if c_count == 2:
                graph.nextRow()
                c_count = 0

        self.graph, self.plts, self.legends, self.curvs, self.chans = graph, plts, legends, curvs, scope_cs.chans
        # put in grid
        self.grid.addWidget(graph, 1, 0)

    def update_plot(self, chan):
        self.curvs[chan.name].setData(chan.aval)

    def rerange(self):
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
            self.plts[dk].setXRange(0, self.chans[n].nelems, padding=0)

    def setLegendsVisible(self, state):
        for k in self.legends:
            self.legends[k].setVisible(state)


if __name__ == '__main__':
    from sys import argv, exit
    app = QApplication(argv)

    scope_chans = ScopesChansContainer()

    win = Scope(scope_chans)
    win.resize(1980, 1200)
    win.show()
    exit(app.exec_())
