# -*- encoding: UTF-8 -*-
from . import controllers

import logging 
_logger = logging.getLogger(__name__)

try:
    import odoo
    target = odoo.service.server.server
    if not target:
        # we started too early, probably because of a server wide module issue...
        _logger.error('Cannot run newrelic as a server wide module because it needs to patch the running server.')

    try:
        instrumented = target._nr_instrumented
    except AttributeError as e:
        instrumented = target._nr_instrumented = False

    if instrumented:
        _logger.info("NewRelic instrumented already")
    else:
        import odoo.tools.config as config
        import newrelic.agent


        try:
            newrelic.agent.initialize(config['new_relic_config_file'], config['new_relic_environment'])
        except KeyError:
            try:
                newrelic.agent.initialize(config['new_relic_config_file'])
            except KeyError:
                _logger.info('NewRelic setting up from env variables')
                newrelic.agent.initialize()

        # Main WSGI Application
        target._nr_instrumented = True
        target.app = newrelic.agent.WSGIApplicationWrapper(target.app)

        # Workers new WSGI Application
        target = odoo.service.wsgi_server
        target.application_unproxied = newrelic.agent.WSGIApplicationWrapper(target.application_unproxied)

        # Error handling
        def status_code(exc, value, tb):
            from werkzeug.exceptions import HTTPException

            # Werkzeug HTTPException can be raised internally by Odoo or in
            # user code if they mix Odoo with Werkzeug. Filter based on the
            # HTTP status code.

            if isinstance(value, HTTPException):
                return value.code

        def _nr_wrapper_handle_exception_(wrapped):
            def _handle_exception(*args, **kwargs):
                transaction = newrelic.agent.current_transaction()

                if transaction is None:
                    return wrapped(*args, **kwargs)

                transaction.notice_error(status_code=status_code)

                name = newrelic.agent.callable_name(args[1])
                with newrelic.agent.FunctionTrace(transaction, name):
                    return wrapped(*args, **kwargs)

            return _handle_exception

        target = odoo.http.WebRequest
        target._handle_exception = _nr_wrapper_handle_exception_(target._handle_exception)


except ImportError:
    _logger.warn('newrelic python module not installed or other missing module')