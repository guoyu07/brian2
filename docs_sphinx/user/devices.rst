Devices
=======

Brian supports generating standalone code for multiple devices. In this mode, running a Brian script generates
source code in a project tree for the target device/language. This code can then be compiled and run on the device,
and modified if needed. At the moment, the only 'device' supported is standalone C++ code.
In some cases, the speed gains can be impressive, in particular for smaller networks with complicated spike
propagation rules (such as STDP).

.. _cpp_standalone:

C++ standalone
--------------

To use the C++ standalone mode, you only have to make very small changes to your script. The exact change depends on
whether your script has only a single `run` (or `Network.run`) call, or several of them:

Single run call
~~~~~~~~~~~~~~~
At the beginning of the script, i.e. after the import statements, add::

    set_device('cpp_standalone')

The `CPPStandaloneDevice.build` function will be automatically called with default arguments right after the `run`
call. If you need non-standard arguments then you can specify them as part of the `set_device` call::

    set_device('cpp_standalone', directory='my_directory', debug=True)

Multiple run call
~~~~~~~~~~~~~~~~~
At the beginning of the script, i.e. after the import statements, add::

    set_device('cpp_standalone', build_on_run=False)

After the last `run` call, call `device.build` explicitly::

    device.build(directory='output', compile=True, run=True, debug=False)

The `~CPPStandaloneDevice.build` function has several arguments to specify the output directory, whether or not to
compile and run the project after creating it (using ``gcc``) and whether or not to compile it with debugging support
or not.

Limitations
~~~~~~~~~~~
Not all features of Brian will work with C++ standalone, in particular Python based network operations and
some array based syntax such as ``S.w[0, :] = ...`` will not work. If possible, rewrite these using string
based syntax and they should work. Also note that since the Python code actually runs as normal, code that does
something like this may not behave as you would like::

    results = []
    for val in vals:
        # set up a network
        run()
        results.append(result)

The current C++ standalone code generation only works for a fixed number of `~Network.run` statements, not with loops.
If you need to do loops or other features not supported automatically, you can do so by inspecting the generated
C++ source code and modifying it, or by inserting code directly into the main loop as follows::

    device.insert_code('main', '''
    cout << "Testing direct insertion of code." << endl;
    ''')

Variables
~~~~~~~~~
After a simulation has been run (after the `run` call if `set_device` has been called with ``build_on_run`` set to
``True`` or after the `Device.build` call with ``run`` set to ``True``), state variables and
monitored variables can be accessed using standard syntax, with a few exceptions (e.g. string expressions for indexing).

.. _openmp:

Multi-threading with OpenMP
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
    OpenMP code has not yet been well tested and so may be inaccurate.

When using the C++ standalone mode, you have the opportunity to turn on multi-threading, if your C++ compiler is compatible with
OpenMP. By default, this option is turned off and only one thread is used. However, by changing the preferences of the codegen.cpp_standalone
object, you can turn it on. To do so, just add the following line in your python script::

    prefs.devices.cpp_standalone.openmp_threads = XX

XX should be a positive value representing the number of threads that will be
used during the simulation. Note that the speedup will strongly depend on the
network, so there is no guarantee that the speedup will be linear as a function
of the number of threads. However, this is working fine for networks with not
too small timestep (dt > 0.1ms), and results do not depend on the number of
threads used in the simulation.
