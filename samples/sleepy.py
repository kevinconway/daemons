#!/usr/bin/env python

"""Sample daemon which just sleeps."""

import logging
import os
import sys
import time

from daemons.prefab import run


class SleepyDaemon(run.RunDaemon):

    """A daemon which uses time.sleep as the action."""

    def run(self):
        """Main functionality loop goes here."""
        while True:

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
