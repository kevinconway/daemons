"""Sample daemon which just sleeps."""

import time

from daemons.prefab import run


class SleepyDaemon(run.RunDaemon):

    """A daemon which uses time.sleep as the action."""

    def run():
        """Main functionality loop goes here."""
        while True:

            time.sleep(1)
