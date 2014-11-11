"""Function wrappers which create daemons."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import functools

from .prefab import run as rund
from .prefab import step as stepd


def run(pidfile):
    """Wrap a function is a RunDaemon object."""
    def outer_wrapper(fn):

        class RunDaemonWrapper(rund.RunDaemon):

            """RunDaemon which wraps some arbitrary function."""

            _fn = None

            def run(self):

                self._fn()

        d = RunDaemonWrapper(pidfile=pidfile)

        @functools.wraps(fn)
        def inner_wrapper(*args, **kwargs):

            d._fn = functools.partial(fn, *args, **kwargs)
            d.start()

        inner_wrapper.stop = lambda: d.stop()

        return inner_wrapper

    return outer_wrapper


def step(pidfile):
    """Wrap a function is a StepDaemon object."""
    def outer_wrapper(fn):

        class StepDaemonWrapper(stepd.StepDaemon):

            """StepDaemon which wraps some arbitrary function."""

            _fn = None

            def step(self):

                self._fn()

        d = StepDaemonWrapper(pidfile=pidfile)

        @functools.wraps(fn)
        def inner_wrapper(*args, **kwargs):

            d._fn = functools.partial(fn, *args, **kwargs)
            d.start()

        inner_wrapper.stop = lambda: d.stop()

        return inner_wrapper

    return outer_wrapper
