{
    'name': 'NewRelic Instrumentation',
    'description': 'Wraps requests etc.',
    'version': '1.1',
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
