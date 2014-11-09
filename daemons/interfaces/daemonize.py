"""Standard interface for daemonization logic."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class DaemonizeManager(object):

    """Implementations of this mixin provide process daemonization."""

    def daemonize(self):
        """Background and daemonize the process.

        Once daemonized the pid must be set to the correct value. If there is
        and error in daemonization the exit code should be DAEMONIZE_FAILED.
        """
        raise NotImplementedError()
