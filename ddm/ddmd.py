#!/usr/bin/env python3

from ic_loop import *
from acc_ctl.ddm_ctl import DdmServer

from PyQt5 import QtCore
import cothread
import signal
import sys

def sigint_proc(signum, frame):
    print('\nexiting...')
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_proc)

a = QtCore.QCoreApplication(sys.argv)
app = cothread.iqt()

ddms = DdmServer()  # doom's day machne server

ic_loop = ICLoop()  # injection complex 0-level automatics

# updateEshots = pyqtSignal(float)
# updatePshots = pyqtSignal(float)
# updateLinRunmode = pyqtSignal(float)
# updateModeDelay = pyqtSignal(float)

# updateParticles = pyqtSignal(float)
# updateClockSrc = pyqtSignal(float)


ddms.updateEshots.connect(ic_loop.setEshots)
ddms.updatePshots.connect(ic_loop.setPshots)





# ic_loop.linStarter.runmodeChanged.connect(ddms.linacRunmode)
# ddms.setLinRunmode.connect(ic_loop.linStarter.setRunmode)
#
# ddms.setEshots.connect(ic_loop.setEshots)
# ddms.setPshots.connect(ic_loop.setPshots)
# ddms.setParticles.connect(ic_loop.setParticles)
#
# ic_loop.linStarter.runDone.connect(ddms.injected_send)
# ic_loop.extractor.extractionDone.connect(ddms.extracted_send)




cothread.WaitForQuit()
