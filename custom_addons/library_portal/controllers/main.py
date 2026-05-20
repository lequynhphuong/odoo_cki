# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import re

class LibraryPortalController(http.Controller):

    @http.route('/library/books', type='http', auth='public', website=True)
    def list_books(self, **kwargs):
        books = request.env['library.book'].sudo().search([('state', '=', 'available')])
        return request.render('library_portal.book_list', {'books': books})

    @http.route('/library/book/<int:book_id>', type='http', auth='public', website=True)
    def book_detail(self, book_id, **kwargs):
        book = request.env['library.book'].sudo().browse(book_id)
        if not book.exists():
            return request.not_found()
        return request.render('library_portal.book_detail', {'book': book})

    @http.route('/library/borrow/<int:book_id>', type='http', auth='public', website=True, methods=['GET'])
    def borrow_form(self, book_id, **kwargs):
        book = request.env['library.book'].sudo().browse(book_id)
        if not book.exists():
            return request.not_found()
        return request.render('library_portal.borrow_form', {
            'book': book,
            'errors': {},
            'values': {}
        })

    @http.route('/library/borrow/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def submit_borrow(self, **kwargs):
        book_id = kwargs.get('book_id')
        name = kwargs.get('name', '').strip()
        email = kwargs.get('email', '').strip()
        phone = kwargs.get('phone', '').strip()

        errors = {}
        if not name:
            errors['name'] = 'Tên không được để trống'
        if not email or '@' not in email:
            errors['email'] = 'Email phải chứa ký tự @'

        book = request.env['library.book'].sudo().browse(int(book_id)) if book_id else None
        if not book or not book.exists():
            return request.not_found()

        if errors:
            return request.render('library_portal.borrow_form', {
                'book': book,
                'errors': errors,
                'values': {'name': name, 'email': email, 'phone': phone}
            })

        # Tạo borrow request
        borrow_request = request.env['library.borrow.request'].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'book_id': book.id,
        })

        return request.redirect('/library/borrow/thank-you?id=%s' % borrow_request.id)

    @http.route('/library/borrow/thank-you', type='http', auth='public', website=True)
    def thank_you(self, **kwargs):
        request_id = kwargs.get('id')
        borrow_request = request.env['library.borrow.request'].sudo().browse(int(request_id)) if request_id else None
        if not borrow_request.exists():
            return request.not_found()
        return request.render('library_portal.thank_you', {'borrow_request': borrow_request})

    # JSON APIs
    @http.route('/api/library/books', type='json', auth='public')
    def api_books(self):
        books = request.env['library.book'].sudo().search([('state', '=', 'available')])
        data = []
        for book in books:
            data.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'quantity': book.quantity,
            })
        return {'books': data}

    @http.route('/api/library/borrow', type='json', auth='public', methods=['POST'])
    def api_borrow(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        book_id = kwargs.get('book_id')

        if not name or not email or not book_id:
            return {'success': False, 'error': 'Missing required fields'}

        book = request.env['library.book'].sudo().browse(int(book_id))
        if not book.exists():
            return {'success': False, 'error': 'Book not found'}
        if book.quantity <= 0:
            return {'success': False, 'error': 'Book not available'}

        borrow_request = request.env['library.borrow.request'].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'book_id': book.id,
        })
        return {'success': True, 'request_id': borrow_request.id}

    @http.route('/api/library/my-requests', type='json', auth='user')
    def api_my_requests(self):
        user_email = request.env.user.email
        if not user_email:
            return {'requests': []}
        requests = request.env['library.borrow.request'].search([('email', '=', user_email)])
        data = []
        for req in requests:
            data.append({
                'id': req.id,
                'name': req.name,
                'email': req.email,
                'phone': req.phone,
                'book_name': req.book_id.name,
                'request_date': req.request_date,
                'state': req.state,
            })
        return {'requests': data}