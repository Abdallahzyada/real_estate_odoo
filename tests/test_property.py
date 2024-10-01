from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_01_record = self.env['property'].create({
            'ref':'PRT00000012',
            'name': 'test case 1',
            'description': 'desc',
            'post_code': '12345',
            'date_availability': fields.date.today(),
            'expected_selling_date': fields.date.today(),
            'expected_price': 15000000.00,
            'selling_price': 13000000.00,
            'bedrooms': 3

        })

    def test_01_property_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(property_id, [{
            'ref': 'PRT00000016',
            'name': 'test case 1',
            'description': 'desc',
            'post_code': '12345',
            'date_availability': fields.date.today(),
            'expected_selling_date': fields.date.today(),
            'expected_price': 15000000.00,
            'selling_price': 13000000.00,
            'bedrooms': 3
        }])