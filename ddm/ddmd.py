#!/usr/bin/env python3
import sys
from aux.service_daemon import Service
from aQt.QtCore import QCoreApplication
from injext_looper import InjExtLoop

# remove this when demonization added
# import signal
#signal.signal(signal.SIGINT, signal.SIG_DFL)



def clean():
    print('exiting doom\'s day machine')
    app.quit()
    sys.stdout.flush()

def run_main():
    global app
    app = QCoreApplication(sys.argv)
    injext_loop = InjExtLoop()
    app.exec_()


ddmd = Service("ddmd", run_main, clean)

