"""This module contains a Daemon extension that listens for messages."""

import time
import logging

LOG = logging.getLogger(__name__)

from ..base import Daemon


class MessageDaemon(Daemon):
    """This daemon provides a specialized interface over the base daemon.

    This daemon implements its own 'run()' method which enters a loop of
    polling for messages and then dispatching those messages.

    In order to implement this daemon the 'get_message()' and
    'handle_message()' methods must be defined.

    Messages daemons can be constructed with an optional 'idle_time' which is
    the amount of time to sleep/idle when 'get_message()' returns None.
    """

    # This alias for sleep is placed here to allow extensions to change the
    # idle behaviour of the loop without monkey patching the time library.
    sleep = time.sleep

    def __init__(self, pidfile, idle_time=0.1):

        self.idle_time = idle_time

        super(MessageDaemon, self).__init__(pidfile)

        LOG.info(
            "Starting message daemon (%r) with idle time (%r).",
            pidfile,
            idle_time
        )

    def run(self):
        """This method puts the daemon into a poll/action loop.

        This method should not be extended or overwritten. Instead,
        implementations of this daemon should implement the 'get_message()'
        and 'handle_message()' methods.
        """

        while True:

            message = self.get_message()
            LOG.debug("Daemon (%r) got message (%r).", self.pidfile, message)

            if message is None:

                LOG.debug(
                    "Daemon (%r) did not get message. Going idle for (%r).",
                    self.pidfile,
                    self.idle_time
                )

                self.sleep(self.idle_time)
                continue

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
