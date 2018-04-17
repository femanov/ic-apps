#!/usr/bin/env python3

import sys

from aux import str2u
from aux.Qt import QtCore, QtGui, uic, QtWidgets

from acc_ctl.mode_ser import ModesClient
from acc_db.chan_kinds import KindTable
from acc_db.sys_tree import *

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_row = None
        self.mode_list = None
        uic.loadUi('saver.ui', self)
        with open("./saver.qss", "r") as fh:
            self.setStyleSheet(fh.read())
        self.show()

        self.mark_colors = ['#efebe7', '#efebe7', '#efebe7', '#efebe7',
                            '#55ffff', '#ff86ff', '#75ff91', '#ff6b6b']
        self.marks = ['einj', 'eext', 'pinj', 'pext', 'e2v4', 'p2v4', 'e2v2', 'p2v2']

        self.like = None
        self.num_modes = 0

        self.db = acc_db()

        self.tableWidgetmodes.cellClicked.connect(self.mode_select)

        self.nrows_spinbox.setValue(100)
        self.nrows_spinbox.setMinimum(0)
        self.startrow_spinbox.setMinimum(0)
        self.maxrows_spinbox.setReadOnly(True)
        self.nrows_spinbox.done.connect(self.update_adapter)
        self.startrow_spinbox.done.connect(self.update_adapter)

        self.update_nummodes()
        self.update_modelist()
        self.row_background = self.tableWidgetmodes.item(0, 0).background()

        self.devtree = DevTree(self.sysTree, False, False)
        self.kindctl = KindTable(self.kindTable)

        self.markButs = [self.pushButtonMarkeinj, self.pushButtonMarkeext, self.pushButtonMarkpinj,
                         self.pushButtonMarkpext, self.pushButtonMarke2v4, self.pushButtonMarkp2v4,
                         self.pushButtonMarke2v2, self.pushButtonMarkp2v2]
        for x in range(len(self.marks)):
            self.markButs[x].clicked.connect(self.mark)
            self.markButs[x].setStyleSheet('QPushButton {background-color:' + self.mark_colors[x] + '; }')

        self.pushButtonArchive.clicked.connect(self.archive)
        self.pushButtonArchive.setStyleSheet("QPushButton {background-color:#ff0000; }")
        self.pushButtonSave.clicked.connect(self.save_mode)
        self.commentLine.returnPressed.connect(self.save_mode)
        self.pushButtonLoad.clicked.connect(self.load_mode)

        self.lineEditLike.editingFinished.connect(self.update_like)

        self.pushButtonPrev.clicked.connect(self.prev_modes)
        self.pushButtonNext.clicked.connect(self.next_modes)

    def prev_modes(self):
        offset = self.startrow_spinbox.value()
        limit = self.nrows_spinbox.value()
        if offset - limit >= 0:
            self.startrow_spinbox.setValue(offset-limit)


    def next_modes(self):
        offset = self.startrow_spinbox.value()
        limit = self.nrows_spinbox.value()
        if offset + limit < self.num_modes:
            self.startrow_spinbox.setValue(offset+limit)


    def mode_select(self, row, col):
        if self.selected_row is not None:
            self.tableWidgetmodes.item(self.selected_row, 0).setBackground(self.row_background)
            self.tableWidgetmodes.item(self.selected_row, 1).setBackground(self.row_background)
            self.tableWidgetmodes.item(self.selected_row, 2).setBackground(self.row_background)
        self.selected_row = row
        self.tableWidgetmodes.item(row, 0).setBackground(QtGui.QColor(0, 255, 255))
        self.tableWidgetmodes.item(row, 1).setBackground(QtGui.QColor(0, 255, 255))
        self.tableWidgetmodes.item(row, 2).setBackground(QtGui.QColor(0, 255, 255))

    def update_like(self):
        like_in = str(self.lineEditLike.text())
        if like_in == '':
            self.like = None
        else:
            self.like = '%' + like_in + '%'
        self.update_nummodes()
        self.update_modelist()

    def update_nummodes(self):
        if self.like is None:
            self.db.execute("SELECT count(id) from mode where archived=0")
        else:
            self.db.execute("SELECT count(id) from mode where archived=0 and (author ILIKE %s or comment ILIKE %s)",
                            (self.like, self.like))
        self.num_modes = self.db.cur.fetchall()[0][0]
        self.db.conn.commit()
        self.maxrows_spinbox.setValue(self.num_modes)

    def update_adapter(self, num):
        self.update_modelist()

    def update_modelist(self):
        # select marked modes
        self.db.execute("SELECT mode.id,mode.author,mode.comment,mode.stime,modemark.id,modemark.name FROM mode"
                        " LEFT JOIN modemark on mode.id = modemark.mode_id"
                        " WHERE modemark.id IS NOT NULL ORDER BY mode.stime DESC")
        marked = self.db.cur.fetchall()
        self.db.conn.commit()

        # select all modes with like
        limit = self.nrows_spinbox.value()
        offset = self.startrow_spinbox.value()
        unmarked = self.db.mode_list(limit, offset, self.like)

        self.tableWidgetmodes.setRowCount(len(marked) + len(unmarked))
        for ind in range(len(marked)):
            row = marked[ind]
            item = QtWidgets.QTableWidgetItem(row[1])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidgetmodes.setItem(ind, 0, item)
            item = QtWidgets.QTableWidgetItem(row[2])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidgetmodes.setItem(ind, 1, item)
            item = QtWidgets.QTableWidgetItem(row[3].strftime("%Y-%m-%d %H:%M:%S"))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidgetmodes.setItem(ind, 2, item)
            item = QtWidgets.QTableWidgetItem(row[5])
            if marked[ind][4] <= len(self.mark_colors):
                item.setBackground(QtGui.QColor(self.mark_colors[row[4] - 1]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidgetmodes.setItem(ind, 3, item)

        row_shift = len(marked)
        for ind in range(len(unmarked)):
            row = unmarked[ind]
            item = QtWidgets.QTableWidgetItem(row[1])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidgetmodes.setItem(row_shift + ind, 0, item)
            item = QtWidgets.QTableWidgetItem(row[2])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidgetmodes.setItem(row_shift + ind, 1, item)
            item = QtWidgets.QTableWidgetItem(row[3].strftime("%Y-%m-%d %H:%M:%S"))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidgetmodes.setItem(row_shift + ind, 2, item)

        self.tableWidgetmodes.resizeRowsToContents()
        self.tableWidgetmodes.resizeColumnsToContents()

        self.selected_row = None
        self.mode_list = marked + unmarked

    def save_mode(self):
        comment = str2u(self.commentLine.text())
        if len(comment) == 0:
            return
        author = str2u(self.authorLine.text())
        mode_client.save_mode(author, comment)
        self.commentLine.setText("")
        self.statusBar.showMessage("saving mode....")

    def mode_saved(self):
        self.update_nummodes()
        self.update_modelist()
        self.statusBar.showMessage("mode saved")

    def load_mode(self):
        if self.selected_row is None:
            self.statusBar.showMessage('mode not selected')
            return
        tree_list = self.devtree.ntree.br_list
        syslist = [x.db_id for x in tree_list if x.selected == 2]
        sel_types = self.kindctl.selected()
        mode_client.load_mode(self.mode_list[self.selected_row][0], syslist, sel_types)
        self.statusBar.showMessage('loading mode...')

    def mode_loaded(self, msg):
        self.statusBar.showMessage("mode loaded:" + msg)

    def archive(self):
        if self.selected_row is None:
            self.statusBar.showMessage('mode not selected')
            return
        self.db.archive_mode(self.mode_list[self.selected_row][0])
        self.update_modelist()

    def mark(self):
        if self.selected_row is None:
            self.statusBar.showMessage('mode not selected')
            return
        ind = self.markButs.index(self.sender())
        mode_client.mark_mode(self.mode_list[self.selected_row][0], self.marks[ind], '', 'saver', ind+1)

    def update_db(self):
        self.update_nummodes()
        self.update_modelist()


app = QtWidgets.QApplication(sys.argv)

mode_client = ModesClient()

win = MyWindow()

mode_client.modeSaved.connect(win.mode_saved)
mode_client.modeLoaded.connect(win.mode_loaded)
mode_client.update.connect(win.update_db)

sys.exit(app.exec_())