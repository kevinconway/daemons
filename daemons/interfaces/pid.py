"""Standard interface for PID management functionality."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os


class PidManager(object):

    """Implementations of this mixin provide management of a PID."""

    def __init__(self, *args, **kwargs):
        """Initialize the daemon with a pidfile."""
        self._pidfile = kwargs.pop("pidfile", None)
        if not self._pidfile:

            raise ValueError("Pidfile cannot be None.")

        super(PidManager, self).__init__(*args, **kwargs)

    @property
    def pidfile(self):
        """Get the absolute path of the pidfile."""
        return os.path.abspath(
            os.path.expandvars(os.path.expanduser(self._pidfile))
        )

    @property
    def pid(self):
        """Get the pid which represents a daemonized process.

        The result should be None if the process is not running.
        """
        raise NotImplementedError()

    @pid.setter
    def pid(self, pidnum):
        """Set the pid for a running process."""
        raise NotImplementedError()

    @pid.deleter
    def pid(self):
        """Stop managing the current pid."""
        raise NotImplementedError()
