#!/usr/bin/env python3
from cservice import CXService
import pycx4.pycda as cda
from injext_looper import InjExtLoop
from ic_modules.acc_ctl.beam_switch import LinBeamSwitch


class DDMService(CXService):
    def main(self):
        self.injext_loop = InjExtLoop()
        self.b_swc = LinBeamSwitch()


    def clean(self):
        self.log_str('exiting doom\`s day machine daemon')


ddmd = DDMService("ddmd")

