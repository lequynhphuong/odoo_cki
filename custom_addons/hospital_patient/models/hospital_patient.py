from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Bệnh nhân'

    name = fields.Char(string='Tên bệnh nhân', required=True)
    birth_date = fields.Date(string='Ngày sinh')
    age = fields.Integer(string='Tuổi', compute='_compute_age', store=True)
    disease = fields.Char(string='Bệnh')
    doctor_id = fields.Many2one(
        'hospital.doctor',
        string='Bác sĩ phụ trách',
        ondelete='set null',
    )
    needs_parent = fields.Boolean(string='Cần phụ huynh', compute='_compute_needs_parent', store=True)

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

    @api.depends('age')
    def _compute_needs_parent(self):
        for record in self:
            record.needs_parent = bool(record.age and record.age < 10)

    @api.constrains('name', 'doctor_id')
    def _check_unique_doctor_for_patient(self):
        for record in self:
            if not record.name or not record.doctor_id:
                continue
            duplicate = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id),
                ('doctor_id', '!=', record.doctor_id),
            ], limit=1)
            if duplicate:
                raise ValidationError(
                    'Một bệnh nhân chỉ được đăng ký với một bác sĩ duy nhất.'
                )

    def update_patient_info(self, name=None, birth_date=None, disease=None, doctor_id=None):
        self.ensure_one()
        values = {}
        if name is not None:
            values['name'] = name
        if birth_date is not None:
            values['birth_date'] = birth_date
        if disease is not None:
            values['disease'] = disease
        if doctor_id is not None:
            values['doctor_id'] = doctor_id.id if hasattr(doctor_id, 'id') else doctor_id
        if values:
            self.write(values)
        return self
