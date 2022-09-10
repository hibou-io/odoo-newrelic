
from odoo import http, tools

try:
    if tools.config['debug_mode']:
        class TestErrors(http.Controller):
            @http.route('/test_errors_404', auth='public')
            def test_errors_404(self):
                import werkzeug
                return werkzeug.exceptions.NotFound('Successful test of 404')

            @http.route('/test_errors_500', auth='public')
            def test_errors_500(self):
                raise ValueError
except KeyError:
    pass
