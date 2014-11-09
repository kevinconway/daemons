"""Standard interface for daemon start/stop/restart management."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class StartStopManager(object):

    """Implementations of this mixin provide process start/stop management."""

    def start(self):
        """Start the process with daemonization.

        If the process is already started this call should exit with code
        ALREADY_RUNNING. Otherwise it must call the 'daemonize' method and then
        call 'run'.
        """
        raise NotImplementedError()

    def stop(self):
        """Stop the daemonized process.

        If the process is already stopped this call should exit successfully.
        If the process cannot be stopped this call should exit with code
        STOP_FAILED.
        """
        raise NotImplementedError()

    def restart(self):
        """Restart a runnin daemon."""
        raise NotImplementedError()

    def run(self):
        """Perform the daemon logic."""
        raise NotImplementedError()


class StartStopStepManager(StartStopManager):

    """Implementations of this mixin provide process start/stop management.

    This differs from the standard start/stop manager in that it handles
    looping forever opting, instead, for calling a 'step' method which
    implements the daemon logic in discrete calls rather than a loop itself.
    """

    def run(self):
        """Loop forever and call 'step'."""
        while True:

            self.step()

    def step(self):
        """Perform the daemon logic."""
        raise NotImplementedError()
