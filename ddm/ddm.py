#!/usr/bin/env python3
from acc_ctl.ddm_ctl import DdmClient

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys


class RingInEx(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi('ddm.ui', self)

        with open("./style/buttons.qss", "r") as fh:
            self.setStyleSheet(fh.read())

        self.show()

        self.ddmc = DdmClient()

        #self.ddma.extractor.startSrcChanged.connect(self.startsrc.setValue)

        #self.startsrc.done.connect(self.ddma.extractor.setStartSrc)

        #self.ddma.linStarter.runmodeChanged.connect(self.linacRunmode.setValue)
        #self.linacRunmode.done.connect(self.ddma.linStarter.setRunmode)

        #self.eshots.done.connect(self.ddma.setEshots)
        #self.pshots.done.connect(self.ddma.setPshots)

        #self.particles.done.connect(self.ddma.setParticles)

        #self.modedelay.done.connect(self.ddma.modeCtl.setDelay)
        #self.modedelay.setValue(3000)

        #self.ddma.stateChanged.connect(self.showState)

        self.ddmc.nshotsUpdate.connect(self.nshot.setValue)


        # Button Actions
        self.fire.clicked.connect(self.ddmc.linrun)
        self.stop.clicked.connect(self.ddmc.stop)
        self.extract.clicked.connect(self.ddmc.extract)
        self.autofire.clicked.connect(self.ddmc.autorun)
        self.round.clicked.connect(self.ddmc.round)

        #self.ddma.icmodeChanged.connect(self.icmode.setValue)

    # def showState(self, state):
    #     self.statusbar.showMessage(self.ddma.stateMsg[state])
    #
    # def taskcb(self, index):
    #     self.task = index






app = QApplication(sys.argv)

win = RingInEx()


sys.exit(app.exec_())
