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
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, api, _


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    _description = 'Customization in Purchase Order'

    # Method to Create Owner(customer) in Purchase Order
    @api.model
    def create(self, vals):
        res = super(PurchaseOrderInherit, self).create(vals)
        if res['partner_id']:
            res['partner_id']['is_owner'] = True
        return res

    # method to Edit existing Customer and create new customer its saved in Owner Master
    def write(self, vals):
        res = super(PurchaseOrderInherit, self).write(vals)
        if vals.get('partner_id'):
            obj = self.env['res.partner'].browse(vals.get('partner_id'))
            obj['is_owner'] = True
        return res

