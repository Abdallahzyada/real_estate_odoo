from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, tracking=1, translate=True )
    ref = fields.Char(default='New', readonly='1')
    description = fields.Text(groups="app_one.property_manager_group")
    post_code = fields.Char(required=1, size=6)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    expected_price = fields.Float(tracking=1)
    selling_price = fields.Float(tracking=1)
    diff = fields.Float(compute="_compute_diff", groups="app_one.property_manager_group")
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
    is_late = fields.Boolean()

    _sql_constraints = [('unique_name','unique("name")','This Name Already exists!')]

    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError('Please add a valid number of bedrooms!')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'


    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_close(self):
        for rec in self:
            rec.create_history_record(rec.state, 'close')
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

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                if rec.state != 'sold' or rec.state !='close':
                    rec.is_late = True


    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or '',
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {
            'default_property_id': self.id,
        }
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    #create
    @api.model
    def create(self, vals_list):
        res = super(Property, self).create(vals_list)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res


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