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
from random import randint


def _get_default_color(self):
    return randint(1, 11)


# Room Bed Space Type/Category
class BedSpaceBirthType(models.Model):
    _name = "birth.type"
    _description = "Bed space Category details"

    name = fields.Char()


# Room Partition Types Details
class RoomPartitionType(models.Model):
    _name = "room.partition.type"
    _description = "Room Partition Type"

    name = fields.Char()


class InheritProduct(models.Model):
    _inherit = 'product.template'

    floor_id = fields.Many2one('floor.details')


# Building Floor Details
class PropertyFloorDetails(models.Model):
    _name = "floor.details"
    _description = "Floor Details"

    name = fields.Char('name')
    apartment_ids = fields.One2many('product.template', 'floor_id',string='Apartment')


# Room  Furniture Details
class RoomFurniture(models.Model):
    _name = "room.furniture"
    _description = "Room Furniture"

    color = fields.Integer('Color', default=_get_default_color)
    name = fields.Char()


# Room Electronics Details
class RoomElectronics(models.Model):
    _name = "room.electronics"
    _description = "Room Electronics Details"
    color = fields.Integer('Color', default=_get_default_color)
    name = fields.Char()


# Room Equipment Details
class RoomEquipments(models.Model):
    _name = "room.equipment.details"
    _description = "Rooms Equipments"

    color = fields.Integer('Color', default=_get_default_color)
    name = fields.Char()
