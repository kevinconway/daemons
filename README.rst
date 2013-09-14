=======
Daemons
=======

**Well behaved unix daemons for every occasion.**

What Is Daemons?
===================

Daemons is a resource library for Python developers that want to create daemon
processes.

Simply import, extend, and start.

Show Me
=======

.. code-block:: python

    #!/usr/bin/python

    import sys
    import logging
    import time

    from daemons.base import Daemon

    logging.basicConfig(filename="daemon.log", level=logging.DEBUG)


    class SleepyDaemon(Daemon):

        def run(self):

            while True:

                time.sleep(1)


    if __name__ == '__main__':

        action = sys.argv[1]

        d = SleepyDaemon(pidfile='daemon.pid')

        if action == "start":

            d.start()

        elif action == "stop":

            d.stop()

        elif action == "restart":

            d.restart()

What else does it do?
=====================

The daemon classes in this package are simply meant to provide a base for
building custom daemons. None of them "do" anything on their own. All daemons
can have the "run()" method extended to provide custom functionality.

Built in to each daemon class is:

-   Pidfile management.

-   Signal trapping.

-   Logging output using Python's standard lib "logging" module.

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
