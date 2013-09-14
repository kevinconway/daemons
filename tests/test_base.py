import logging
LOG = logging.getLogger(__name__)

import os
import time
import signal

from subprocess import call


def test_start(tmpdir):

    # Set up temp file paths.
    test_directory = os.path.dirname(os.path.realpath(__file__))
    temp_directory = str(tmpdir)
    helper_path = os.path.join(test_directory, 'sleepy.py')
    log_path = os.path.join(temp_directory, 'test.log')
    pid_path = os.path.join(temp_directory, 'test.pid')

    # Start the test daemon.
    call(['python',
          helper_path,
          pid_path,
          log_path,
          'start'])

    # Wait a second to make sure the daemon is running.
    time.sleep(1)

    # A log file should be generated at start.
    assert os.path.exists(log_path)

    # A pid file should be generated at start.
    assert os.path.exists(pid_path)

    # Stop the test daemon.
    call(['python',
          helper_path,
          pid_path,
          log_path,
          'stop'])


def test_stop(tmpdir):

    # Set up temp file paths.
    test_directory = os.path.dirname(os.path.realpath(__file__))
    temp_directory = str(tmpdir)
    helper_path = os.path.join(test_directory, 'sleepy.py')
    log_path = os.path.join(temp_directory, 'test.log')
    pid_path = os.path.join(temp_directory, 'test.pid')

    # Start the test daemon.
    call(['python',
          helper_path,
          pid_path,
          log_path,
          'start'])

    # Wait a second to make sure the daemon is running.
    time.sleep(1)

    # Stop the test daemon.
    call(['python',
          helper_path,
          pid_path,
          log_path,
          'stop'])

    # Wait a second to make sure the daemon is stopped.
    time.sleep(1)

    # Log file should persist after stop.
    assert os.path.exists(log_path)

    # Pid file should be removed after stop.
    assert not os.path.exists(pid_path)


def test_responds_to_signal(tmpdir):

    # Set up temp file paths.
    test_directory = os.path.dirname(os.path.realpath(__file__))
    temp_directory = str(tmpdir)
    helper_path = os.path.join(test_directory, 'sleepy.py')
    log_path = os.path.join(temp_directory, 'test.log')
    pid_path = os.path.join(temp_directory, 'test.pid')

    # Start the test daemon.
    call(['python',
          helper_path,
          pid_path,
          log_path,
          'start'])

    # Wait a second to make sure the daemon is running.
    time.sleep(1)

    # Stop the test daemon.
    with open(pid_path, 'r') as pidfile:

        os.kill(int(pidfile.read()), signal.SIGTERM)

    # Wait a second to make sure the daemon is stopped.
    time.sleep(1)

    # Log file should persist after stop.
    assert os.path.exists(log_path)

    # Pid file should be removed after stop.
    assert not os.path.exists(pid_path)
