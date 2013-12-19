"""This module contains the base daemon class.

This daemon implementation is a modification of work performed by Sander
Marechal. Sander's original work can be found at
http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/.

Modifications to the original include:

-   Unix signal handling to provide process cleanup.
-   Updated Python syntax.
-   Integration of Python 'logging' module.
"""

from functools import partial
import logging
import os
import signal
import sys
import time


LOG = logging.getLogger(__name__)


class Daemon(object):
    """A generic daemon class.

    This class should not be used directly. Instead, it should be subclassed.

    All subclasses must define a 'run()' method.

    Any methods that need to be run on stop should be appended to the
    'tear_down' list. These must be callables that accept no arguments.

    All tear_down failures are logged but do not prevent the daemon from
    stopping.

    This Daemon listens for SIGABRT, SIGINT, SIGQUIT, and SIGTERM. When any one
    of these signals is recieved the shutdown/cleanup process is executed.
    """

    tear_down = []

    def __init__(self, pidfile):

        self.pid = None
        self.pidfile = pidfile
        if not self.pidfile.startswith('/'):
            self.pidfile = os.path.join(os.getcwd(), self.pidfile)

        self.tear_down.append(partial(os.remove, self.pidfile))

        signal.signal(signal.SIGABRT, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGQUIT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def daemonize(self):

        self._double_fork()

        # Write pidfile.
        self.pid = str(os.getpid())

        try:

            with open(self.pidfile, 'w+') as pidfile:

                pidfile.write("%s\n" % (self.pid,))

        except IOError:

            LOG.exception("Failed to write pidfile (%s).", self.pidfile)
            sys.exit(1)

        LOG.info(
            "Daemon (%s) process running with pidfile (%s).",
            self.pid,
            self.pidfile,
        )

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

        except OSError as err:

            LOG.exception("Fork #1 failed: %d (%s)", err.errno, err.strerror)
            sys.exit(1)

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
                "Fork #2 failed: %d (%s)",
                err.errno, err.strerror
            )
            sys.exit(1)

    def start(self):
        """Start the daemon."""

        # Check to see if the daemon is already running.
        try:

            with open(self.pidfile, 'r') as pidfile:

                pid = int(pidfile.read().strip())

        except IOError:

            pid = None

        if pid is not None:

            message = "Pidfile %s already exist. Cannot start daemon."
            LOG.error(message, self.pidfile)
            sys.exit(1)

        # Start the daemon.
        self.daemonize()

        # Begin the daemon actions.
        try:

            LOG.info("Daemon (%s) entering run loop.", self.pid)
            self.run()

        except Exception:

            message = "Uncaught exception in the daemon run() method for (%s)"
            LOG.exception(message, self.pid)

    def stop(self, ignore=False):
        """Stop the daemon.

        If the 'ignore' parameter is set to True then a failure to stop the
        daemon will not result in an error.
        """

        # Get the pid from the pidfile.
        try:

            with open(self.pidfile, 'r') as pidfile:

                pid = int(pidfile.read().strip())

        except IOError:

            pid = None

        if pid is None:

            if ignore is True:

                message = "No pidfile (%s) found when calling stop."
                LOG.warning(message, self.pidfile)

                return None

            message = "Pidfile %s does not exist. Cannot stop daemon."
            LOG.error(message, self.pidfile)
            sys.exit(1)

        # Try killing the daemon process.
        try:

            while True:

                # Here we use a SIGTERM to kill the process for two reasons:
                # 1) It ensures that the cleanup functions are triggered.
                # 2) It allows for stop to be used in something similar to
                # an init script. For example, if you want a script that can
                # start/stop/restart the daemon process it needs to be able
                # to stop the process after it is already daemonized. Since
                # the stop() method cannot be called on the daemonized object
                # directly we use the signal to trigger the desired behaviour.
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)

        except OSError as err:

            # Check that the process has been killed and force removal
            # of the pidfile in the event of a cleanup failure.
            err_string = str(err)
            if err_string.find("No such process") > 0:

                if os.path.exists(self.pidfile):

                    os.remove(self.pidfile)

            else:

                LOG.exception("Failed to kill process (%s).", self.pid)
                sys.exit(1)

        LOG.info("Daemon (%s) stopped.", self.pid)

    def shutdown(self, *args, **kwargs):
        """Run all cleanup functions and then exit."""

        status = 0

        LOG.info("Daemon (%s) running cleanup.", self.pid)
        for func in self.tear_down:

            try:

                func()

            except Exception:

                status = 1
                LOG.exception("A tear down function failed to complete.")

        LOG.info("Daemon (%s) done running cleanup.", self.pid)
        sys.exit(status)

    def restart(self):
        """Restart the daemon."""

        LOG.info("Daemon (%s) restarting.", self.pid)
        self.stop(ignore=True)
        self.start()

    def run(self):
        """Begin the main daemon loop.

        This method will repeatedly call the '_step()' method.
        """

        while True:

            self._step()

    def _step(self):
        """Overwrite this method to implement daemon behaviour."""

        raise NotImplementedError()
