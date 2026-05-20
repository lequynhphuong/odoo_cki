{
    'name': 'Library Portal',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Library management portal for website visitors',
    'description': 'A module to manage books and allow visitors to view books and register loans via forms and JSON API.',
    'author': 'Phuong Le',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'data/demo_data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
}