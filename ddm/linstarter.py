
from PyQt5.QtCore import QObject, pyqtSignal
import pycx4.pycda as cda

runmodes = {
    'continous': 0,
    'counter':   1
}

#CX version names:
# syn_ie4.mode
# syn_ie4.re_bum
# syn_ie4.bum_start
# syn_ie4.bum_stop
# syn_ie4.ie_bum
# syn_ie4.bum_going
# syn_ie4.lam_sig

class LinStarter(QObject):
    runmodeChanged = pyqtSignal(int)
    shotsLeftChanged = pyqtSignal(int)
    counterRunChanged = pyqtSignal(int)
    neventsChanged = pyqtSignal(int)
    runDone = pyqtSignal()

    def __init__(self):
        super(LinStarter, self).__init__()

        # state variables.
        self.runmode = 0  # 0 - continous, 1 - counter
        self.runRequested = 0  # 0 - run not requested, 1 - requested
        self.counterRun = 0  # 0 - not running, 1 - running
        self.shotsLeft = 0  #  - stop point
        self.nevents = 0  # inctementing when counter cycle ends
        self.nshots = 0  # number of requested shots

        # catools.camonitor("ic.linac.shotCount", self.shotsLeftUpdate, datatype=int)
        # catools.camonitor("ic.linac.shotCycle", self.neventsUpdate, datatype=int)
        # catools.camonitor("ic.linac.runStatus", self.statusUpdate, datatype=int)

        self.c_runmode = cda.DChan('syn_ie4.mode')
        self.c_start = cda.DChan('syn_ie4.bum_start')
        self.c_stop = cda.DChan('syn_ie4.bum_stop')
        self.c_runmode = cda.DChan('syn_ie4.mode')



    def shotsLeftUpdate(self, value):
        self.shootsLeft = value
        self.shotsLeftChanged.emit(value)
        if value > 3500 and value < 4094:
            self.stopCounter()
            print("stop error")

    def neventsUpdate(self, value):
        self.nevents = value
        self.neventsChanged.emit(value)
        if self.runRequested == 1:
            self.runRequested = 0
            self.runDone.emit()

    def statusUpdate(self, value):
        runmode = (value & 0b10000) >> 4
        counterRun = int(not ((value & 0b1000000) >> 6))

        if self.runmode != runmode:
            self.runmode = runmode
            if self.runmode == 0:
                self.runRequested = 0
            self.runmodeChanged.emit(runmode)
        if counterRun != self.counterRun:
            self.counterRun = counterRun

            self.counterRunChanged.emit(counterRun)

    # Low Level requests

    def setRunmode(self, mode):
        if isinstance(mode, str):
            mode_val = runmodes[mode]
        else:
            mode_val = mode
        if self.runmode != mode_val:
            catools.caput("ic.linac.runmode", mode_val)

    def setCounter(self, nshots):
        if self.shotsLeft == nshots:
            self.shotsLeftChanged.emit(nshots)
            return
        catools.caput("ic.linac.shotNum", nshots)

    def startCounter(self):
        if self.runmode == 1 and self.counterRun == 0:
            self.runRequested = 1
            catools.caput("ic.linac.runCounter", 1)  # run
        else:
            catools.caput("ic.linac.runCounter", 1)  # run
            print("running")

    def stopCounter(self):
        if self.runRequested and self.counterRun == 1:
            catools.caput("ic.linac.stopCounter", 1)
            self.runRequested = 0

    # High Level Requests
    def newCounterCycle(self, nshots):
        if self.nshots != nshots:
            self.setCounter(nshots)
        self.startCounter()
