#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

import pycx4.q5cda as cda

# v2kCAS 172.16.1.110 20041
# v5CAS v2k-k500-1.inp.nsk.su 20041
#
#



class k500state():
    def __init__(self):
        super()

        self.schans = {
            'v5_cas':  cda.StrChan("vcas::v2k-k500-1:20041.VEPP5.K500.Mode"),
            'v2k_cas': cda.StrChan("vcas::172.16.1.110:20041.VEPP5.K500.Mode"),
        }




class K500stateWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('k500state.ui', self)

        #with open("./style/buttons.qss", "r") as fh:
        #    self.setStyleSheet(fh.read())








app = QApplication(sys.argv)


w = K500stateWidget()

w.show()

sys.exit(app.exec_())
