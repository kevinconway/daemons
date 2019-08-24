"""Simple daemonize manager implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import sys

from ..interfaces import daemonize as daemonize_iface
from ..interfaces import exit

LOG = logging.getLogger(__name__)


class SimpleDaemonizeManager(daemonize_iface.DaemonizeManager):

    """Daemonizer which does a unix double fork."""

    def daemonize(self):
        """Double fork and set the pid."""
        self._double_fork()

        # Write pidfile.
        self.pid = os.getpid()

        LOG.info("Succesfully daemonized process {0}.".format(self.pid))

    def _double_fork(self):
        """Do the UNIX double-fork magic.

        See Stevens' "Advanced Programming in the UNIX Environment" for details
        (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:

            pid = os.fork()
            if pid > 0:

                # Exit first parent.
                sys.exit(0)
                return None

        except OSError as err:

            LOG.exception(
                "Fork #1 failed: {0} ({1})".format(err.errno, err.strerror)
            )
            sys.exit(exit.DAEMONIZE_FAILED)
            return None

        # Decouple from parent environment.
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Do second fork.
        try:

            pid = os.fork()
            if pid > 0:

                # Exit from second parent.
                sys.exit(0)

        except OSError as err:

            LOG.exception(
                "Fork #2 failed: {0} ({1})".format(err.errno, err.strerror)
            )
            sys.exit(exit.DAEMONIZE_FAILED)
            return None
