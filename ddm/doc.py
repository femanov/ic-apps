#low-Level

class LinStarter(QObject):
    runmodeChanged = pyqtSignal(int)
    shotsLeftChanged = pyqtSignal(int)
    counterRunChanged = pyqtSignal(int)
    neventsChanged = pyqtSignal(int)
    runDone = pyqtSignal()

    def setRunmode(self, mode):
    def setCounter(self, nshots):
    def startCounter(self):
    def stopCounter(self):
    def newCounterCycle(self, nshots):



class Extractor(QObject):
    eventCountChanged = pyqtSignal(int)
    extractMaskChanged = pyqtSignal(int)
    startSrcChanged = pyqtSignal(int)
    extractionDone = pyqtSignal()

    def setClockSrc(self, value):
    def setExtractMask(self, mask):
    def stopExtraction(self):
    def extract(self):


class ICLoop(QObject):
    stateChanged = pyqtSignal(int)
    stateMsg = pyqtSignal(str)
    icmodeChanged = pyqtSignal(int)

    # stage events
    preparing2inject = pyqtSignal()
    injecting = pyqtSignal()
    injected = pyqtSignal()
    preparing2extract = pyqtSignal()
    extracting = pyqtSignal()
    extracted = pyqtSignal()

    def setParticles(self, particles):
    def setEshots(self, num):
    def setPshots(self, num):
    def stop(self):
    def inject(self):
    def extract(self):
    def execRound(self):
    def execBurst(self):


