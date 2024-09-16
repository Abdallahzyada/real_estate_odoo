from odoo import fields, models

class Building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'no'

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()

