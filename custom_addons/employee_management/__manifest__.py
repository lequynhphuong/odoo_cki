{
    'name': 'Employee Management',          
    'version': '1.0',     
    'category': 'Custom',    
    'summary': 'Module quản lý nhân viên',
    'author': 'Phuong Le',
    'depends': ['base'],                
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',  
        'views/employee_menu.xml',
    ],
    'installable': True,
    'application': True,
}