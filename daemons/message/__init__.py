"""This module contains a Daemon extension that listens for messages."""

import logging
import time

from ..base import Daemon


LOG = logging.getLogger(__name__)


class MessageDaemon(Daemon):
    """This daemon provides a specialized interface over the base daemon.

    This daemon implements its own 'run()' method which enters a loop of
    polling for messages and then dispatching those messages.

    In order to implement this daemon the 'get_message()' and
    'handle_message()' methods must be defined.

    Message daemons can be constructed with an optional 'idle_time' which is
    the amount of time to sleep/idle when 'get_message()' returns None.
    """

    # This alias for sleep is placed here to allow extensions to change the
    # idle behaviour of the loop without monkey patching the time library.
    sleep = staticmethod(time.sleep)

    def __init__(self, pidfile, idle_time=0.1):

        self.idle_time = idle_time

        super(MessageDaemon, self).__init__(pidfile)

        LOG.info(
            "Starting message daemon (%r) with idle time (%r).",
            self.pid,
            self.idle_time,
        )

    def _step(self):
        """This method grabs a new message and dispaches it to the handler.

        This method should not be extended or overwritten. Instead,
        implementations of this daemon should implement the 'get_message()'
        and 'handle_message()' methods.
        """

        message = self.get_message()
        LOG.debug("Daemon (%r) got message (%r).", self.pid, message)

        if message is None:

            self.sleep(self.idle_time)
            return

        self.handle_message(message)

    def get_message(self):
        """This method returns a message.

        The means by which this method retrieves message is determined by the
        implementation.

        The content and type of the message returned are also determined by the
        implementation.

        Whether or not this method blocks until a message can be retrieved is
        determined by the implementation.

        The only constraint placed on this method is that it must return 'None'
        when returning an empty message or no message.
        """

        raise NotImplementedError()

    def handle_message(self, message):
        """This method uses a message to initiate some action.


        """

        raise NotImplementedError()
