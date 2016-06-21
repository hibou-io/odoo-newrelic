*********************************
NewRelic Instrumentation for Odoo
*********************************


Someone tells you, "Hey your site is being *slow* right now."

What do you do?  Restart Odoo? Look at Nginx access logs?  Could it Postgres?

We've all been there...

========
Features
========

* Web errors (like 404's) are not treated as errors.
* Server errors (like 500's) are caught and show up in the Errors area.
* Transactions are named by route.
* Postgres and Python metrics are easily visible.
* Front end page metrics (page rendering) is enabled by default. (only on the front end)
* Works in threaded (workers=0) and multi process (workers>0) modes.


===========
Get Started
===========

1) Install the newrelic python package through pip or from source.
2) Create a newrelic.ini file `NewRelic Python Quick Start <https://docs.newrelic.com/docs/agents/python-agent/getting-started/python-agent-quick-start>`_ (you can skip if you'd rather use ENV variable, see (3) from below)
3) Install this module into your addons folder, or add it to your Odoo addons path.

Now you need a way to load your NewRelic LICENSE KEY (usually via the newrelic.ini) file.

1) add something like this to your **openers-server.conf** file: *new_relic_config_file = /etc/odoo/newrelic.ini*  (you can also set *new_relic_environment = staging* , or some other environment in your Odoo configuration)
2) set an environment variable: *NEW_RELIC_CONFIG_FILE=/etc/odoo/newrelic.ini*
3) set environment variables for the whole NewRelic configuration. See `NewRelic Python Agent Configuration <https://docs.newrelic.com/docs/agents/python-agent/installation-configuration/python-agent-configuration#environment-variables>`_

Restart your odoo process and install the 'newrelic' module in Odoo Apps. (You may need to restart your odoo server again and look at the logs for information on misconfiguration or missing modules.)



Known Issues
============

* Due to the nature of /longpolling, this transaction is ignored on purpose. (feature?)
* Background tasks are not profiled.
* Could probably use better transaction naming.


Docker
======

Want to test this module out, but don't have gevent and newrelic installed?  I've got a Docker image for you!
`hibou/odoo:9.0 <https://hub.docker.com/r/hibou/odoo/>`_

=======
Licence
=======

Please see `LICENSE <https://github.com/hibou-io/odoo-newrelic/blob/master/LICENSE>`_.

Copyright Hibou Corp. 2016. This module was not sponsored in any way by NewRelic, I just happen to like profiling.