
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from linstarter import  LinStarter
from extractor import Extractor
import pycx4.qcda as cda
from acc_ctl.mode_ser import ModesClient

particles = ["e", "p"]
state_names = ["idle", "preinject", "inject", "injected", "preextract", "extract", "extracted"]
stateMsg = ["Stopped!", "Preparing for injection", "Injecting", "Injection finished",
            "Preparing for extraction", "Extracting", "Beam Extracted"]

run_modes = ["idle", "single-action", "single-cycle", "auto-cycle"]


class InjExtLoop(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.particles = "e"
        self.req_particles = None

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
            self.__preextract, self.__extract2, self.__extracted
        ]

        # output channels
        self.c_stateMsg = cda.StrChan('cxhw:0.ddm.stateMsg', on_update=True)

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

        # option-command channels
        self.c_particles = cda.StrChan('cxhw:0.ddm.particles', on_update=True)
        self.c_particles.valueMeasured.connect(self.particles_update)
        self.c_particles.setValue(self.particles)

        self.c_extr_train = cda.DChan('cxhw:0.ddm.extr_train')
        self.c_extr_train.valueMeasured.connect(self.train_proc)

        self.c_extr_train_interval = cda.DChan('cxhw:0.ddm.extr_train_interval')
        self.c_extr_train_interval.valueMeasured.connect(self.train_interval_update)

        # event channels
        self.c_injected = cda.DChan('cxhw:0.ddm.injected')
        self.c_extracted = cda.DChan('cxhw:0.ddm.extracted')



    def train_interval_update(self, chan):
        if chan.val > 0:
            self.extractor.set_training_interval(chan.val)
        else:
            chan.setValue(self.extractor.training_interval)

    def train_proc(self, chan):
        print("extr_train: ", chan.val)
        if chan.val and self.ic_runmode == 'idle':
            self.extractor.start_training()


    def particles_update(self, chan):
        if self.particles == chan.val or chan.val not in {'e', 'p'}:
            return
        if self.ic_runmode == 'idle':
            self.particles = chan.val
            self.linStarter.set_particles(self.particles)
            print("particles set: ", self.particles)
        else:
            self.req_particles = chan.val
            print("particles requested: ", self.req_particles)

    def cmd_proc(self, chan):
        if chan.first_cycle:
            return
        sn = chan.short_name()
        print(sn)
        if sn == "stop":
            self.stop()
            return
        if sn == "linrun":
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


    def run_state(self):
        print('run_state_call, state: ', self.state)
        if self.ic_runmode == 'idle':
            return
        s_ind = state_names.index(self.state)
        self.c_stateMsg.setValue(stateMsg[s_ind])
        self.states[s_ind]()

    def next_state(self):
        print('next_state_call')
        s_ind = state_names.index(self.state)
        ns_ind = s_ind + 1

        if ns_ind < len(state_names):
            self.state = state_names[ns_ind]
            self.run_state()

    def __idle(self):
        print('idle state')
        pass

    def __preinject(self):
        print("__preinject")
        if self.req_particles is not None:
            self.particles = self.req_particles
            self.req_particles = None
            print("particles updated to: ", self.particles)

        mode = self.modes[self.particles][0]  # 0 - injection
        self.modeCtl.load_marked(mode, self.mode_subsys, ['rw'])

    def __inject2(self):
        print("__inject2")
        self.linStarter.start()

    def __injected(self):
        self.c_injected.setValue(1)
        if self.ic_runmode in {"single-cycle", "auto-cycle"}:
            #self.next_state()
            self.timer.singleShot(50, self.next_state)

    def __preextract(self):
        mode = self.modes[self.particles][1]  # 1 - extraction modes
        self.modeCtl.load_marked(mode, self.mode_subsys, ['rw'])

    def __extract2(self):
        self.extractor.extract()

    def __extracted(self):
        self.c_extracted.setValue(1)
        if self.ic_runmode == "auto-cycle":
            self.state = "preinject"
            self.run_state()


    def setParticles(self, particles):
        self.particles = particles

    # stop any operation
    def stop(self):
        print('stop')
        self.ic_runmode = 'idle'
        self.state = 'idle'
        self.linStarter.stop()
        self.extractor.stop()

    def inject(self):
        print('inject')
        self.ic_runmode = "single-action"
        self.state = "preinject"
        self.run_state()

    def extract(self):
        print('extract')
        # check if something injected
        self.ic_runmode = "single-action"
        self.state = "preextract"
        self.run_state()

    def exec_round(self):
        print('execRound')
        self.ic_runmode = "single-cycle"
        self.state = "preinject"
        self.run_state()

    def exec_burst(self):
        print('execBurst')
        self.ic_runmode = "auto-cycle"
        self.state = "preinject"
        self.run_state()
