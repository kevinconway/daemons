"""Test suite for the simple pid manager implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import getpass
import os

from daemons.pid import simple


def test_empty_pid_when_not_exist(tmpdir):
    """Test that the pid is None when the file does not exist."""
    m = simple.SimplePidManager(pidfile=str(tmpdir.join("test.pid")))
    assert m.pid is None


def test_pidfile_is_absolute_path():
    """Test that the pidfile is converted to an absolute path."""
    pidfile = "~/test.pid"
    user = getpass.getuser()
    m = simple.SimplePidManager(pidfile=pidfile)
    assert "~" not in m.pidfile
    assert m.pidfile == "{0}/test.pid".format(os.path.expanduser("~"))
    assert user in m.pidfile


def test_reads_pid_when_exists(tmpdir):
    """Test that the pid is read when available."""
    pidfile = str(tmpdir.join("test.pid"))
    pid = os.getpid()
    with open(pidfile, "w+") as f:

        f.write("{0}\n".format(pid))

    m = simple.SimplePidManager(pidfile=pidfile)
    assert m.pid == pid


def test_deletes_pid(tmpdir):
    """Test that the pidfile is deleted when using del."""
    pidfile = str(tmpdir.join("test.pid"))
    pid = os.getpid()
    with open(pidfile, "w+") as f:

        f.write("{0}\n".format(pid))

    m = simple.SimplePidManager(pidfile=pidfile)
    del m.pid
    assert not tmpdir.join("test.pid").check()
    assert m.pid is None


def test_handle_stale_pid(tmpdir):
    """Test that None is returned if pid is not running."""
    pidfile = str(tmpdir.join("test.pid"))
    # Linux normaly wraps pids at 32768, but the limit it 2^22
    # choose a value that is a legal pid that won't appear on the test system
    pid = 123456
    with open(pidfile, "w+") as f:

        f.write("{0}\n".format(pid))

    m = simple.SimplePidManager(pidfile=pidfile)
    assert m.pid is None
