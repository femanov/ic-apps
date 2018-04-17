#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cothread
from cothread.catools import *

from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic

import dialogs

from cdr_wrapper import *
from actl import *
import json

class RingInEx(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('ddm1.ui', self)
        self.show()

        self.whlist = [self.egenc1dly,
                       self.egenc2dly,
                       self.egenc3dly,
                       self.egenc4dly,
                       self.eform1pdly,
                       self.eform1ndly,
                       self.eform2pdly,
                       self.eform2ndly,
                       self.euakk1,
                       self.euakk2,
                       self.egenc1mask,
                       self.egenc2mask,
                       self.egenc3mask,
                       self.egenc4mask,
                       self.eform1pmask,
                       self.eform1nmask,
                       self.eform2pmask,
                       self.eform2nmask,

                       self.pgenc1dly,
                       self.pgenc2dly,
                       self.pgenc3dly,
                       self.pgenc4dly,
                       self.pform1pdly,
                       self.pform1ndly,
                       self.pform2pdly,
                       self.pform2ndly,
                       self.puakk1,
                       self.puakk2,
                       self.pgenc1mask,
                       self.pgenc2mask,
                       self.pgenc3mask,
                       self.pgenc4mask,
                       self.pform1pmask,
                       self.pform1nmask,
                       self.pform2pmask,
                       self.pform2nmask
                       ]

        self.pvlist = ["V5:S:IE:E:Delay1C",
                       "V5:S:IE:E:Delay2C",
                       "V5:S:IE:E:Delay3C",
                       "V5:S:IE:E:Delay4C",
                       "V5:S:IE:E:Delay11C",
                       "V5:S:IE:E:Delay12C",
                       "V5:S:IE:E:Delay13C",
                       "V5:S:IE:E:Delay14C",
                       "V5:S:IE:E:Voltage1C",
                       "V5:S:IE:E:Voltage2C",
                       "V5:S:IE:E:DelayMaskC.B0",
                       "V5:S:IE:E:DelayMaskC.B1",
                       "V5:S:IE:E:DelayMaskC.B2",
                       "V5:S:IE:E:DelayMaskC.B3",
                       "V5:S:IE:E:Delay1MaskC.B0",
                       "V5:S:IE:E:Delay1MaskC.B1",
                       "V5:S:IE:E:Delay1MaskC.B2",
                       "V5:S:IE:E:Delay1MaskC.B3",

                       "V5:S:IE:P:Delay1C",
                       "V5:S:IE:P:Delay2C",
                       "V5:S:IE:P:Delay3C",
                       "V5:S:IE:P:Delay4C",
                       "V5:S:IE:P:Delay11C",
                       "V5:S:IE:P:Delay12C",
                       "V5:S:IE:P:Delay13C",
                       "V5:S:IE:P:Delay14C",
                       "V5:S:IE:P:Voltage1C",
                       "V5:S:IE:P:Voltage2C",
                       "V5:S:IE:P:DelayMaskC.B0",
                       "V5:S:IE:P:DelayMaskC.B1",
                       "V5:S:IE:P:DelayMaskC.B2",
                       "V5:S:IE:P:DelayMaskC.B3",
                       "V5:S:IE:P:Delay1MaskC.B0",
                       "V5:S:IE:P:Delay1MaskC.B1",
                       "V5:S:IE:P:Delay1MaskC.B2",
                       "V5:S:IE:P:Delay1MaskC.B3"
                       ]

        self.whlist_i = [self.egenc1dly_i,
                         self.egenc2dly_i,
                         self.egenc3dly_i,
                         self.egenc4dly_i,
                         self.eform1pdly_i,
                         self.eform1ndly_i,
                         self.eform2pdly_i,
                         self.eform2ndly_i,
                         self.euakk1_i,
                         self.euakk2_i,
                         self.egenc1mask_i,
                         self.egenc2mask_i,
                         self.egenc3mask_i,
                         self.egenc4mask_i,
                         self.eform1pmask_i,
                         self.eform1nmask_i,
                         self.eform2pmask_i,
                         self.eform2nmask_i,

                         self.pgenc1dly_i,
                         self.pgenc2dly_i,
                         self.pgenc3dly_i,
                         self.pgenc4dly_i,
                         self.pform1pdly_i,
                         self.pform1ndly_i,
                         self.pform2pdly_i,
                         self.pform2ndly_i,
                         self.puakk1_i,
                         self.puakk2_i,
                         self.pgenc1mask_i,
                         self.pgenc2mask_i,
                         self.pgenc3mask_i,
                         self.pgenc4mask_i,
                         self.pform1pmask_i,
                         self.pform1nmask_i,
                         self.pform2pmask_i,
                         self.pform2nmask_i,
                         ]

        self.whlist_e = [self.egenc1dly_e,
                         self.egenc2dly_e,
                         self.egenc3dly_e,
                         self.egenc4dly_e,
                         self.eform1pdly_e,
                         self.eform1ndly_e,
                         self.eform2pdly_e,
                         self.eform2ndly_e,
                         self.euakk1_e,
                         self.euakk2_e,
                         self.egenc1mask_e,
                         self.egenc2mask_e,
                         self.egenc3mask_e,
                         self.egenc4mask_e,
                         self.eform1pmask_e,
                         self.eform1nmask_e,
                         self.eform2pmask_e,
                         self.eform2nmask_e,

                         self.pgenc1dly_e,
                         self.pgenc2dly_e,
                         self.pgenc3dly_e,
                         self.pgenc4dly_e,
                         self.pform1pdly_e,
                         self.pform1ndly_e,
                         self.pform2pdly_e,
                         self.pform2ndly_e,
                         self.puakk1_e,
                         self.puakk2_e,
                         self.pgenc1mask_e,
                         self.pgenc2mask_e,
                         self.pgenc3mask_e,
                         self.pgenc4mask_e,
                         self.pform1pmask_e,
                         self.pform1nmask_e,
                         self.pform2pmask_e,
                         self.pform2nmask_e
                        ]

        self.cycle_pvs = ["V5:SYN:CountM",
                          "V5:SYN:Status00C.B4",
                          "V5:SYN:BPS:SwitchC"
                         ]

        self.cycle_wlist = [self.nshoot,
                            self.linacRunmode,
                            self.strobsrc
                           ]

        camonitor(self.pvlist, self.callback, format=FORMAT_CTRL)
        camonitor(self.cycle_pvs, self.cycle_cb, format=FORMAT_CTRL)

        for w in self.cycle_wlist:
            w.done.connect(self.setdata_cycle)

        for w in self.whlist:
            w.done.connect(self.setdata)

        # Menu Actions
        self.actionQuit.triggered.connect(exit)
        self.actionHw_ext.triggered.connect(self.hw2ext)
        self.actionHw_inj.triggered.connect(self.hw2inj)
        self.actionExt_hw.triggered.connect(self.ext2hw)
        self.actionInj_hw.triggered.connect(self.inj2hw)
        self.actionInj_hw.triggered.connect(self.inj2hw)
        self.actionSave_mode.triggered.connect(self.save_mode)
        self.actionLoad_mode.triggered.connect(self.load_mode)

        # Button Actions
        self.fire.clicked.connect(self.ic_fire)
        self.stop.clicked.connect(self.ic_stop)
        self.extract.clicked.connect(self.ext_fire)
        self.autofire.clicked.connect(self.auto_fire)

        # task combobox action
        self.task.currentIndexChanged.connect(self.taskcb)

        self.ic_ctl_pvs = ["V5:SYN:EventM",
                           "V5:SYN:Status00M",
                           "V5:SYN:BPS:EventM",
                           "V5:SYN:BPS:StatusM",
                           ""]

        self.mode_pv = dict.fromkeys(self.pvlist)

        self.mode_user_i = {}
        for x in self.whlist_i:
            self.mode_user_i[str(x.objectName)] = 0

        self.mode_user_e = {}
        for x in self.whlist_e:
            self.mode_user_e[str(x.objectName)] = 0


        self.state = 0
        self.linac_firemode = 0
        self.extraction_mask = 0
        self.fire = False
        self.auto = 0

        self.linac_eventm = 0

        self.task = 0  # manual operation mode by default
        # task indexes:
        # manual, store&stop, store&extract, keep current

        self.stage = 0
        self.stage_name = ["nothing", "prepare to inject", "injecting",
                           "prepare to extract", "extracting", ""]

    def auto_fire(self):
        self.auto = 1

    def inj_prepare(self):
        self.inj2hw()
        if self.linac_firemode == 0:
            caput("V5:SYN:Status00C.B4", 1)
            self.linac_firemode = 1
        #update counter value
        caput("V5:SYN:CountC", self.eshots.value())
        #mask extraction channel
        caput("V5:SYN:BPS:MaskC.B0", 1)

    def inject(self):
        self.statusbar.showMessage("injecting....")
        caput("V5:SYN:StartC.PROC", 1)
        self.linac_eventm = caget("V5:SYN:EventM")
        self.linac_eventm_pv = camonitor("V5:SYN:EventM", self.injection_done)

    def injection_done(self, value):
        if value == self.linac_eventm:
            return
        self.linac_eventm_pv.close()
        self.statusbar.showMessage("injection done: cycle %d" % value)
        if self.task == 0:  # manual injection
            self.statusbar.showMessage("injection done: stop")
            return
        if self.task == 1:  # store & stop
            self.statusbar.showMessage("injection done: task done")
            return
        if self.task == 2:  # store & extract
            self.statusbar.showMessage("injection done: extracting")
            return

    def ext_prepare(self):
        self.ext2hw()
        # forbid linac FIRE
        caput("V5:SYN:StopC.PROC", 1)
        #unmask extraction channel
        caput("V5:SYN:BPS:MaskC.B0", 0)

    def ext_fire(self):
        self.ext_prepare()
        self.statusbar.showMessage("extracting...")
        # allow extraction
        caput("V5:SYN:BPS:StartC.PROC", 1)
        self.ext_eventm = caget("V5:SYN:BPS:EventM")
        self.ext_eventm_pv = camonitor("V5:SYN:BPS:EventM", self.extracted)

    def extracted(self, value):
        if value == self.ext_eventm:
            return
        self.statusbar.showMessage("beam extracted!")
        self.ext_eventm_pv.close()

    def ic_fire(self):
        print "fired"
        self.fire = True
        self.inj_prepare()
        self.inject()


    def ic_stop(self):
        self.fire = False
        caput("V5:SYN:StopC.PROC", 1)
        print "stopped"

    def cycle_cb(self, value, index):
        self.cycle_wlist[index].setValue(value)

    def setdata_cycle(self, value):
        ind = self.cycle_wlist.index(self.sender())
        caput(self.cycle_pvs[ind], value)

    def callback(self, value, index):
        self.whlist[index].setValue(value)
        self.mode_pv[self.pvlist[index]] = value

    def setdata(self, value):
        ind = self.whlist.index(self.sender())
        caput(self.pvlist[ind], value)


    def hw2ext(self):
        for x in self.whlist_e:
            x.setValue(self.whlist[self.whlist_e.index(x)].value())

    def hw2inj(self):
        for x in self.whlist_i:
            x.setValue(self.whlist[self.whlist_i.index(x)].value())

    def inj2hw(self):
        for x in self.whlist_i:
            self.whlist[self.whlist_i.index(x)].setValue(x.value())

    def ext2hw(self):
        for x in self.whlist_e:
            self.whlist[self.whlist_e.index(x)].setValue(x.value())

    def save_mode(self):
        dlg = dialogs.save_mode_dialog(self)
        if dlg.exec_():
            comment = dlg.getComent()
            self.mode_pv["comment"] = str(comment)
            print(json.dumps(self.mode_pv, indent=4))
            for x in self.whlist_i:
                self.mode_user_i[str(x.objectName())] = x.value()
            for x in self.whlist_e:
                self.mode_user_e[str(x.objectName())] = x.value()

            print(json.dumps(self.mode_user_i, indent=4))
            print(json.dumps(self.mode_user_e, indent=4))


    def load_mode(self):
        pass


    def taskcb(self, index):
        self.task = index






app = cothread.iqt()

win = RingInEx()


cothread.WaitForQuit()
