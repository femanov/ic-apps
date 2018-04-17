#!/usr/bin/env python

import cothread

from PyQt4.QtGui import *
from submachines import *
from settings.cx import *


# class RingInEx(QMainWindow):
#
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#         uic.loadUi('ddm_mini.ui', self)
#         self.show()
#
#         # task combobox action
#         self.task.currentIndexChanged.connect(self.taskcb)
#
#         self.ddma = ddma()
#
#         self.ddma.linStarter.shotsLeftChanged.connect(self.nshot.setValue)
#
#         self.ddma.extractor.startSrcChanged.connect(self.startsrc.setValue)
#         self.startsrc.done.connect(self.ddma.extractor.setStartSrc)
#
#         self.ddma.linStarter.runmodeChanged.connect(self.linacRunmode.setValue)
#         self.linacRunmode.done.connect(self.ddma.linStarter.setRunmode)
#
#         self.eshots.done.connect(self.ddma.setEshots)
#         self.eshots.setValue(10)
#         self.pshots.done.connect(self.ddma.setPshots)
#         self.pshots.setValue(20)
#
#         self.particles.done.connect(self.ddma.setParticles)
#
#         self.modedelay.done.connect(self.ddma.mode_switch.setDelay)
#         self.modedelay.setValue(3000)
#
#         self.ddma.stateChanged.connect(self.showState)
#
#         # Button Actions
#         self.fire.clicked.connect(self.ddma.inject)
#         self.stop.clicked.connect(self.ddma.stop)
#         self.extract.clicked.connect(self.ddma.extract)
#         self.autofire.clicked.connect(self.ddma.execBurst)
#         self.round.clicked.connect(self.ddma.execRound)
#
#         self.ddma.icmodeChanged.connect(self.icmode.setValue)
#
#     def showState(self, state):
#         self.statusbar.showMessage(self.ddma.stateMsg[state])
#
#     def taskcb(self, index):
#         self.task = index


class ddm_middle:
    def __init__(self):

        self.ddma = ddma()

        # register command channels
        self.fire_chan = cda.strchan(ctl_server + ".ddm.fire@u")
        self.stop_chan = cda.strchan(ctl_server + ".ddm.stop@u")
        self.round_chan  = cda.
        self.extract_chan = cda.strchan(ctl_server + ".ddm.extract@u")
        self.autofire_chan = cda.strchan(ctl_server + ".ddm.autofire@u")

        self.eshots_chan = cda.strchan(ctl_server + ".ddm.eshots@u")
        self.pshots_chan = cda.strchan(ctl_server + ".ddm.pshots@u")
        self.mode_delay_chan = cda.strchan(ctl_server + ".ddm.mode_delay@u")


self.mode_delay_chan = cda.strchan(ctl_server + ".ddm.mode_delay@u")

app = cothread.iqt()

mid = ddm_middle()

cothread.WaitForQuit()
