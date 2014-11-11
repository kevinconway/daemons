"""Message manager implementation powered by eventlet."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import eventlet

from ..interfaces import message


class EventletMessageManager(message.MessageManager):

    """MessageManager that uses eventlet for message dispatching."""

    @property
    def pool(self):
        """Get an eventlet pool used to dispatch requests."""
        self._pool = self._pool or eventlet.GreenPool(size=self.pool_size)
        return self._pool

    def dispatch(self, message):
        """Execute handle_message within a context from the pool."""
        self.pool.spawn_n(self.handle_message, message)
