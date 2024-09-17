from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, tracking=1)
    description = fields.Text()
    post_code = fields.Char(required=1, size=6)
    date_availability = fields.Date(tracking=1)
    expected_price = fields.Float(tracking=1)
    selling_price = fields.Float(tracking=1)
    diff = fields.Float(compute="_compute_diff")
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
        ('west', 'West')],
        default='east',
        tracking=1
    )
    owner_id = fields.Many2one('owner', tracking=1)
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')
    state = fields.Selection([
        ('draft', "Draft"),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('close', 'Closed')
    ],default='draft')

    line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)

    _sql_constraints = [('unique_name','unique("name")','This Name Already exists!')]

    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError('Please add a valid number of bedrooms!')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'


    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    def action_close(self):
        for rec in self:
            rec.state = 'close'

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                return {
                    'warning': {'title':'warning', 'message':'Negative Number'}
                }

    # #create
    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(Property, self).create(vals_list)
    #     #logic
    #     return res
    # #write
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     #logic
    #     return res
    #
    # #update
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     #logic
    #     return res
    #
    # #delete
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     #logic
    #     return res


class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')