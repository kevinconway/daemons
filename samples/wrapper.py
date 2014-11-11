#!/usr/bin/env python

"""Sample daemon which wraps a normal function."""

import logging
import os
import sys
import time

from daemons import daemonizer


LOG = logging.getLogger(__name__)


@daemonizer.run(pidfile=os.path.join(os.getcwd(), "daemon.pid"))
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
