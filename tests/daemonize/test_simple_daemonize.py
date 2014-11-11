"""Test suite for the double fork daemonize manager."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time

import pytest

from daemons.daemonize import simple
from daemons.pid import simple as simple_pid


class DaemonTest(simple_pid.SimplePidManager, simple.SimpleDaemonizeManager):

    """Daemon for testing."""


@pytest.fixture
def pidfile(tmpdir):
    """Get a pidfile in tmp space."""
    return str(tmpdir.join("test.pid"))


@pytest.fixture
def handler(pidfile):
    """Get an instance of the daemonize manager."""
    return DaemonTest(pidfile=pidfile)


def test_double_fork_daemonizes(handler, monkeypatch):
    """Test that double fork daemonizes a process."""
    monkeypatch.setattr(sys, "exit", lambda code: code)
    handler.daemonize()
    monkeypatch.undo()

    # Tests were failing intermittently due to a timing issue where the pid
    # file would still be in the process of writing to disk while being read
    # from.
    time.sleep(.1)
    assert handler.pid is not None
