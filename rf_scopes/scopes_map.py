# RF measurement scopes signals map and settings

srv = 'cxhw:15'

cmap = {
    'adc250_8a': {'line0': 'kls1_hv', 'line1': 'kls2_hv', 'line2': 'kls3_hv', 'line3': 'kls4_hv'},
    'adc250_8c': {'line0': 'kls1_in', 'line1': 'kls2_in', 'line2': 'kls3_in', 'line3': 'kls4_in'},
    'adc250_8e': {'line0': 's1_in', 'line1': 's1_out', 'line2': 's2_in', 'line3': 's2_out'},
    'adc250_90': {'line0': 's3_in', 'line1': 's3_out', 'line2': 's4_in', 'line3': 's4_out'},
    'adc250_92': {'line0': 's5_in', 'line1': 's5_out', 'line2': 's6_in', 'line3': 's6_out'},
    'adc250_94': {'line0': 's7_in', 'line1': 's7_out', 'line2': 's8_in', 'line3': 's8_out'},
    'adc250_96': {'line0': 's9_in', 'line1': 's9_out', 'line2': 's10_in', 'line3': 's10_out'},
    'adc250_98': {'line0': 's11_in', 'line1': 's11_out', 'line2': 's12_in', 'line3': 's12_out'},
    'adc250_9a': {'line0': 's13_in', 'line1': 's13_out', 'line2': 's14_in', 'line3': 's14_out'},
    'adc250_9c': {'line0': 'grp_in', 'line1': '', 'line2': 'gun_hv', 'line3': 'beam'},
}

ltimer_scopes = ('adc250_8a', 'adc250_8c', 'adc250_8e', 'adc250_90', 'adc250_92', 'adc250_94',
                 'adc250_96', 'adc250_98', 'adc250_9a')

p_sign = {'s4_in', 's6_in', 's8_in', 's10_out'}

c_sign = set()
for ks in cmap:
    for kd in cmap[ks]:
        if cmap[ks][kd].startswith('s') and cmap[ks][kd] not in p_sign:
            c_sign.add(cmap[ks][kd])
c_sign.add('gun_hv')
