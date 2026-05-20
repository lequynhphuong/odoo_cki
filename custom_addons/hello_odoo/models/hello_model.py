from odoo import models, fields
class HelloOdoo (models.Model):
    _name = 'hello.odoo'
    _description = 'Hello Odoo Model'
    
    name = fields.Char(string='Ten', required=True, default='Hello Odoo')