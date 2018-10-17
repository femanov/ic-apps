#!/usr/bin/env python3

import time
#import sys
#import datetime

from aux import str2u
from aux.Qt import QtCore, QtGui, uic, QtWidgets
from acc_db.mode_list import ModeListFull
from acc_db.sys_tree import SysTree
from acc_db.chan_kinds import KindTable
from acc_ctl.mode_ser import ModesClient


class SaverWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SaverWidget, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        self.flist = ModeListFull()
        self.flist.setFixedSize(800, 800)
        self.grid.addWidget(self.flist, 0, 0, 2, 1)

        self.stree = SysTree()
        self.grid.addWidget(self.stree, 0, 1)
        self.stree.selectionChanged.connect(self.sys_cb)

        self.kindt = KindTable()
        self.kindt.setFixedSize(350, 160)
        self.grid.addWidget(self.kindt, 1, 1)
        self.kindt.selectionChanged.connect(self.kinds_cb)

        self.status_text = QtWidgets.QPlainTextEdit()
        self.status_text.setFixedHeight(40)
        self.status_text.setReadOnly(True)
        self.status_text.setCenterOnScroll(True)
        self.grid.addWidget(self.status_text, 2, 0, 1, 2)

        self.selected_kinds = self.kindt.selected()
        self.selected_sys = []

        self.flist.ctrlw.load.connect(self.load_mode)

        self.mode_cli = ModesClient()
        self.mode_cli.modeSaved.connect(self.mode_saved)
        self.mode_cli.modeLoaded.connect(self.mode_loaded)
        self.mode_cli.update.connect(self.update_db)

        self.flist.saveMode.connect(self.save)
        self.flist.outMsg.connect(self.print_msg)
        self.flist.markMode.connect(self.mode_cli.mark_mode)

    def sys_cb(self, syslist):
        self.selected_sys = syslist

    def kinds_cb(self, kindlist):
        self.selected_kinds = kindlist

    def load_mode(self):
        if self.flist.selected_mode is None:
            self.print_msg('load: mode not selected')
            return
        if not self.selected_kinds:
            self.print_msg('load: no kinds selected')
            return
        if not self.selected_sys:
            self.print_msg('load: no systems selected')
            return
        self.mode_cli.load_mode(self.flist.selected_mode, self.selected_sys, self.selected_kinds)
        self.print_msg('loading...')

    def mode_loaded(self, dict_msg):
        self.print_msg("mode loaded:" + dict_msg['msg'], dict_msg['time'])

    def save(self, author, comment):
        self.print_msg("saving mode...")
        self.mode_cli.save_mode(author, comment)

    def mode_saved(self, dict_msg):
        self.flist.update_modenum()
        self.flist.update_modelist()
        self.print_msg("mode saved", dict_msg['time'])

    def update_db(self):
        self.flist.update_modenum()
        self.flist.update_modelist(update_marked=True)

    def print_msg(self, msg, srv_time=None):
        if srv_time is None:
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(srv_time/1e6))
        self.status_text.appendPlainText(msg_time + ": " + msg)
        self.status_text.ensureCursorVisible()


app = QtWidgets.QApplication(['saver'])

w = SaverWidget()
w.show()
w.flist.update_modelist()


app.exec_()

