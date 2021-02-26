#!/usr/bin/env python3

import pycx4.pycda as cda
from cservice import CXService
from time import sleep

class RFScopesProc:
    def __init__(self):
        self.shot_c = cda.IChan("cxhw:15.l_timer.shot", on_update=True)

        self.scopes_update_c = cda.IChan("cxhw:15.adc250_9a.marker", on_update=True)
        self.scopes_update_c.valueMeasured.connect(self.shot_done)
        self.shot_c.setValue(1)

    def shot_done(self, chan):
        sleep(0.5)
        self.shot_c.setValue(self.shot_c.val+1)
        print("shot done")

class RFScopesProcService(CXService):
    def main(self):
        self.rf_proc = RFScopesProc()


#s = RFScopesProcService('rf_scopes_proc')


rf_proc = RFScopesProc()

cda.main_loop()
