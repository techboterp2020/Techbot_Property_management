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
###############################################################################

from odoo import api, fields, models, api, _
from random import randint
# from odoo.exceptions import ValidationError


# Function for Take random number for set Color for any2many widget
def _get_default_color(self):
    return randint(1, 11)


class RoomKitchen(models.Model):
    _name = 'room.kitchen.details'
    _description = "Kitchen Dtails"

    name = fields.Char()
    equipment_ids = fields.Many2many('room.equipment.details', 'room_kitchen_equipment_rel')
    electronics_ids = fields.Many2many('room.electronics', 'room_kitchen_electronics_rel')
    furniture_ids = fields.Many2many('room.furniture', 'room_kitchen_furniture_rel')


class RoomToilet(models.Model):
    _name = 'room.toilet.details'
    _description = "Toilet Details"

    name = fields.Char()
    equipment_ids = fields.Many2many('room.equipment.details', 'room_toilet_equipment_rel')
    electronics_ids = fields.Many2many('room.electronics', 'room_toilet_electronics_rel')
