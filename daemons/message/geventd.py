"""This module contains a MessageDaemon extension that uses gevent."""

import logging

import gevent
import gevent.pool

from .pooled import PooledMessageDaemon


LOG = logging.getLogger(__name__)


class GeventMessageDaemon(PooledMessageDaemon):
    """This daemon extends the base PooledMessageDaemon class to use gevent.

    The implementation interface is exactly the same as the MessageDaemon. The
    only differences are that the sleep/idle mechanism is replaced by a
    cooperative yield from gevent and each message is dispatched on a
    different gevent thread.
    """

    sleep = staticmethod(gevent.sleep)

    def _create_pool(self, pool_size):

        return gevent.pool.Pool(size=pool_size)

    def _dispatch(self, func):

        LOG.debug(
            "Daemon (%r) attempting to start new greenthread with (%r) "
            "active and (%r) free",
            self.pid,
            self.pool.size - self.pool.free_count(),
            self.pool.free_count(),
        )
        self.pool.spawn_raw(func)
