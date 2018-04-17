#!/usr/bin/env python



class ddm_middle(QObject):
    def __init__(self):
        super(QObject, self).__init__()

        self.pvlist = ["V5:S:IE:E:Delay1C",
                       "V5:S:IE:E:Delay2C",
                       "V5:S:IE:E:Delay3C",
                       "V5:S:IE:E:Delay4C",
                       "V5:S:IE:E:Delay11C",
                       "V5:S:IE:E:Delay12C",
                       "V5:S:IE:E:Delay13C",
                       "V5:S:IE:E:Delay14C",

                       "V5:S:IE:E:DelayMaskC.B0",
                       "V5:S:IE:E:DelayMaskC.B1",
                       "V5:S:IE:E:DelayMaskC.B2",
                       "V5:S:IE:E:DelayMaskC.B3",
                       "V5:S:IE:E:Delay1MaskC.B0",
                       "V5:S:IE:E:Delay1MaskC.B1",
                       "V5:S:IE:E:Delay1MaskC.B2",
                       "V5:S:IE:E:Delay1MaskC.B3",

                       "V5:S:IE:E:Voltage1C",
                       "V5:S:IE:E:Voltage2C"
                       ]

        self.channames = ["ic.injext.ekicker.gen_c1_dly",
                          "ic.injext.ekicker.gen_c2_dly",
                          "ic.injext.ekicker.gen_c3_dly",
                          "ic.injext.ekicker.gen_c4_dly",
                          "ic.injext.ekicker.form1p_dly",
                          "ic.injext.ekicker.form1n_dly",
                          "ic.injext.ekicker.form2p_dly",
                          "ic.injext.ekicker.form2n_dly",

                          "ic.injext.ekicker.gen_c1_mask",
                          "ic.injext.ekicker.gen_c2_mask",
                          "ic.injext.ekicker.gen_c3_mask",
                          "ic.injext.ekicker.gen_c4_mask",
                          "ic.injext.ekicker.form1p_mask",
                          "ic.injext.ekicker.form1n_mask",
                          "ic.injext.ekicker.form2p_mask",
                          "ic.injext.ekicker.form2n_mask",

                          "ic.injext.ekicker.u_akk1",
                          "ic.injext.ekicker.u_akk2"
                         ]
        self.mchans = []
        for x in self.pvlist:
            ind = self.pvlist.index(x)
            self.mchans.append(middleChanEpics(x, self.channames[ind]))



app = cothread.iqt()

mid = ddm_middle()


cothread.WaitForQuit()
