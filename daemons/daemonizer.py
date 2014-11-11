"""Function wrappers which create daemons."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import functools

from .prefab import run as rund
from .prefab import step as stepd


class DaemonizingWrapper(object):

    """Function wrapper which daemonizes the wrapped function."""

    DaemonClass = None

    def __init__(self, pidfile, signals=None):
        """Initialize the wrapper with a pidfile and signal handler mapping."""
        self._pidfile = pidfile
        self._signals = signals or {}

        if not isinstance(self._signals, dict):

            raise TypeError("Signals must be a dictionary.")

    def __call__(self, fn):
        """Decorate a function with daemonization."""
        d = self.DaemonClass(pidfile=self._pidfile)

        for signum, handlers in self._signals.items():

            for handler in handlers:

                d.handle(signum, handler)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            """Start daemonization and pass args to the original func."""
            d._fn = functools.partial(fn, *args, **kwargs)
            d.start()

        wrapper.stop = lambda: d.stop()

        return wrapper


class RunDaemonWrapper(rund.RunDaemon):

    """RunDaemon which runs some arbitrary function."""

    _fn = None

    def run(self):
        """Run the arbitrary function."""
        self._fn()


class StepDaemonWrapper(stepd.StepDaemon):

    """StepDaemon which runs some arbitrary function."""

    _fn = None

    def step(self):
        """Run the arbitrary function."""
        self._fn()


class RunDaemonizingWrapper(DaemonizingWrapper):

    """Function wrapper which wraps using a RunDaemon."""

    DaemonClass = RunDaemonWrapper


class StepDaemonizingWrapper(DaemonizingWrapper):

    """Function wrapper which wraps using a StepDaemon."""

    DaemonClass = StepDaemonWrapper


run = RunDaemonizingWrapper
step = StepDaemonizingWrapper
