from odoo import models, fields

class Property(models.Model):
    _name = 'property'

    name = fields.Char()
    description = fields.Text()
    post_code = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('east', 'East'),
        ('north', 'Nort'),
        ('south', 'South'),
        ('west', 'West')]
    )