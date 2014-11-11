"""Test suite for the simple pid manager implementation."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import getpass

from daemons.pid import simple


def test_empty_pid_when_not_exist(tmpdir):
    """Test that the pid is None when the file does not exist."""
    m = simple.SimplePidManager(pidfile=str(tmpdir.join("test.pid")))
    assert m.pid is None


def test_pidfile_is_absolut_path():
    """Test that the pidfile is converted to an absolute path."""
    pidfile = "~/test.pid"
    user = getpass.getuser()
    m = simple.SimplePidManager(pidfile=pidfile)
    assert '~' not in m.pidfile
    assert m.pidfile == '/home/{0}/test.pid'.format(user)


def test_reads_pid_when_exists(tmpdir):
    """Test that the pid is read when available."""
    pidfile = str(tmpdir.join("test.pid"))
    with open(pidfile, "w+") as f:

        f.write("1234\n")

    m = simple.SimplePidManager(pidfile=pidfile)
    assert m.pid == 1234


def test_deletes_pid(tmpdir):
    """Test that the pidfile is deleted when using del."""
    pidfile = str(tmpdir.join("test.pid"))
    with open(pidfile, "w+") as f:

        f.write("4321\n")

    m = simple.SimplePidManager(pidfile=pidfile)
    del m.pid
    assert not tmpdir.join("test.pid").check()
    assert m.pid is None
