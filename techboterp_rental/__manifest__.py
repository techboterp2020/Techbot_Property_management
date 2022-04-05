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
    'name': 'Techboterp PMS Rental Custom module',
    'version': '15.1.2.8',
    'summary': 'To Create Rental',
    'description': 'Odoo15 Property Management System,Odoo15 Real estate, Property Management, Odoo 15',
    'category': 'Industries',
    'author': 'TecbotERP',
    'website': "https://techboterp.com",
    'company': 'TechbotErP',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': -10,
    'depends': [
        'base', 'techboterp_pms', 'sale_renting',
        'techboterp_product_master_custom',
        'techboterp_pms_contacts_customization'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_setting_rental_views.xml',
        'views/rental_sale_order_views.xml',
        'views/rental_report_views.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
