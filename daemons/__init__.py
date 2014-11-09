"""This package contains base classes for creating Python daemons.

These daemon implementations are a modification of work performed by Sander
Marechal. Sander's original work can be found at
http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/.

Modifications to the original include:

-   Unix signal handling to provide process cleanup.
-   Updated Python syntax.
-   Integration of Python 'logging' module.
-   Organization of code into modules
-   Specialized extensions for different workflows
-   Integration of green-threads (eventlet and gevent)
"""
