"""Noop daemonize manager implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os


class NoopDaemonizeManager(object):

    """Daemonizer which does nothing. Useful for testing and debugging."""

    def daemonize(self):
        """Do nothing."""
        self.pid = os.getpid()
        return None
