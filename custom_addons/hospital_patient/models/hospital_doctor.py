from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Bác sĩ'

    name = fields.Char(string='Tên bác sĩ', required=True)
    phone = fields.Char(string='Số điện thoại')
    birth_date = fields.Date(string='Ngày sinh')
    age = fields.Integer(string='Tuổi', compute='_compute_age', store=True)
    specialization = fields.Char(string='Chuyên môn')
    status = fields.Selection([
        ('active', 'Đang làm việc'),
        ('on_leave', 'Đang nghỉ'),
        ('inactive', 'Không còn làm việc'),
    ], string='Trạng thái', default='active')
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string='Danh sách bệnh nhân')

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone:
                digits = ''.join(ch for ch in record.phone if ch.isdigit())
                if len(digits) != 10:
                    raise ValidationError('Số điện thoại bác sĩ phải có đúng 10 chữ số.')

    @api.constrains('birth_date')
    def _check_birth_date(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.birth_date and record.birth_date > today:
                raise ValidationError('Ngày sinh không thể lớn hơn ngày hiện tại.')

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.birth_date:
                birth_date = fields.Date.from_string(record.birth_date)
                current_date = fields.Date.from_string(today)
                age = current_date.year - birth_date.year
                if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
                    age -= 1
                record.age = age
            else:
                record.age = 0

    def action_set_active(self):
        self.status = 'active'

    def action_set_on_leave(self):
        self.status = 'on_leave'

    def action_set_inactive(self):
        self.status = 'inactive'