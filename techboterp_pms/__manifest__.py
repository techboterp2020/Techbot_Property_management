{
    'name': 'Property Management',
    'version': '15.1.8.0',
    'summary': 'Property Management System',
    'description': 'Odoo15 Property Management System,Odoo15 Real estate, Property Management, Odoo 15',
    'category': 'Industries',
    'author': 'TecbotERP',
    'website': "https://techboterp.com",
    'company': 'TechbotErP',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': -10,
    'depends': [
        'base',
        'stock',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/property_management_system_views.xml',
        'views/property_apartment_type_views.xml',
        'views/floor_details_views.xml',
        'views/bed_space_type_views.xml',
        'views/room_partition_type_views.xml',
        'views/room_kitchen_details_views.xml',
        'views/room_toilet_details_views.xml',
        'views/property_management_menu.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
