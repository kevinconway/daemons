"""This module contains a MessageDaemon extension that uses gevent."""

import logging

import gevent
import gevent.pool

from . import MessageDaemon


LOG = logging.getLogger(__name__)


class GeventMessageDaemon(MessageDaemon):
    """This daemon extends the base MessageDaemon class to use gevent.

    The implementation interface is exactly the same as the MessageDaemon. The
    only differences are that the sleep/idle mechanism is replaced by a
    cooperative yield from gevent and each message is dispatched on a
    different gevent thread.
    """

    sleep = staticmethod(gevent.sleep)

    def __init__(self,
                 pidfile,
                 idle_time=0.1,
                 pool_size=100,
                 aggressive_yield=False):

        self.pool_size = pool_size
        self.aggressive_yield = aggressive_yield

        super(GeventMessageDaemon, self).__init__(pidfile, idle_time)

        LOG.info(
            "Starting gevent message daemon (%r) with pool size (%r) and "
            "aggresive yield set to (%r).",
            self.pid,
            self.pool_size,
            self.aggressive_yield,
        )

    def run(self):
        """This method puts the daemon into a poll/action loop.

        This method should not be extended or overwritten. Instead,
        implementations of this daemon should implement the 'get_message()'
        and 'handle_message()' methods.

        This loop makes use of an gevent Pool to manage maximum greenthread
        concurrency. The behaviour of the pool, and greenthreads in general, is
        such that there must be a cooperative yield in order for gevent to
        switch context into another greenthread.

        This loop, by default, will only yield on an empty message and when the
        Pool has allocated the maximum allowed greenthreads. To yield the
        loop after each message, set the aggressive_yield bit to True.
        """

        pool = gevent.pool.Pool(size=self.pool_size)

        while True:

            message = self.get_message()
            LOG.debug(
                "Daemon (%r) got message (%r).",
                self.pid,
                message,
            )

            if message is None:

                LOG.debug(
                    "Daemon (%r) received no message. Going idle for (%r).",
                    self.pid,
                    self.idle_time,
                )

                self.sleep(self.idle_time)
                continue

            LOG.debug(
                "Daemon (%r) attempting to start new greenthread with (%r) "
                "active and (%r) free",
                self.pid,
                pool.size - pool.free_count(),
                pool.free_count(),
            )
            pool.spawn(self.handle_message, message)

            if self.aggressive_yield is True:

                gevent.sleep(0)
