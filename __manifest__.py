{
    'name': 'Real Estate',
    'technical_name': 'real_estate',
    'description': 'a simple app',
    'author': 'abdallah zyada',
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'contacts', 'mail', 'account', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/sale_order_view.xml',
        'views/building_view.xml',
    ],
    'application': True
}