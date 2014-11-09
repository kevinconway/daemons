"""Standard interface for message management functionality."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import time


class MessageManager(object):

    """Implementations provide management of messages to the process."""

    # This alias for sleep is placed here to allow extensions to change the
    # idle behaviour of the loop without monkey patching the time library.
    sleep = staticmethod(time.sleep)

    def __init__(self, *args, **kwargs):
        """Initialize the daemon with an idle_time and pool_size."""
        self.idle_time = kwargs.pop("idle_time", 0.1)
        self.pool_size = kwargs.pop("pool_size", 100)

        super(MessageManager, self).__init__(*args, **kwargs)

    @property
    def pool(self):
        """Get a pool used to dispatch requests."""
        raise NotImplementedError()

    def dispatch(self, message):
        """Execute handle_message within a context from the pool."""
        raise NotImplementedError()

    def step(self):
        """Grab a new message and dispatch it to the handler.

        This method should not be extended or overwritten. Instead,
        implementations of this daemon should implement the 'get_message()'
        and 'handle_message()' methods.
        """
        message = self.get_message()
        if message is None:

            self.sleep(self.idle_time)
            return None

        self.dispatch(message)
        # In non-greenthread environments this does nothing. In green-thread
        # environments this yields the context so messages can be acted upon
        # before exhausting the threadpool.
        self.sleep(0)

    def get_message(self):
        """Get a message from some source.

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
        """Do something with a message."""
        raise NotImplementedError()
