"""This module contains a MessageDaemon extension that uses eventlet."""

import eventlet
import logging

LOG = logging.getLogger(__name__)

from . import MessageDaemon


class EventletMessageDaemon(MessageDaemon):
    """This daemon extends the base MessageDaemon class to use eventlet.

    The implementation interface is exactly the same as the MessageDaemon. The
    only differences are that the sleep/idle mechanism is replaced by a
    cooperative yield from eventlet and each message is dispatched on a
    different eventlet thread.
    """

    sleep = staticmethod(eventlet.sleep)

    def __init__(self,
                 pidfile,
                 idle_time=0.1,
                 pool_size=100,
                 aggressive_yield=False):

        self.pool_size = pool_size
        self.aggressive_yield = aggressive_yield

        super(EventletMessageDaemon, self).__init__(pidfile, idle_time)

        LOG.info(
            "Starting gevent message daemon (%r) with pool size (%r) and "
            "aggresive yield set to (%r).",
            self.pidfile,
            self.pool_size,
            self.aggressive_yield
        )

    def run(self):
        """This method puts the daemon into a poll/action loop.

        This method should not be extended or overwritten. Instead,
        implementations of this daemon should implement the 'get_message()'
        and 'handle_message()' methods.

        This loop makes use of an eventlet GreenPool to manage maximum
        greenthread concurrency. The behaviour of the pool, and greenthreads
        in general, is such that there must be a cooperative yield in order
        for eventlet to switch context into another greenthread.

        This loop, by default, will only yield on an empty message and when the
        GreenPool has allocated the maximum allowed greenthreads. To yield the
        loop after each message, set the aggressive_yield bit to True.
        """

        pool = eventlet.GreenPool(size=self.pool_size)

        while True:

            message = self.get_message()
            LOG.debug(
                "Daemon (%r) got message (%r).",
                self.pidfile,
                message
            )

            if message is None:

                LOG.debug(
                    "Daemon (%r) received no message. Going idle for (%r).",
                    self.pidfile,
                    self.idle_time
                )

                self.sleep(self.idle_time)
                continue

            LOG.debug(
                "Daemon (%r) attempting to start new greenthread with (%r) "
                "active and (%r) free",
                self.pidfile,
                pool.running(),
                pool.free()
            )
            pool.spawn(self.handle_message, message)

            if self.aggressive_yield is True:

                eventlet.sleep(0)
