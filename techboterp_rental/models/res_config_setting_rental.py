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

from odoo import api, fields, models, api, _


class RentalResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Res Config Settings Rental '

    module_restrict_sale_renting = fields.Boolean(string="Restrict Zero Qty To Sale")

    @api.model
    def get_values(self):
        res = super(RentalResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        restrict_sale_renting = params.get_param('module_restrict_sale_renting',  default=False)
        res.update(module_restrict_sale_renting=restrict_sale_renting)
        return res

    def set_values(self):
        super(RentalResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            "module_restrict_sale_renting",
            self.module_restrict_sale_renting)
