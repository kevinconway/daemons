#!/usr/bin/env python

"""Sample daemon which wraps a normal function."""

import logging
import os
import signal
import sys
import time

from daemons import daemonizer


LOG = logging.getLogger(__name__)


def log_goodbye():
    """Log a goodbye message when the daemon stops."""
    LOG.debug("Process shutting down...")


@daemonizer.run(
    pidfile=os.path.join(os.getcwd(), "daemon.pid"),
    signals={signal.SIGTERM: (log_goodbye,)},
)
def main(idle):
    """Any normal python logic which runs a loop. Can take arguments."""
    while True:

        LOG.debug("Sleeping for {0} seconds.".format(idle))
        time.sleep(idle)


if __name__ == "__main__":

    action = sys.argv[1]

    logging.basicConfig(filename="daemon.log", level=logging.DEBUG)

    if action == "start":

        main(20)

    elif action == "stop":

        main.stop()

    elif action == "restart":

        main.stop()
        main(20)
