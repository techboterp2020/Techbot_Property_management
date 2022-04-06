# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: TechbotErp(<https://techboterp.com/>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE , Version v1.0
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'PMS Product Master',
    'version': '15.0.3.2.5',
    'summary': 'To Create Property Product Master',
    'description': 'Odoo15 Property Management System,Odoo15 Real estate, Property Management, Odoo 15',
    'category': 'Industries',
    'author': 'TecbotERP',
    'website': "https://techboterp.com",
    'company': 'TechbotErP',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': -10,
    'depends': [
        'base', 'techboterp_pms', 'sale_renting', 'stock'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/room_bedspace_details_views.xml',
        'views/room_partition_details_views.xml',
        'views/room_details_views.xml',
        'views/apartment_master_details_views.xml',
        'views/property_overview.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'techboterp_product_master_custom/static/src/scss/productoverview.scss',
        ],
    },
}
