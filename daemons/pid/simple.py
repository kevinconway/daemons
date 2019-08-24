"""Simple pid manager implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import sys
import errno

from ..interfaces import pid
from ..interfaces import exit


LOG = logging.getLogger(__name__)


class SimplePidManager(pid.PidManager):

    """PidManager which uses a simple pidfile."""

    @property
    def pid(self):
        """Get the pid which represents a daemonized process.

        The result should be None if the process is not running.
        """
        try:

            with open(self.pidfile, "r") as pidfile:

                try:

                    pid = int(pidfile.read().strip())

                except ValueError:

                    return None

                try:

                    os.kill(pid, 0)

                except OSError as e:

                    if e.errno == errno.EPERM:

                        return pid

                    elif e.errno == errno.ESRCH:

                        return None

                    LOG.exception(
                        "os.kill returned unhandled error "
                        "{0}".format(e.strerror)
                    )
                    sys.exit(exit.PIDFILE_ERROR)

                return pid

        except IOError:

            if not os.path.isfile(self.pidfile):

                return None

            LOG.exception("Failed to read pidfile {0}.".format(self.pidfile))
            sys.exit(exit.PIDFILE_INACCESSIBLE)

    @pid.setter
    def pid(self, pidnum):
        """Set the pid for a running process."""
        try:

            with open(self.pidfile, "w+") as pidfile:

                pidfile.write("{0}\n".format(pidnum))

        except IOError:

            LOG.exception("Failed to write pidfile {0}).".format(self.pidfile))
            sys.exit(exit.PIDFILE_INACCESSIBLE)

    @pid.deleter
    def pid(self):
        """Stop managing the current pid."""
        try:

            os.remove(self.pidfile)

        except IOError:

            if not os.path.isfile(self.pidfile):

                return None

            LOG.exception("Failed to clear pidfile {0}).".format(self.pidfile))
            sys.exit(exit.PIDFILE_INACCESSIBLE)
