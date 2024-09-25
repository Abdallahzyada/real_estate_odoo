from odoo import fields,models

class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    reason = fields.Text()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], default='draft')

    def action_confirm(self):
        if self.property_id.state == 'close':
            self.property_id.state = self.state
            self.property_id.create_history_record('close', self.state, self.reason)