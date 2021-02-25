#!/usr/bin/env python3

import pycx4.pycda as cda
from cservice import CXService

class RFScopesProc:
    def __init__(self):
        self.shot_c = cda.IChan("cxhw:15.l_timer.shot")

        self.scopes_update_c = cda.IChan("cxhw:15.adc250_9c.marker")
        self.scopes_update_c.valueMeasured.connect(self.shot_done)

    def shot_done(self, chan):
        self.shot_c.setValue(1)


class RFScopesProcService(CXService):
    def main(self):
        self.rf_proc = RFScopesProc()


s = RFScopesProcService('dcct_proc')
