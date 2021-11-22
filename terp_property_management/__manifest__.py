{
    'name': 'Property Management',
    'version': '15.0.1.0.0',
    'summary': 'Property Management System',
    'description': 'Odoo15 Property Management System,Odoo15 Realestate, Property Mangement, Odoo 15',
    'category': 'Industries',
    'author': 'TecbotERP',
    'website': "https://techboterp.com",
    'company': 'TechbotErP',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'crm',
        'account',
        'sale_management',
        'stock',

    ],
    'data': [

        'views/property_details_view.xml',

        'security/ir.model.access.csv'

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
