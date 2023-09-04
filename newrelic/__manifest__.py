{
    'name': 'NewRelic Instrumentation',
    'description': 'Wraps requests etc.',
    'version': '16.0.0.9.0',
    'website': 'https://hibou.io/',
    'author': 'Hibou Corp. <hello@hibou.io>',
    'license': 'AGPL-3',
    'category': 'Tool',
    'depends': [
        'web',
    ],
    'external_dependencies': {
        "python": ["newrelic"],
    },    
    "installable": True,
    "application": False,
}
