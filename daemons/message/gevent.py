"""Message manager implementation powered by gevent."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import gevent

from ..interfaces import message


class GeventMessageManager(message.MessageManager):

    """MessageManager that uses gevent for message dispatching."""

    @property
    def pool(self):
        """Get an gevent pool used to dispatch requests."""
        self._pool = self._pool or gevent.pool.Pool(size=self.pool_size)
        return self._pool

    def dispatch(self, message):
        """Execute handle_message within a context from the pool."""
        self.pool.spawn(self.handle_message, message)
