"""Sample daemon which just sleeps."""

import time

from daemons.prefab import run


class SleepyStepDaemon(run.RunDaemon):

    """A daemon which uses time.sleep as the action."""

    def step():
        """Main functionality goes here. This is called in a loop."""
        time.sleep(1)
