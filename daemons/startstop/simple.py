"""Simple implementation of daemon start/stop/restart management."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import logging
import signal
import sys
import time

from ..interfaces import exit
from ..interfaces import startstop


LOG = logging.getLogger(__name__)


class SimpleStartStopManager(startstop.StartStopManager):

    """Relies on other interfaces to provide functionality."""

    def start(self):
        """Start the process with daemonization.

        If the process is already started this call should exit with code
        ALREADY_RUNNING. Otherwise it must call the 'daemonize' method and then
        call 'run'.
        """
        if self.pid is not None:

            LOG.error(
                "The process is already running with pid {0}.".format(self.pid)
            )
            sys.exit(exit.ALREADY_RUNNING)

        self.daemonize()

        LOG.info("Beginning run loop for process.")
        try:

            self.run()

        except Exception:

            LOG.exception("Uncaught exception in the daemon run() method.")
            self.stop()
            sys.exit(exit.RUN_FAILURE)

    def stop(self):
        """Stop the daemonized process.

        If the process is already stopped this call should exit successfully.
        If the process cannot be stopped this call should exit with code
        STOP_FAILED.
        """
        if self.pid is None:

            return None

        try:

            while True:

                self.send(signal.SIGTERM)
                time.sleep(0.1)

        except RuntimeError as err:

            if "No such process" in str(err):

                LOG.info("Succesfully stopped the process.")
                return None

            LOG.exception("Failed to stop the process:")
            sys.exit(exit.STOP_FAILED)

        except TypeError as err:

            if "an integer is required" in str(err):

                LOG.info("Succesfully stopped the process.")
                return None

            LOG.exception("Failed to stop the process:")
            sys.exit(exit.STOP_FAILED)

    def restart(self):
        """Restart a runnin daemon."""
        self.stop()
        self.start()

    def run(self):
        """Perform the daemon logic."""
        raise NotImplementedError()


class SimpleStartStopStepManager(
    startstop.StartStopStepManager, SimpleStartStopManager
):

    """Step manager which leverages SimpleStartStopManager."""

    def step(self):
        """Perform the daemon logic."""
        raise NotImplementedError()
