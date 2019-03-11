
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from linstarter import  LinStarter
from extractor import Extractor
from pu_switcher import PUSwitcher
from acc_ctl.linbeamctl import LinBeamCtl

import pycx4.qcda as cda
from acc_ctl.mode_ser import ModesClient


particles = ["e", "p"]
state_names = ["idle",
               "preinject", "inject", "injected",
               "preextract", "extract", "extracted",
               "pu_switching", "pu_switched"]
stateMsg = ["Stopped!", "Preparing for injection", "Injecting", "Injection finished",
            "Preparing for extraction", "Extracting", "Beam Extracted",
            "particle-users switching", "particle-users switched"]

run_modes = ["idle", "single-action", "single-cycle", "auto-cycle"]


class InjExtLoop(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.particles = "e"
        self.req_particles = None

        self.pu_mode = None
        self.req_pu_mode = None
        self.req_kickers_mode = False
        self.state = 'idle'
        self.ic_runmode = 'idle'

        self.linStarter = LinStarter()
        self.extractor = Extractor()
        self.modeCtl = ModesClient()
        self.pu_ctl = PUSwitcher()

        self.mode_subsys = [37, 38, 39]
        self.modes = {
            'e': [1, 2],
            'p': [3, 4]
        }

        self.modeCtl.markedReady.connect(self.kickers_loaded)
        self.linStarter.runDone.connect(self.next_state)
        self.extractor.extractionDone.connect(self.next_state)
        self.pu_ctl.switching_done.connect(self.next_state)

        self.timer = QTimer()

        self.states = [
            self.__idle,
            self.__preinject, self.__inject2, self.__injected,
            self.__preextract, self.__extract2, self.__extracted,
            self.__pu_switching, self.__pu_switched
        ]

        # output channels
        self.c_state = cda.StrChan('cxhw:0.ddm.state', on_update=True, max_nelems=20)
        self.c_stateMsg = cda.StrChan('cxhw:0.ddm.stateMsg', on_update=True, max_nelems=20)

        self.c_icrunmode = cda.StrChan('cxhw:0.ddm.ICRunMode', on_update=True, max_nelems=20)

        # command channels
        self.cmds = ['stop', 'inject', 'extract', 'nround', 'autorun', 'e2v4', 'p2v4', 'e2v2', 'p2v2']
        self.c_cmds = [cda.IChan('cxhw:0.ddm.' + x, on_update=True) for x in self.cmds]
        for c in self.c_cmds:
            c.valueMeasured.connect(self.cmd_proc)

        # option-command channels
        self.c_particles = cda.StrChan('cxhw:0.ddm.particles', on_update=True, max_nelems=20)
        self.c_particles.valueMeasured.connect(self.particles_update)
        self.c_particles.setValue(self.particles)

        self.c_extr_train = cda.IChan('cxhw:0.ddm.extr_train',  on_update=True)
        self.c_extr_train.valueMeasured.connect(self.train_proc)

        self.c_extr_train_interval = cda.DChan('cxhw:0.ddm.extr_train_interval', on_update=True)
        self.c_extr_train_interval.valueMeasured.connect(self.train_interval_update)

        # event channels
        self.c_injected = cda.IChan('cxhw:0.ddm.injected', on_update=True)
        self.c_extracted = cda.IChan('cxhw:0.ddm.extracted', on_update=True)

        # beam current channels
        self.c_beamcur = cda.DChan('cxhw:0.dcct.beamcurrent', on_update=True)
        self.c_extr_beamCur = cda.DChan('cxhw:0.dcct.ExtractionCurrent', on_update=True)

        self.c_v2k_auto = cda.IChan('cxhw:0.ddm.v2k_auto', on_update=True)
        self.c_v2k_particles = cda.StrChan('cxhw:0.bep.particles', on_update=True, max_nelems=20)
        self.c_v2k_particles.valueMeasured.connect(self.v2k_auto_mode)
        self.c_v2k_offline = cda.IChan('cxhw:0.bep.offline', on_update=True)
        self.c_v2k_offline.valueMeasured.connect(self.v2k_offline_proc)

        self.linbeam_cor = LinBeamCtl()


    def v2k_offline_proc(self, chan):
        if self.c_v2k_auto.val == 0 or self.pu_mode not in {'e2v2', 'p2v2'}:
            return
        if self.c_v2k_offline.val == 1:
            self.linbeam_cor.close_beam()
        elif self.c_v2k_offline.val == 0:
            self.linbeam_cor.open_beam()

    def v2k_auto_mode(self, chan):
        print('v2k mode chanded to: ', chan.val)
        print('current mode: ', self.pu_mode)
        if self.c_v2k_auto.val == 0 or self.req_pu_mode is not None:
            return
        if chan.val == 'positrons' and self.pu_mode == 'e2v2':
            self.p2v2()
        if chan.val == 'electrons' and self.pu_mode == 'p2v2':
            self.e2v2()

    def train_interval_update(self, chan):
        if chan.val > 0:
            self.extractor.set_training_interval(chan.val)
        else:
            chan.setValue(self.extractor.training_interval)

    def train_proc(self, chan):
        if chan.val and self.ic_runmode == 'idle':
            self.extractor.start_training()

    def particles_update(self, chan):
        if self.req_pu_mode is not None:
            return
        if self.particles == chan.val or chan.val not in {'e', 'p'}:
            return
        if self.ic_runmode == 'idle':
            self.set_particles(chan.val)
        else:
            self.req_particles = chan.val

    def set_particles(self, p):
        #print('set particles call')
        if self.particles == p:
            return
        self.particles = p
        self.linStarter.set_particles(self.particles)
        if self.c_particles.val != p:
            self.c_particles.setValue(p)

    def set_pu_mode(self, mode):
        if self.pu_mode == mode:
            return
        self.req_pu_mode = mode
        #print('requested mode: ', mode)
        if self.ic_runmode == 'idle':
            #print('going to switching state')
            self.run_state('pu_switching')

    def kickers_loaded(self):
        if self.req_kickers_mode:
            self.timer.singleShot(80, self.next_state)
            self.req_kickers_mode = False


    def run_state(self, state=None):
        if state is not None:
            self.state = state
        self.c_state.setValue(self.state)
        if self.ic_runmode == 'idle':
            return
        s_ind = state_names.index(self.state)
        self.c_stateMsg.setValue(stateMsg[s_ind])
        self.states[s_ind]()

    def next_state(self):
        s_ind = state_names.index(self.state)
        ns_ind = s_ind + 1
        if ns_ind < len(state_names):
            self.state = state_names[ns_ind]
            self.run_state()

    def __idle(self):
        pass

    def __preinject(self):
        if self.req_particles is not None:
            self.set_particles(self.req_particles)
            self.req_particles = None
        if self.req_pu_mode is not None:
            self.run_state('pu_switching')
            return

        self.req_kickers_mode = True
        inj_mode = self.modes[self.particles][0]
        self.modeCtl.load_marked(inj_mode, self.mode_subsys, ['rw'])

    def __inject2(self):
        self.linStarter.start()

    def __injected(self):
        self.c_injected.setValue(1)
        if self.ic_runmode in {"single-cycle", "auto-cycle"}:
            self.next_state()

    def __preextract(self):
        self.req_kickers_mode = True
        ext_mode = self.modes[self.particles][1]  # 1 - extraction modes
        self.modeCtl.load_marked(ext_mode, self.mode_subsys, ['rw'])

    def __extract2(self):
        self.c_extr_beamCur.setValue(self.c_beamcur.val)
        self.extractor.extract()

    def __extracted(self):
        self.c_extracted.setValue(1)
        if self.ic_runmode == "auto-cycle":
            self.state = "preinject"
            self.run_state()

    def __pu_switching(self):
        print("switching")
        if self.req_pu_mode is None:
            print('mode not requested')
            return
        self.set_particles(self.req_pu_mode[0])
        self.pu_ctl.switch_mode(self.req_pu_mode)

    def __pu_switched(self):
        print('mode switching complete')
        self.pu_mode = self.req_pu_mode
        self.req_pu_mode = None
        if self.ic_runmode == "auto-cycle":
            self.run_state("preinject")
        else:
            self.run_state('idle')

    def cmd_proc(self, chan):
        if chan.first_cycle:
            return
        sn = chan.short_name()
        getattr(self, sn)()

    def set_runmode(self, runmode):
        self.ic_runmode = runmode
        self.c_icrunmode.setValue(runmode)

    def stop(self):
        self.linStarter.stop()
        self.extractor.stop()
        self.set_runmode('idle')
        self.run_state('idle')

    def inject(self):
        self.set_runmode("single-action")
        self.run_state('preinject')

    def extract(self):
        # check if something injected
        self.set_runmode("single-action")
        self.run_state('preextract')

    def nround(self):
        self.set_runmode("single-cycle")
        self.run_state('preinject')

    def autorun(self):
        self.set_runmode("auto-cycle")
        self.run_state('preinject')

    def e2v4(self):
        self.set_pu_mode('e2v4')

    def p2v4(self):
        self.set_pu_mode('p2v4')

    def e2v2(self):
        self.set_pu_mode('e2v2')

    def p2v2(self):
        self.set_pu_mode('p2v2')

