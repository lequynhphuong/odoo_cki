# -*- coding: utf-8 -*-

from odoo import models, fields

class LibraryBorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Library Borrow Request'

    name = fields.Char(string='Tên người mượn')
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    book_id = fields.Many2one('library.book', string='Book', required=True)
    request_date = fields.Datetime(string='Request Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ], string='State', default='draft')