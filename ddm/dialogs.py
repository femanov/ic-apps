
from PyQt4 import QtGui
from PyQt4 import uic

class save_mode_dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi('ddm_save_mode.ui', self)
        self.show()

    def getComent(self):
        return self.comment.toPlainText()
