"""Test suite for the simple signal manager implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import signal
import sys

import pytest

from daemons.signal import simple


@pytest.fixture
def pid():
    """Get the current process id."""
    return os.getpid()


@pytest.fixture
def handler(pid):
    """Get an instance of the signal manager."""
    m = simple.SimpleSignalManager()
    m.pid = pid
    return m


@pytest.fixture
def nonstop_signal():
    """Get a signal which does not stop the process."""
    return signal.SIGCHLD


@pytest.fixture
def stop_signal():
    """Get a signal which stops the process."""
    return signal.SIGTERM


def test_can_send_signals(handler, nonstop_signal):
    """Test that the manager can send signals to a process."""
    triggered = {"value": False}

    def flip_bit(signum, frame):

        triggered["value"] = True

    signal.signal(nonstop_signal, flip_bit)
    handler.send(nonstop_signal)

    assert triggered["value"] is True


def test_can_register_signal_handlers(handler, pid, nonstop_signal):
    """Test that the manager can register signal handlers."""
    triggered = {"value": False}

    def flip_bit():

        triggered["value"] = True

    handler.handle(nonstop_signal, flip_bit)
    os.kill(pid, nonstop_signal)

    assert triggered["value"] is True


def test_triggers_shutdown_on_stop(handler, pid, stop_signal, monkeypatch):
    """Test that the manager can handle stop signals."""
    triggered = {"value": False}
    exited = {"value": False, "code": -1}

    def trigger():

        triggered["value"] = True

    def exit(code):

        exited["value"] = True
        exited["code"] = code

    monkeypatch.setattr(sys, "exit", exit)
    handler.handle(stop_signal, trigger)
    os.kill(pid, stop_signal)
    monkeypatch.undo()

    assert triggered["value"] is True
    assert exited["value"] is True
    assert exited["code"] == 0
    assert hasattr(handler, "pid") is False or handler.pid is None
