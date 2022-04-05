# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

from odoo import fields, models, tools


class RentalReportInherit(models.Model):
    _inherit = "sale.rental.report"
    _description = "Rental Analysis Report Inherit"


    # For Geting Report
    is_room = fields.Boolean('Rooms',related='order_id.is_room')  # For Rooms
    is_partition = fields.Boolean('Partition', related='order_id.is_partition')  # For Rooms
    is_bed_space = fields.Boolean('Bed Space', related='order_id.is_bed_space')  # For Rooms


