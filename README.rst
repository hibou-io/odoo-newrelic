*********************************
New Relic Instrumentation for Odoo
*********************************


Someone tells you, "Hey your site is being *slow* right now."
What do you do?  Restart Odoo? Look at Nginx access logs?  Could it be PostgreSQL?
We've all been there...

===========
Get Started
===========

1) Install the newrelic python package through pip or from source:

```
pip3 install newrelic
```

2) Create a newrelic.ini file `New Relic Python Quick Start <https://docs.newrelic.com/docs/agents/python-agent/getting-started/python-agent-quick-start>`_ (you can skip if you'd rather use ENV variable, see (3) from below):

```
newrelic-admin generate-config YOUR_LICENSE_KEY /etc/odoo-newrelic.ini
```

3) Add this module to your existing addons folder or create a new addons folder and add it to the Odoo addons path.
4) Make sure that Odoo loads and uses your New Relic details which are usually set in a New Relic configuration file.
Add the New Relic configuration file to your **odoo-server.conf** file:

```
new_relic_config_file = /etc/odoo-newrelic.ini
```

Optionally you can set environment variables for the whole New Relic configuration. See `New Relic Python Agent Configuration <https://docs.newrelic.com/docs/agents/python-agent/installation-configuration/python-agent-configuration#environment-variables>`_

5) Restart your odoo process and install the 'newrelic' module in Odoo Apps. (You may need to restart your odoo server again and look at the logs for information about a misconfiguration or missing modules.)

========
Features
========

* Web errors (like 404's) are not treated as errors.
* Server errors (like 500's) are caught and show up in the Errors area.
* Transactions are named by route.
* PostgreSQL and Python metrics are easily visible.
* Front end page metrics (page rendering) is enabled by default. (only on the front end)
* Works in threaded (workers=0) and multi process (workers>0) modes.

.. image:: https://cloud.githubusercontent.com/assets/744550/16216646/51bb121e-3721-11e6-86de-8e0f728adc93.png
    :alt: 'Main'
    :width: 988
    :align: left

.. image:: https://cloud.githubusercontent.com/assets/744550/16216648/56763590-3721-11e6-89f4-9843ad216572.png
    :alt: 'Transactions'
    :width: 988
    :align: left

.. image:: https://cloud.githubusercontent.com/assets/744550/16216650/5ef7f2b2-3721-11e6-93e3-5f53b76775f9.png
    :alt: 'Browser'
    :width: 988
    :align: left

.. image:: https://cloud.githubusercontent.com/assets/744550/16216733/210d5da6-3722-11e6-9d10-5c928d235ff1.png
    :alt: 'Errors'
    :width: 988
    :align: left

.. image:: https://cloud.githubusercontent.com/assets/744550/16216737/264dea6a-3722-11e6-9265-d1034b1fc0db.png
    :alt: 'Error Detail'
    :width: 988
    :align: left



Known Issues
============

* Due to the nature of /longpolling, this transaction is ignored on purpose. (feature?)
* Background tasks are not profiled.
* Could probably use better transaction naming.

=======
Licence
=======

Please see `LICENSE <https://github.com/hibou-io/odoo-newrelic/blob/master/LICENSE>`_.

Copyright Hibou Corp. 2020. This module was not sponsored in any way by New Relic, I just happen to like profiling.
