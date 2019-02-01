#!/usr/bin/env python3

from settings.db import acc_cfg
from acc_db.db import AccConfig
import pycx4.qcda as cda

preset_ids = {
    'p0': 72,
    'p1': 73,
    'p2': 74,
    'p3': 75
}


def preset_chans(preset_id):
    db = AccConfig(**acc_cfg)
    db.execute("select chan_name from sys_chans(%s)", (preset_id,))
    return [x[0] for x in db.cur.fetchall()]


preset_base = preset_chans(preset_ids['p0'])

presets = {k: [x.replace('.p0.', '.' + k + '.') for x in preset_base] for k in preset_ids if not k == 'p0'}
presets['p0'] = preset_base
presets['hw'] = [x.replace('.p0.', '.') for x in preset_base]

#print(presets)


class KickersPresetMgr:
    def __init__(self):
        self.presets = presets
        self.chans = {k: [cda.IChan(x) for x in self.presets[k]] for k in self.presets}
        self.c_activate = cda.IChan('ic.ie.activate_preset_n')

    def activate(self, n_preset):
        self.c_activate.setValue(n_preset)

    def copy(self, **kwargs):
        src = kwargs.get('src', 'hw')
        dst = kwargs.get('dst', None)
        if dst is None:
            return
        for ind in range(len(self.chans[src])):
            self.chans[dst][ind].setValue(self.chans[src][ind].val)

