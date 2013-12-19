import uuid

import pytest

from daemons.message import MessageDaemon


@pytest.fixture
def message_daemon(tmpdir):

    pidfile_name = str(tmpdir.join('test_pid_%s.pid' %(uuid.uuid4(),)))
    d = MessageDaemon(
        pidfile=pidfile_name,
        idle_time=0.1,
    )
    d.run = lambda: None
    d._double_fork = lambda: None

    return d


def test_step_calls_get_message(message_daemon):

    count = {"get_message": 0}
    def get_message():
        count['get_message'] += 1

    message_daemon.get_message = get_message
    message_daemon.handle_message = lambda x,y: None

    message_daemon._step()

    assert count['get_message'] == 1

def test_step_calls_handle_message(message_daemon):

    count = {"handle_message": 0}
    def handle_message(message):
        count['handle_message'] += 1

    message_daemon.get_message = lambda: True
    message_daemon.handle_message = handle_message

    message_daemon._step()

    assert count['handle_message'] == 1


def test_step_brokers_message_to_handle_message(message_daemon):

    state = {"message": None}
    def handle_message(message):
        state['message'] = message

    message_daemon.get_message = lambda: "PASS"
    message_daemon.handle_message = handle_message

    message_daemon._step()

    assert state['message'] == "PASS"


def test_step_exist_early_on_empty_message(message_daemon):
    count = {"get_message": 0, "handle_message": 0}
    def get_message():
        count['get_message'] += 1
        return None
    def handle_message(message):
        count['handle_message'] += 1

    message_daemon.get_message = get_message
    message_daemon.handle_message = handle_message

    message_daemon._step()

    assert count['get_message'] == 1
    assert count['handle_message'] == 0
