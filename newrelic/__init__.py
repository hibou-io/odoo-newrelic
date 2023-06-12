import os
from . import controllers
from odoo.tools import config

import logging 
_logger = logging.getLogger(__name__)


def initialization():
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
        nr_app = newrelic.agent.WSGIApplicationWrapper(target.app)
        target.app = nr_app

        # Workers new WSGI Application
        target = odoo.service.wsgi_server
        target.application_unproxied = newrelic.agent.WSGIApplicationWrapper(target.application_unproxied)
        
        try:
            _logger.info('attaching to bus controller')
            import odoo.addons.bus.controllers.main
            newrelic.agent.wrap_background_task(odoo.addons.bus.controllers.main, 'BusController._poll', application=nr_app)
            _logger.info('finished attaching to bus controller')
        except Exception as e:
            _logger.exception(e)
        
        # Additional configurable hooks
        # Can be comma separated like
        # odoo.models.BaseModel:public,odoo.other.Something:limited
        nr_odoo_trace = os.environ.get('NEW_RELIC_ODOO_TRACE', config.get('new_relic_odoo_trace'))
        # will default to a limited set
        if nr_odoo_trace is None:
            # it is None because it got a default, lets provide one
            nr_patches = ['odoo.models.BaseModel:limited']
        else:
            # the user specified, so they may intend for it to be unset
            nr_patches = nr_odoo_trace.strip().split(',')
        try:
            _logger.info('Applying Tracing to %s' % (nr_patches))
            for patch in nr_patches:
                patch_base, patch_type = patch.split(':')
                _module = None
                _paths = []
                if patch_base == 'odoo.models.BaseModel':
                    import odoo.models
                    _module = odoo.models
                    if patch_type == 'all':
                        _paths += ['BaseModel.%s' % (func, ) for func in dir(odoo.models.BaseModel) if callable(getattr(odoo.models.BaseModel, func)) and not func.startswith("__")]
                    elif patch_type == 'public':
                        _paths += ['BaseModel.%s' % (func, ) for func in dir(odoo.models.BaseModel) if callable(getattr(odoo.models.BaseModel, func)) and not func.startswith("_")]
                    elif patch_type == 'limited':
                        _paths += [
                            # CRUD
                            'BaseModel.create',
                            'BaseModel.read',
                            'BaseModel.read_group',
                            'BaseModel.write',
                            'BaseModel.unlink',
                            # Search
                            'BaseModel.search',
                            'BaseModel.search_read',
                            'BaseModel.search_count',
                        ]
                if _module:
                    for path in _paths:
                        newrelic.agent.wrap_function_trace(_module, path)
        except Exception as e:
            _logger.exception(e)
                    
        
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


try:
    # the Odoo server will stop after its initialization, server will not be available for monkey-patching
    if not config.get("stop_after_init"):
        initialization()

except ImportError:
    _logger.warn('newrelic python module not installed or other missing module')
