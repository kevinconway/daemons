=======
Daemons
=======

**Well behaved unix daemons for every occasion.**

What Is Daemons?
================

`Daemons` is a resource library for Python developers that want to create
daemon processes. The classes in this library provide the basic daemonization,
signal handling, and pid management functionality while allowing for any
implementation of behaviour and logic.

Show Me
=======

.. code-block:: python

    #!/usr/bin/python

    import sys
    import logging
    import time

    from daemons.prefab import run


    class SleepyDaemon(run.RunDaemon):

        def run(self):

            while True:

                time.sleep(1)


    if __name__ == '__main__':

        action = sys.argv[1]

        logging.basicConfig(filename="daemon.log", level=logging.DEBUG)
        d = SleepyDaemon(pidfile='daemon.pid')

        if action == "start":

            d.start()

        elif action == "stop":

            d.stop()

        elif action == "restart":

            d.restart()

What Is Included?
=================

The daemons in the 'prefab' module come bundled with the following features:

-   pidfile management
-   signal handling
-   start/stop/restart functionality
-   unix process daemonization

The default implementation of these feature are all driven by Python standard
library modules. Each component may be overridden or extended by adding another
base class to your daemon that implements the component interface. Check the
'interfaces' package for items to implement.

The 'prefab' daemons come in three flavors. The 'RunDaemon' requires that you
implement the 'run' method which should use some form of a loop. If the 'run'
method completes the process will stop. The 'StepDaemon' requires that you
implement the 'step' method. The process will call 'step' on an infinite loop.
The eventlet and gevent message daemons require that you implement the
'get_message' and 'handle_message' methods. These will fetch and handle
messages within green-threads.

License
=======

::

    Copyright 2013 Kevin Conway

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


Contributing
============

All contributions to this project are protected under the agreement found in
the `CONTRIBUTING` file. All contributors should read the agreement but, as
a summary::

    You give us the rights to maintain and distribute your code and we promise
    to maintain an open source distribution of anything you contribute.
