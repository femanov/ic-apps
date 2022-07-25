#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton


from acc_db.mode_list import *


class ModeListFiltered(BaseGridW):
    markMode = QtCore.pyqtSignal(int, str, str, str)  # mode_id, mark_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modes_db = ModesDB()

        self.filterw = ModeListFilter()
        self.grid.addWidget(self.filterw, 0, 0)

        self.listw = ModeList(db=self.modes_db)
        self.grid.addWidget(self.listw, 1, 0)

        self.update_modenum()
        self.filterw.set_nrows(100)
        self.filterw.ctrlsUpdate.connect(self.listw.update_modelist)

    # def mode_sel_cb(self, mode_id):
    #     if self.selected_mode is None and mode_id > 0:
    #         self.ctrlw.mark.connect(self.mark_cb)
    #     self.selected_mode = mode_id

    # def mark_cb(self, mark):
    #     self.markMode.emit(self.selected_mode, mark, 'saver', 'automatic mode')

    def update_modenum(self):
        self.modes_db.execute("select count(id) from mode")
        m_num = self.modes_db.cur.fetchall()[0][0]
        self.filterw.set_maxrows(m_num)

    def update_modelist(self, update_marked=False):
        fvals = self.filterw.vals()
        if update_marked:
            fvals['update_marked'] = True
        self.listw.update_modelist(**fvals)


class MarksEditor(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("name:"), 0, 0)
        self.grid.addWidget(QLabel("author:"), 1, 0)

        self.name_line = QLineEdit()
        self.grid.addWidget(self.name_line, 0, 1)

        self.author_line = QLineEdit()
        self.grid.addWidget(self.author_line, 1, 1)

        self.btn_save = QPushButton('save')
        self.grid.addWidget(self.btn_save, 0, 2, 2, 1)
        #self.btn_save.clicked.connect(self.save_cb)


class Marker(ModeListFiltered):
    def __init__(self, parent=None):
        super().__init__(parent)

        grow = self.grid.rowCount()
        self.mark_edit = MarksEditor()
        self.grid.addWidget(self.mark_edit, grow, 0)


app = QApplication(['mode list test'])

w = Marker()
w.resize(900, 800)
w.show()


app.exec_()

