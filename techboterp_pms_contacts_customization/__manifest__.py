{
    'name': 'PMS Contacts',
    'version': '15.0.2.1.5',
    'summary': 'Property Management System Owner and Tenant Contact Creation',
    'description': 'Odoo15 Property Management System,Odoo15 Realestate, Property Mangement, Odoo 15',
    'category': 'Industries',
    'author': 'TecbotERP',
    'website': "https://techboterp.com",
    'company': 'TechbotErP',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': -10,
    'depends': [
        'base',
        'techboterp_pms',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/res_partner_owner_view.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
