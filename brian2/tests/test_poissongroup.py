from numpy.testing.utils import assert_equal
from nose import with_setup
from nose.plugins.attrib import attr

from brian2 import *
from brian2.devices.device import reinit_devices


@attr('standalone-compatible')
@with_setup(teardown=reinit_devices)
def test_single_rates():
    # Specifying single rates
    P0 = PoissonGroup(10, 0*Hz)
    Pfull = PoissonGroup(10, 1. / defaultclock.dt)

    # Basic properties
    assert len(P0) == len(Pfull) == 10
    assert len(repr(P0)) and len(str(P0))
    spikes_P0 = SpikeMonitor(P0)
    spikes_Pfull = SpikeMonitor(Pfull)
    run(2*defaultclock.dt)
    assert_equal(spikes_P0.count, np.zeros(len(P0)))
    assert_equal(spikes_Pfull.count, 2 * np.ones(len(P0)))

@attr('standalone-compatible')
@with_setup(teardown=reinit_devices)
def test_rate_arrays():
    P = PoissonGroup(2, np.array([0, 1./defaultclock.dt])*Hz)
    spikes = SpikeMonitor(P)
    run(2*defaultclock.dt)

    assert_equal(spikes.count, np.array([0, 2]))

@attr('standalone-compatible')
@with_setup(teardown=reinit_devices)
def test_propagation():
    # Using a PoissonGroup as a source for Synapses should work as expected
    P = PoissonGroup(2, np.array([0, 1./defaultclock.dt])*Hz)
    G = NeuronGroup(2, 'v:1')
    S = Synapses(P, G, pre='v+=1', connect='i==j')
    run(2*defaultclock.dt)

    assert_equal(G.v[:], np.array([0., 2.]))


@attr('standalone-compatible')
@with_setup(teardown=reinit_devices)
def test_poissongroup_subgroup():
    # It should be possible to take a subgroup of a PoissonGroup
    P = PoissonGroup(4, [0, 0, 0, 0]*Hz)
    P1 = P[:2]
    P2 = P[2:]
    P2.rates = 1./defaultclock.dt
    G = NeuronGroup(4, 'v:1')
    S1 = Synapses(P1, G[:2], pre='v+=1', connect='i==j')
    S2 = Synapses(P2, G[2:], pre='v+=1', connect='i==j')
    run(2*defaultclock.dt)

    assert_equal(G.v[:], np.array([0., 0., 2., 2.]))

if __name__ == '__main__':
    test_single_rates()
    test_rate_arrays()
    test_propagation()
    test_poissongroup_subgroup()
