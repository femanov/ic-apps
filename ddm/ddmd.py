#!/usr/bin/env python3

from PyQt5 import QtCore

# remove this when demonization added
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)



from injext_looper import InjExtLoop

import sys


app = QtCore.QCoreApplication(sys.argv)


injext_loop = InjExtLoop()


app.exec_()
