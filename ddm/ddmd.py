#!/usr/bin/env python3
import sys
from aux.service_daemon import CothreadQtService
from injext_looper import InjExtLoop


class DDMService(CothreadQtService):
    def main(self):
        self.injext_loop = InjExtLoop()

    def clean(self):
        self.log_str('exiting doom\`s day machine')


ddmd = DDMService("ddmd")

