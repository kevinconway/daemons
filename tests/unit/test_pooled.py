import uuid

import pytest

from daemons.message.pooled import PooledMessageDaemon


@pytest.fixture
def pooled_daemon(tmpdir):

    pidfile_name = str(tmpdir.join('test_pid_%s.pid' %(uuid.uuid4(),)))
    class TestDaemon(PooledMessageDaemon):
        def _create_pool(self, pool_size):
            return pool_size
        def _dispatch(self, func):
            return func()
    d = TestDaemon(
        pidfile=pidfile_name,
        idle_time=0.1,
        pool_size=10,
        aggressive_yield=True,
    )
    d.run = lambda: None
    d._double_fork = lambda: None

    return d


def test_init_creates_pool(pooled_daemon):

    # The pool should be set to whatever is returned from the _create_pool
    # implementation. For the test the pool_size is returned for a simple
    # sanity check.
    assert pooled_daemon.pool == pooled_daemon.pool_size


def test_step_calls_get_message(pooled_daemon):

    count = {"get_message": 0}
    def get_message():
        count['get_message'] += 1

    pooled_daemon.get_message = get_message
    pooled_daemon.handle_message = lambda x,y: None

    pooled_daemon._step()

    assert count['get_message'] == 1

def test_step_calls_handle_message(pooled_daemon):

    count = {"handle_message": 0}
    def handle_message(message):
        count['handle_message'] += 1

    pooled_daemon.get_message = lambda: True
    pooled_daemon.handle_message = handle_message

    pooled_daemon._step()

    assert count['handle_message'] == 1


def test_step_brokers_message_to_handle_message(pooled_daemon):

    state = {"message": None}
    def handle_message(message):
        state['message'] = message

    pooled_daemon.get_message = lambda: "PASS"
    pooled_daemon.handle_message = handle_message

    pooled_daemon._step()

    assert state['message'] == "PASS"


def test_step_exist_early_on_empty_message(pooled_daemon):
    count = {"get_message": 0, "handle_message": 0}
    def get_message():
        count['get_message'] += 1
        return None
    def handle_message(message):
        count['handle_message'] += 1

    pooled_daemon.get_message = get_message
    pooled_daemon.handle_message = handle_message

    pooled_daemon._step()

    assert count['get_message'] == 1
    assert count['handle_message'] == 0


def test_step_does_not_sleep_when_aggressive_yield_is_false(pooled_daemon):
    count = {"sleep": 0}
    def sleep(length):
        count['sleep'] += 1

    pooled_daemon.aggressive_yield = False
    pooled_daemon.sleep = sleep
    pooled_daemon.get_message = lambda: True
    pooled_daemon.handle_message = lambda x: True

    pooled_daemon._step()

    assert count['sleep'] == 0


def test_step_does_sleep_when_aggressive_yield_is_true(pooled_daemon):
    count = {"sleep": 0}
    def sleep(length):
        count['sleep'] += 1

    pooled_daemon.sleep = sleep
    pooled_daemon.get_message = lambda: True
    pooled_daemon.handle_message = lambda x: True

    pooled_daemon._step()

    assert count['sleep'] == 1
