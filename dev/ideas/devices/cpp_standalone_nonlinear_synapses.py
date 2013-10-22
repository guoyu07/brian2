standalone_mode = True
plot_results = True

from brian2 import *
import time
import shutil

start = time.time()

if standalone_mode:
    from brian2.devices.cpp_standalone import *
    set_device('cpp_standalone')
else:
    brian_prefs['codegen.target'] = 'weave'
    #brian_prefs['codegen.target'] = 'numpy'

a=1/(10*ms)
b=1/(10*ms)
c=1/(10*ms)

input=NeuronGroup(2, 'dv/dt=1/(10*ms):1', threshold='v>1', reset='v=0')
neurons = NeuronGroup(1, """dv/dt=(g-v)/(10*ms) : 1
                            g : 1""")
S=Synapses(input,neurons,
           '''# This variable could also be called g_syn to avoid confusion
              dg/dt=-a*g+b*x*(1-g) : 1
              g_post = g : 1 (summed)
              dx/dt=-c*x : 1
              w : 1 # synaptic weight
           ''', pre='x+=w') # NMDA synapses

S.connect(True)
S.w = '1+9*i'
input.v = '0.5*i'

#M = StateMonitor(S, 'g', record=True)
#Mn = StateMonitor(neurons, 'g', record=0)

net = Network(input, neurons, S,
              #M, Mn,
              )

net.run(1000*ms)

if standalone_mode:
    shutil.rmtree('output')
    build(project_dir='output', compile_project=True, run_project=True)

if not standalone_mode and plot_results:
    import matplotlib.pyplot as plt
    plt.subplot(2, 1, 1)
    plt.plot(M.t / ms, M.g.T)
    plt.subplot(2, 1, 2)
    plt.plot(Mn.t / ms, Mn[0].g)
    plt.show()
    