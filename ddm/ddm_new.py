#!/usr/bin/env python3

from aux.Qt import QtCore, QtGui, QtWidgets

from fwidgets.cx_spinbox import CXSpinBox
from fwidgets.cx_checkbox import CXCheckBox
from fwidgets.cx_pushbutton import CXPushButton


from training_ctl_widget import TrainingCtlW


class Line(QtWidgets.QFrame):
    def __init__(self, *args):
        super(Line, self).__init__(*args)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(3)

class InjExtCtl(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(InjExtCtl, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        self.grid.addWidget(QtWidgets.QLabel("injection/extraction control"),
                            0, 0, 1, 4, QtCore.Qt.AlignHCenter)

        self.grid.addWidget(QtWidgets.QLabel("e-shots"), 1, 0)
        self.sb_eshots = CXSpinBox(cname='cxhw:0.ddm.eshots')
        self.grid.addWidget(self.sb_eshots, 1, 1)

        self.grid.addWidget(QtWidgets.QLabel("p-shots"), 1, 2)
        self.sb_eshots = CXSpinBox(cname='cxhw:0.ddm.pshots')
        self.grid.addWidget(self.sb_eshots, 1, 3)


        self.b_inject = CXPushButton('Inject', cname='cxhw:0.ddm.inject')
        self.grid.addWidget(self.b_inject, 2, 0)

        self.b_extract = CXPushButton('Extract', cname='cxhw:0.ddm.extract')
        self.grid.addWidget(self.b_extract, 2, 1)

        self.b_round = CXPushButton('Round', cname='cxhw:0.ddm.nround')
        self.grid.addWidget(self.b_round, 3, 0)

        self.b_auto = CXPushButton('Auto', cname='cxhw:0.ddm.autorun')
        self.grid.addWidget(self.b_auto, 3, 1)

        self.b_stop = CXPushButton('Stop', cname='cxhw:0.ddm.stop')
        self.grid.addWidget(self.b_stop, 3, 2)

        self.grid.addWidget(Line(), 4, 0, 1, 4)

        self.grid.addWidget(QtWidgets.QLabel("shots left"), 5, 0)
        self.sb_nshots = CXSpinBox(cname='canhw:19.syn_ie4.ie_bum')
        self.grid.addWidget(self.sb_nshots, 5, 1)




class DDMWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DDMWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        self.extr_trainer = TrainingCtlW()
        self.grid.addWidget(self.extr_trainer, 0, 0)

        self.grid.addWidget(Line(), 1, 0)

        self.inj_ext = InjExtCtl()
        self.grid.addWidget(self.inj_ext, 2, 0)



        #self.grid.addWidget(QtWidgets.QLabel("Automatic Injection/extraction control"), 2, 0, 1, 4, QtCore.Qt.AlignHCenter)




app = QtWidgets.QApplication(['DDM_test'])

w = DDMWidget()
w.show()

app.exec_()
