
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from linstarter import  LinStarter
from extractor import Extractor
import pycx4.qcda as cda
from acc_ctl.mode_ser import ModesClient


particles = ["e", "p"]
state_names = ["idle",
               "preinject", "inject", "injected",
               "preextract", "extract", "extracted",
               "pu_switching"]
stateMsg = ["Stopped!", "Preparing for injection", "Injecting", "Injection finished",
            "Preparing for extraction", "Extracting", "Beam Extracted"]

run_modes = ["idle", "single-action", "single-cycle", "auto-cycle"]


class InjExtLoop(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.particles = "e"
        self.req_particles = None

        self.pu_mode = None
        self.req_pu_mode = None

        self.state = 'idle'
        self.ic_runmode = 'idle'

        self.linStarter = LinStarter()
        self.extractor = Extractor()
        self.modeCtl = ModesClient()

        self.mode_subsys = [37, 38, 39]
        self.modes = {
            'e': [1, 2],
            'p': [3, 4]
        }

        self.modeCtl.markedReady.connect(self.next_state)
        self.linStarter.runDone.connect(self.next_state)
        self.extractor.extractionDone.connect(self.next_state)
        self.timer = QTimer()


        self.states = [
            self.__idle,
            self.__preinject, self.__inject2, self.__injected,
            self.__preextract, self.__extract2, self.__extracted,
            self.__pu_switching
        ]

        # output channels
        self.c_state = cda.StrChan('cxhw:0.ddm.state', on_update=True)
        self.c_stateMsg = cda.StrChan('cxhw:0.ddm.stateMsg', on_update=True)

        self.c_icrunmode = cda.StrChan('cxhw:0.ddm.ICRunMode', on_update=True)

        # command channels
        self.c_stop = cda.DChan('cxhw:0.ddm.stop', on_update=True)
        self.c_inject = cda.DChan('cxhw:0.ddm.inject', on_update=True)
        self.c_extract = cda.DChan('cxhw:0.ddm.extract', on_update=True)
        self.c_nround = cda.DChan('cxhw:0.ddm.nround', on_update=True)
        self.c_autorun = cda.DChan('cxhw:0.ddm.autorun', on_update=True)
        self.c_stop.valueMeasured.connect(self.cmd_proc)
        self.c_inject.valueMeasured.connect(self.cmd_proc)
        self.c_extract.valueMeasured.connect(self.cmd_proc)
        self.c_nround.valueMeasured.connect(self.cmd_proc)
        self.c_autorun.valueMeasured.connect(self.cmd_proc)

        self.c_e2v4 = cda.DChan('cxhw:0.ddm.e2v4', on_update=True)
        self.c_p2v4 = cda.DChan('cxhw:0.ddm.p2v4', on_update=True)
        self.c_e2v2 = cda.DChan('cxhw:0.ddm.e2v2', on_update=True)
        self.c_p2v2 = cda.DChan('cxhw:0.ddm.p2v2', on_update=True)
        self.c_e2v4.valueMeasured.connect(self.cmd_proc)
        self.c_p2v4.valueMeasured.connect(self.cmd_proc)
        self.c_e2v2.valueMeasured.connect(self.cmd_proc)
        self.c_p2v2.valueMeasured.connect(self.cmd_proc)

        # option-command channels
        self.c_particles = cda.StrChan('cxhw:0.ddm.particles', on_update=True)
        self.c_particles.valueMeasured.connect(self.particles_update)
        self.c_particles.setValue(self.particles)

        self.c_extr_train = cda.DChan('cxhw:0.ddm.extr_train',  on_update=True)
        self.c_extr_train.valueMeasured.connect(self.train_proc)

        self.c_extr_train_interval = cda.DChan('cxhw:0.ddm.extr_train_interval', on_update=True)
        self.c_extr_train_interval.valueMeasured.connect(self.train_interval_update)

        # event channels
        self.c_injected = cda.DChan('cxhw:0.ddm.injected', on_update=True)
        self.c_extracted = cda.DChan('cxhw:0.ddm.extracted', on_update=True)

    def train_interval_update(self, chan):
        if chan.val > 0:
            self.extractor.set_training_interval(chan.val)
        else:
            chan.setValue(self.extractor.training_interval)

    def train_proc(self, chan):
        if chan.val and self.ic_runmode == 'idle':
            self.extractor.start_training()

    def particles_update(self, chan):
        if self.particles == chan.val or chan.val not in {'e', 'p'}:
            return
        if self.ic_runmode == 'idle':
            self.set_particles(chan.val)
        else:
            self.req_particles = chan.val

    def set_particles(self, p):
        self.particles = p
        self.linStarter.set_particles(self.particles)

    def set_pu_mode(self, mode):
        if self.pu_mode == mode:
            return
        if self.ic_runmode == 'idle':
            self.req_pu_mode = mode
            self.run_state('pu_switching')
        else:
            self.req_pu_mode = mode

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
            print("particles updated to: ", self.particles)

        inj_mode = self.modes[self.particles][0]  # 0 - injection
        self.modeCtl.load_marked(inj_mode, self.mode_subsys, ['rw'])

    def __inject2(self):
        self.linStarter.start()

    def __injected(self):
        self.c_injected.setValue(1)
        if self.ic_runmode in {"single-cycle", "auto-cycle"}:
            self.timer.singleShot(50, self.next_state)

    def __preextract(self):
        ext_mode = self.modes[self.particles][1]  # 1 - extraction modes
        self.modeCtl.load_marked(ext_mode, self.mode_subsys, ['rw'])

    def __extract2(self):
        self.extractor.extract()

    def __extracted(self):
        self.c_extracted.setValue(1)
        if self.ic_runmode == "auto-cycle":
            self.state = "preinject"
            self.timer.singleShot(50, self.run_state)

    def __pu_switching(self):
        pass

    # commands
    def cmd_proc(self, chan):
        if chan.first_cycle:
            return
        sn = chan.short_name()
        if sn == "stop":
            self.stop()
            return
        if sn == "inject":
            self.inject()
            return
        if sn == "extract":
            self.extract()
            return
        if sn == "nround":
            self.exec_round()
            return
        if sn == "autorun":
            self.exec_burst()
            return
        if sn == "e2v4":
            self.e2v4()
            return
        if sn == "p2v4":
            self.p2v4()
            return
        if sn == "e2v2":
            self.e2v2()
            return
        if sn == "p2v2":
            self.p2v2()
            return

    # stop any operation
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

    def exec_round(self):
        self.set_runmode("single-cycle")
        self.run_state('preinject')

    def exec_burst(self):
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

