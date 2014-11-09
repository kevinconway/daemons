"""Standard interface for daemon signal management."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class SignalManager(object):

    """Implementations of this mixin provide management of signals."""

    def handle(self, signal, handler):
        """Set a function to run when the given signal is recieved.

        Multiple handlers may be assigned to a single signal. The order of
        handlers does not need to be preserved.

        'signal' must be an integer representing a signal.

        'handler' must be a callable.
        """
        raise NotImplementedError()

    def send(self, signal):
        """Send the given signal to the running process.

        If the process is not running a RuntimeError should be emitted.
        """
        raise NotImplementedError()

    def _handle_signals(self, signum, frame):
        """Handler for all signals.

        This method must be used to handle all signals for the process. It is
        responsible for runnin the appropriate signal handlers registered with
        the 'handle' method unless they are shutdown signals. Shutdown signals
        must trigger the 'shutdown' method.
        """
        raise NotImplementedError()

    def shutdown(self):
        """Handle all signals which trigger a process stop.

        This method should run all appropriate signal handlers registered
        through the 'handle' method. At the end it should cause the process
        to exit with a status code. If any of the handlers raise an exception
        the exit code should be SHUTDOWN_FAILED otherwise SUCCESS.
        """
        raise NotImplementedError()
