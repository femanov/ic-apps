#!/usr/bin/env python3

import pycx4.pycda as cda
from cservice import CXService
import time
from scopes_map import srv, cmap, c_sign, ltimer_scopes

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class RFScopesProc:
    def __init__(self):
        self.marker_chans = {}
        for k in ltimer_scopes:
            self.marker_chans[k] = cda.IChan(srv + '.' + k + '.marker', on_update=True)
            self.marker_chans[k].valueMeasured.connect(self.scope_measured)
        self.num_scopes = len(ltimer_scopes)
        self.updated_count = 0

        self.shot_c = cda.IChan(srv + '.' + "l_timer.shot", on_update=True)
        self.shot_c.setValue(1)

        self.phase_c = cda.IChan(srv + '.' + "l_timer.phase", on_update=True)
        #self.phase_c.valueMeasured.connect(self.print_val)
        self.gatestat_c = cda.IChan(srv + '.' + "l_timer.gatestat", on_update=True)
        #self.gatestat_c.valueMeasured.connect(self.print_val)
        self.event_c = cda.IChan(srv + '.' + "l_timer.event", on_update=True)
        #self.event_c.valueMeasured.connect(self.print_val)

        self.timer = cda.Timer()
        self.timer.singleShot(2000, proc=self.timeout_proc)
        self.t0 = time.time()


    def print_val(self, chan):
        print(chan.name, chan.val, chan.time)

    def scope_measured(self, chan):
        self.updated_count += 1
        if self.updated_count == self.num_scopes:
            self.shot_done(None)

    def shot_done(self, timer):
        self.updated_count = 0
        self.shot_c.setValue(self.shot_c.val+1)
        self.timer.singleShot(2000)

    def timeout_proc(self, timer):
        print('timed out? resetting', time.time() - self.t0)
        self.shot_c.setValue(1)
        self.t0 = time.time()
        self.timer.singleShot(1000)


class RFScopesProcService(CXService):
    def main(self):
        self.rf_proc = RFScopesProc()


s = RFScopesProcService('rf_scopes_proc')


#rf_proc = RFScopesProc()

#cda.main_loop()
