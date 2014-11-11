#!/usr/bin/env python

"""Sample daemon which just sleeps."""

import logging
import os
import sys
import time

from daemons.prefab import step


class SleepyDaemon(step.StepDaemon):

    """A daemon which uses time.sleep as the action."""

    def step(self):
        """Main functionality here. Called in a loop."""
        time.sleep(1)


if __name__ == "__main__":

    action = sys.argv[1]

    logging.basicConfig(filename="daemon.log", level=logging.DEBUG)
    pidfile = os.path.join(os.getcwd(), "daemon.pid")
    d = SleepyDaemon(pidfile=pidfile)

    if action == "start":

        d.start()

    elif action == "stop":

        d.stop()

    elif action == "restart":

        d.restart()
