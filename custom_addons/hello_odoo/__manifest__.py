{
    'name': 'Hello Odoo',
    'version': '19.0.1.0',        
    'author': 'Phuong Le',
    'category': 'Custom',
    'summary': 'Module hien thi Hello Odoo',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/hello_view.xml',
        'views/hello_menu.xml',
    ],
    'installable': True,
    'application': True,
}