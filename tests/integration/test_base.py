import os
import uuid

import pytest

from daemons.base import Daemon


@pytest.fixture
def basic_daemon(tmpdir):

    pidfile_name = str(tmpdir.join('test_pid_%s.pid' %(uuid.uuid4(),)))
    return Daemon(pidfile=pidfile_name)


@pytest.fixture
def patched_daemon(basic_daemon):

    basic_daemon.run = lambda: None
    basic_daemon._double_fork = lambda: None
    return basic_daemon


def test_start_creates_pidfile(patched_daemon):

    pidfile = patched_daemon.pidfile
    patched_daemon.start()

    assert os.path.exists(pidfile)


def test_shutdown_deletes_pidfile(patched_daemon):

    pidfile = patched_daemon.pidfile
    patched_daemon.start()
    try:
        patched_daemon.shutdown()
    except SystemExit:
        pass

    assert not os.path.exists(pidfile)


def test_shutdown_runs_custom_tear_down_functions(patched_daemon):

    patched_daemon.start()

    state = {"passed": False}
    def custom_tear_down():
        state['passed'] = True
    patched_daemon.tear_down.append(custom_tear_down)

    try:
        patched_daemon.shutdown()
    except SystemExit:
        pass

    assert state['passed'] is True
