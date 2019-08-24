"""Simple signal manager implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import logging
import os
import signal
import sys

from ..interfaces import signal as signal_iface
from ..interfaces import exit


LOG = logging.getLogger(__name__)


class SimpleSignalManager(signal_iface.SignalManager):

    """SignalManager which uses the python signal module."""

    kill_signals = (2, 3, 6, 15)  # SIGINT  # SIGQUIT  # SIGABRT  # SIGTERM

    def __init__(self, *args, **kwargs):
        """Initialize the manager with a handler map."""
        super(SimpleSignalManager, self).__init__(*args, **kwargs)

        self._handlers = collections.defaultdict(list)

        # Set up a listener for all possible signals on the system.
        for sig in self.kill_signals:

            signal.signal(sig, self._handle_signals)

    def handle(self, signum, handler):
        """Set a function to run when the given signal is recieved.

        Multiple handlers may be assigned to a single signal. The order of
        handlers does not need to be preserved.

        'signum' must be an integer representing a signal.

        'handler' must be a callable.
        """
        if not isinstance(signum, int):

            raise TypeError(
                "Signals must be given as integers. Got {0}.".format(
                    type(signum)
                )
            )

        if not callable(handler):

            raise TypeError("Signal handlers must be callable.")

        signal.signal(signum, self._handle_signals)
        self._handlers[signum].append(handler)

    def send(self, signum):
        """Send the given signal to the running process.

        If the process is not running a RuntimeError with a message of "No such
        process" should be emitted.
        """
        if not isinstance(signum, int):

            raise TypeError(
                "Signals must be given as integers. Got {0}.".format(
                    type(signum)
                )
            )

        try:

            os.kill(self.pid, signum)

        except OSError as err:

            if "No such process" in err.strerror:

                raise RuntimeError("No such process {0}.".format(self.pid))

            raise err

    def _handle_signals(self, signum, frame):
        """Handler for all signals.

        This method must be used to handle all signals for the process. It is
        responsible for runnin the appropriate signal handlers registered with
        the 'handle' method unless they are shutdown signals. Shutdown signals
        must trigger the 'shutdown' method.
        """
        if signum in self.kill_signals:

            return self.shutdown(signum)

        for handler in self._handlers[signum]:

            handler()

    def shutdown(self, signum):
        """Handle all signals which trigger a process stop.

        This method should run all appropriate signal handlers registered
        through the 'handle' method. At the end it should cause the process
        to exit with a status code. If any of the handlers raise an exception
        the exit code should be SHUTDOWN_FAILED otherwise SUCCESS.
        """
        dirty = False
        for handler in self._handlers[signum]:

            try:

                handler()

            except:  # noqa(E722)
                # The E722 (no bare except) setting is disabled here. The use
                # of bare except is intentional. The goal of this is to catch
                # _any_ error that escapes and ensure the process exits.

                LOG.exception("A shutdown handler failed to execute:")
                dirty = True

        del self.pid

        if dirty:

            sys.exit(exit.SHUTDOWN_FAILED)
            return None

        sys.exit(exit.SUCCESS)
        return None
