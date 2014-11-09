"""Test suite for the double fork daemonize manager."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys

import pytest

from daemons.daemonize import simple
from daemons.pid import simple as simple_pid


class TestDaemon(simple_pid.SimplePidManager, simple.SimpleDaemonizeManager):

    """Daemon for testing."""


@pytest.fixture
def pidfile(tmpdir):
    """Get a pidfile in tmp space."""
    return str(tmpdir.join("test.pid"))


@pytest.fixture
def handler(pidfile):
    """Get an instance of the daemonize manager."""
    return TestDaemon(pidfile=pidfile)


def test_double_fork_daemonizes(handler, monkeypatch):
    """Test that double fork daemonizes a process."""
    monkeypatch.setattr(sys, "exit", lambda code: code)
    handler.daemonize()
    monkeypatch.undo()

    assert handler.pid is not None
