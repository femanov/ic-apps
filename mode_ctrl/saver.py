#!/usr/bin/env python3
import time
from aux.Qt import QtWidgets
from cxwidgets.auxwidgets import BaseGridW
from acc_db.mode_list import ModeListCtrl
from acc_db.sys_tree import SysTree
from acc_db.chan_kinds import KindTable
from acc_ctl.mode_ser import ModesClient
from acc_db.db import ModesDB


class SaverWidget(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.modes_db = ModesDB()

        self.flist = ModeListCtrl()
        self.flist.setFixedSize(850, 800)
        self.grid.addWidget(self.flist, 0, 0, 2, 1)

        self.stree = SysTree()
        self.grid.addWidget(self.stree, 0, 1)
        self.stree.selectionChanged.connect(self.sys_cb)

        self.kindt = KindTable()
        self.kindt.setFixedSize(280, 160)
        self.grid.addWidget(self.kindt, 1, 1)
        self.kindt.selectionChanged.connect(self.kinds_cb)

        self.status_text = QtWidgets.QPlainTextEdit()
        self.status_text.setFixedHeight(40)
        self.status_text.setReadOnly(True)
        self.status_text.setCenterOnScroll(True)
        self.grid.addWidget(self.status_text, 2, 0, 1, 2)

        self.selected_kinds = self.kindt.selected()
        self.selected_sys = []

        self.mode_cli = ModesClient()
        self.mode_cli.modeSaved.connect(self.mode_saved)
        self.mode_cli.modeLoaded.connect(self.mode_loaded)
        self.mode_cli.update.connect(self.update_db)

        self.flist.markMode.connect(self.mode_cli.mark_mode)
        self.flist.archiveMode.connect(self.archive_mode)
        self.flist.loadMode.connect(self.load_mode)
        self.flist.saveMode.connect(self.save)
        self.flist.setZeros.connect(self.set_zeros)
        self.flist.outMsg.connect(self.print_msg)

        self.flist.listw.modeUpdated.connect(self.mode_cli.ask_update)

    def sys_cb(self, syslist):
        self.selected_sys = syslist

    def kinds_cb(self, kindlist):
        self.selected_kinds = kindlist

    def archive_mode(self, mode_id):
        self.modes_db.archive_mode(mode_id)
        self.mode_cli.ask_update()

    def load_mode(self, mode_id):
        if not self.selected_kinds:
            self.print_msg('load: no kinds selected')
            return
        if not self.selected_sys:
            self.print_msg('load: no systems selected')
            return
        self.mode_cli.load_mode(mode_id, self.selected_sys, self.selected_kinds)
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

    def set_zeros(self):
        self.mode_cli.set_zeros(self.selected_sys, self.selected_kinds)

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
w.setFixedSize(w.size())
w.flist.update_modelist()

app.exec_()

