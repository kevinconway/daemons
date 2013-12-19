"""This module contains a MessageDaemon extension that uses execution pools."""

from functools import partial
import logging

from . import MessageDaemon


LOG = logging.getLogger(__name__)


class PooledMessageDaemon(MessageDaemon):
    """This daemon extends the base MessageDaemon class to use resource pools.

    The interface is identical. The difference is that subclasses of this
    daemon can execute message handling within a specialized execution context
    (thread, process, greenthread, etc.) that is managed by a pool.
    """

    def __init__(self,
                 pidfile,
                 idle_time=0.1,
                 pool_size=100,
                 aggressive_yield=False):

        super(PooledMessageDaemon, self).__init__(pidfile, idle_time)

        self.pool_size = pool_size
        self.aggressive_yield = aggressive_yield

        self.pool = self._create_pool(self.pool_size)

        LOG.info(
            "Starting pooled message daemon (%r) with pool size (%r) and "
            "aggresive yield set to (%r).",
            self.pid,
            self.pool_size,
            self.aggressive_yield,
        )

    def _create_pool(self, pool_size):
        """This method should return a resource pool."""

        raise NotImplementedError()

    def _dispatch(self, func):
        """This method should run a function in a context from the pool."""

        raise NotImplementedError()

    def _step(self):
        """This method grabs a new message and calls the pool dispatcher.

        This method should not be extended or overwritten. Instead,
        implementations of this daemon should implement the 'get_message()'
        and 'handle_message()' methods.

        This method will call '_dispatch' with a partial that binds the
        'handle_message' method and the message.
        """

        message = self.get_message()
        LOG.debug(
            "Daemon (%r) got message (%r).",
            self.pid,
            message,
        )

        if message is None:

            self.sleep(self.idle_time)
            return

        self._dispatch(partial(self.handle_message, message))

        if self.aggressive_yield is True:

            self.sleep(0)
