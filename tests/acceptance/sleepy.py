#!/usr/bin/python

"""This module acts as the daemon interface for the test suite."""

import logging
LOG = logging.getLogger(__name__)

import os
import sys
import time

# Rig up some special pathing for tests.
test_directory = os.path.dirname(os.path.realpath(__file__))
package_directory = os.path.join(test_directory, '..', '..')
sys.path.append(package_directory)

import logging

from daemons.base import Daemon


class SleepyDaemon(Daemon):

    def _step(self):

        time.sleep(.1)

if __name__ == '__main__':

    pidfile = sys.argv[1]
    logfile = sys.argv[2]
    action = sys.argv[3]

    # Set up logging to write to log file.
    logging.basicConfig(filename=logfile,
                        level=logging.DEBUG)

    d = SleepyDaemon(pidfile)

    if action == "start":

        d.start()

    elif action == "stop":

        d.stop()

    elif action == "restart":

        d.restart()
