from PyQt5.QtCore import QObject, pyqtSignal
import cothread.catools as catools


class Extractor(QObject):
    eventCountChanged = pyqtSignal(int)
    extractMaskChanged = pyqtSignal(int)
    startSrcChanged = pyqtSignal(int)
    extractionDone = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.extractMask = 0  # 0 - no mask, 1 - mask
        self.extractStatus = 0
        self.extractRequest = 0  # 0 - idle, 1 - requested
        self.eventCount = 0    # incrementing when cycle end.
        self.clockSrc = 0  # source of starting signals
        # to make further access to following PV's faster
        self.pvs_connect = [
            "ic.syn.xfer.extract.mask",
            "ic.extractor.run",
            "ic.extractor.stop"
        ]
        catools.connect(self.pvs_connect)

        catools.camonitor("ic.extractor.eventCount", self.eventUpdate, datatype=int)
        catools.camonitor("ic.extractor.status", self.statusUpdate, datatype=int)
        catools.camonitor("ic.syn.xfer.mask.rbv", self.maskUpdate, datatype=int)
        catools.camonitor("ic.extractor.clockSrc", self.clockSrcUpdate, datatype=int)

    def eventUpdate(self, value):
        self.eventCount = value
        self.eventCountChanged.emit(value)
        if self.extractRequest == 1:
            self.extractRequest = 0
            self.extractionDone.emit()

    def statusUpdate(self, value):
        extractStatus = (value & 0b01000000) >> 6
        if self.extractStatus != extractStatus:
            self.extractStatus = extractStatus

    def maskUpdate(self, value):
        maskB0 = value & 0b1
        if self.extractMask == maskB0:
            self.extractMask = maskB0
            self.extractMaskChanged.emit(maskB0)

    def clockSrcUpdate(self, value):
        self.clockSrc = value
        self.clockSrcChanged.emit(value)

    def setClockSrc(self, value):
        if self.clockSrc != value:
            catools.caput("ic.extractor.clockSrc", value)

    def setExtractMask(self, mask):
        if self.extractMask != mask:
            catools.caput("ic.extractor.mask.set", mask)

    def stopExtraction(self):
        if self.extractRequest == 1:
            self.extractRequest = 0
            catools.caput("ic.extractor.stop", 1)
            return True
        return False

    def extract(self):
        if self.extractRequest == 0:
            catools.caput("ic.extractor.run", 1)
            self.extractRequest = 1
            return True
        return False
