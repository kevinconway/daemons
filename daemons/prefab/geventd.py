"""Gevent message daemon missing get_message and handle_message."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from ..daemonize import simple as simple_daemonize
from ..pid import simple as simple_pid
from ..signal import simple as simple_signal
from ..startstop import simple as simple_startstop
from ..message import gevent as geventd


class GeventDaemon(
    simple_pid.SimplePidManager,
    simple_signal.SimpleSignalManager,
    simple_daemonize.SimpleDaemonizeManager,
    simple_startstop.SimpleStartStopStepManager,
    geventd.GeventMessageManager,
):

    """Message daemon which leverages gevent."""
