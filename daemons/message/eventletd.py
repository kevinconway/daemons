"""This module contains a MessageDaemon extension that uses eventlet."""

import logging

import eventlet

from .pooled import PooledMessageDaemon


LOG = logging.getLogger(__name__)


class EventletMessageDaemon(PooledMessageDaemon):
    """This daemon extends the base PooledMessageDaemon class to use eventlet.

    The implementation interface is exactly the same as the MessageDaemon. The
    only differences are that the sleep/idle mechanism is replaced by a
    cooperative yield from eventlet and each message is dispatched on a
    different eventlet thread.
    """

    sleep = staticmethod(eventlet.sleep)

    def _create_pool(self, pool_size):

        return eventlet.GreenPool(size=pool_size)

    def _dispatch(self, func):

        LOG.debug(
            "Daemon (%r) attempting to start new greenthread with (%r) "
            "active and (%r) free",
            self.pid,
            self.pool.running(),
            self.pool.free(),
        )

        self.pool.spawn_n(func)
