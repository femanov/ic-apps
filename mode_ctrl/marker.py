#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSignal
from cxwidgets import BaseGridW

from acc_db.mode_list import ModeListFilter, ModeList
from acc_db.db import ModesDB
from acc_ctl.mode_ser import ModesClient


class ModeListFiltered(BaseGridW):
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
    mark = pyqtSignal(int, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modes_db = ModesDB()

        self.grid.addWidget(QLabel("mark:"), 0, 0)
        self.grid.addWidget(QLabel("mode:"), 0, 2)
        self.grid.addWidget(QLabel("name:"), 1, 0)
        self.grid.addWidget(QLabel("author:"), 1, 2)
        self.grid.addWidget(QLabel("comment:"), 2, 0)

        self.mark_sel = QComboBox()
        self.grid.addWidget(self.mark_sel, 0, 1)

        self.name_line = QLineEdit()
        self.grid.addWidget(self.name_line, 1, 1)
        self.name_line.setMaxLength(4)

        self.author_line = QLineEdit()
        self.grid.addWidget(self.author_line, 1, 3)

        self.comment_line = QLineEdit()
        self.grid.addWidget(self.comment_line, 2, 1, 1, 3)

        self.btn_mark = QPushButton('mark')
        self.grid.addWidget(self.btn_mark, 1, 4)
        self.btn_mark.clicked.connect(self.mark_cb)

        self.btn_unmark = QPushButton('unmark')
        self.grid.addWidget(self.btn_unmark, 2, 4)

        self.n_rows = 0
        self.marks = None
        self.selected_mode_id = None
        self.mark_sel.currentIndexChanged.connect(self.set_mark)

    def set_mode(self, mode_id):
        self.selected_mode_id = mode_id
        self.modes_db.execute("select count(id) from modemark where mode_id=%s", (mode_id,))
        self.n_rows = self.modes_db.cur.fetchall()[0][0]
        self.mark_sel.clear()
        self.clear_data()
        if self.n_rows == 0:
            self.marks = None
            return
        self.modes_db.execute("select id,name,author,comment from modemark where mode_id=%s", (mode_id,))
        self.marks = self.modes_db.cur.fetchall()
        for x in self.marks:
            self.mark_sel.addItem(x[1], x[0])

    def set_mark(self, index):
        if index < 0:
            return
        raw = self.marks[index]
        self.name_line.setText(raw[1])
        self.author_line.setText(raw[2])
        self.comment_line.setText(raw[3])

    def clear_data(self):
        self.name_line.setText("")
        self.author_line.setText("")
        self.comment_line.setText("")

    def mark_cb(self):
        name = self.name_line.text()
        comment = self.comment_line.text()
        author = self.author_line.text()
        self.mark.emit(self.selected_mode_id, name, comment, author)


class Marker(ModeListFiltered):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.modes_db = ModesDB()

        grow = self.grid.rowCount()
        self.mark_edit = MarksEditor()
        self.grid.addWidget(self.mark_edit, grow, 0)
        self.mark_edit.mark.connect(self.mark_mode)

        self.listw.modeSelected.connect(self.mark_edit.set_mode)

    def mark_mode(self, mode_id, name, comment, author):
        print(f"decided to make mark: {mode_id} {name}, {comment}, {author}")
        if name == "" or author == "":
            print("empty mark name or author not allowed")
            return
        self.modes_db.mark_mode(mode_id, name, comment, author)





app = QApplication(['mode list test'])

w = Marker()
w.resize(900, 800)
w.show()


app.exec_()

