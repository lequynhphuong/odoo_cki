{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Quản lý bệnh viện',
    'author': 'Auto Generated',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/doctor_views.xml',
    ],
    'installable': True,
    'application': True,
}
