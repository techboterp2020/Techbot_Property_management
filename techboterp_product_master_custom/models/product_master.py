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

from odoo import api, fields, models, api, tools, _
from random import randint
from odoo.exceptions import UserError, ValidationError
# from odoo.modules.module import get_module_resource


def _get_default_color(self):
    return randint(1, 11)


class ProductInherit(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(selection_add=[('product', 'Storable Product')], tracking=True,
                                     ondelete={'product': 'set consu'}, default='product')

    is_bed_space = fields.Boolean('Is Bed Space')  # For Bed Space
    is_partition = fields.Boolean('Is Partition')  # For Partition
    is_room = fields.Boolean('Is Room')  # For Rooms
    is_apartment = fields.Boolean('Is Apartment')  # Apartment
    is_qty_updated = fields.Boolean("On Hand Qty Updated")
    color = fields.Integer('Color', default=_get_default_color)

    """ Bed Space Master Details """
    bed_position_id = fields.Many2one('birth.type', string='Bed Type')
    room_id = fields.Many2one('product.template', string="Room Name", domain="[('is_room','=',True)]", tracking=True)

    """ Partition Master Details """
    partition_room_id = fields.Many2one('product.template', string="Room", domain="[('is_room','=',True)]",
                                        tracking=True)
    partition_type_id = fields.Many2one('room.partition.type', string='Partition Type', tracking=True)

    """# Room Details Master #"""
    bed_space_ids = fields.One2many('product.template', 'room_id', domain="[('is_bed_space','=',True)]", tracking=True,
                                    string='Bed Space Name')
    room_partition_ids = fields.One2many('product.template', 'partition_room_id', domain="[('is_partition','=',True)]",
                                         tracking=True, string='Partition details')

    leasing_method = fields.Boolean('is_leasing', default=False)
    leasing_based_on = fields.Selection([('partition', "Partition"), ('bed_space', 'Bed Space')])
    balcony = fields.Selection([("yes", 'Yes'), ('np', 'No')], string="Balcony Available")
    gfa_sqft = fields.Float("GFA(Sqft)")
    gfa_mtr = fields.Float("GFA(m)", compute='_compute_square_meter')


    @api.onchange('gfa_sqft')
    def _compute_square_meter(self):
        for rec in self:
            rec.gfa_mtr = (rec.gfa_sqft / 10.764)

    furniture_ids = fields.Many2many('room.furniture', 'room_furniture_rel', string='Furniture')
    electronics_ids = fields.Many2many('room.electronics', 'room_electronics_rel', string='Electronics')

    """ APARTMENT MASTER """
    apartment_leasing_method = fields.Boolean('is_leasing', default=False)
    apartment_leasing_based_on = fields.Selection([('room', "Rooms")], default='room', string='Leasing Based On')

    # ***********************************************************************************************************
    #  ******** Method to Update On Hand Qty
    def create_onhand_qty(self):
        self.env['stock.quant'].create({
            'product_id': self.product_variant_id.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            # 'location_id': 8,
            'quantity': 1.0,
        })

    @api.model
    def create(self, vals):
        res = super(ProductInherit, self).create(vals)

        # """ Method to Create new Apartment when  create Room  Form view  """
        if res['apartment_id']:
            res['apartment_id']['rent_ok'] = res['apartment_id']['is_apartment'] = True
            res['apartment_id']['sale_ok'] = res['apartment_id']['purchase_ok'] = False
            if not res['apartment_id']['is_qty_updated']:
                res['apartment_id'].create_onhand_qty()
                res['apartment_id']['is_qty_updated'] = True
            if res['is_room']:
                res['apartment_id']['room_ids'] = [(4, res.id)]

        # On room Creation in Bed Space room Form view, set the boolean fields (can be sale, can be purchase, is_room,can be rented)
        if res['room_id']:
            res['room_id']['rent_ok'] = res['room_id']['is_room'] = True
            res['room_id']['sale_ok'] = res['room_id']['purchase_ok'] = False
            if not res['room_id']['is_qty_updated']:
                res['room_id'].create_onhand_qty()  # To Update Room Onhand Qty when create room in Bedspace
                res['room_id']['is_qty_updated'] = True  # Restrict update onhand qty again and again
            if res['room_id']['leasing_based_on'] == 'bed_space':
                res['room_id']['bed_space_ids'] = [(4, res.id)]

        # On room Creation in Partition Form view,  set the boolean fields (can be sale, can be purchase, is_room,can be rented)
        if res['partition_room_id']:
            res['partition_room_id']['rent_ok'] = res['partition_room_id']['is_room'] = True
            res['partition_room_id']['sale_ok'] = res['partition_room_id']['purchase_ok'] = False
            if not res['partition_room_id']['is_qty_updated']:
                res['partition_room_id'].create_onhand_qty()  # To Update Room Onhand Qty when create room in Partition
                res['partition_room_id']['is_qty_updated'] = True
            if res['partition_room_id']['leasing_based_on'] == 'partition':
                res['partition_room_id']['room_partition_ids'] = [(4, res.id)]

        # Method To Update On Hand  Quantity
        if res['is_apartment'] or res['is_room'] or res['is_partition'] or res['is_bed_space']:
            if not res['is_qty_updated']:
                res.create_onhand_qty()
                res['is_qty_updated'] = True

        return res

    # Method to edit Apartment, Room based on
    def write(self, values):
        res = super(ProductInherit, self).write(values)

        # """ Room: Method to Create new Apartment based on  editing apartment field in room Form view  """
        if values.get('apartment_id'):
            obj_apartment = self.browse(values.get('apartment_id'))
            obj_apartment['rent_ok'] = obj_apartment['is_apartment'] = True
            obj_apartment['sale_ok'] = obj_apartment['purchase_ok'] = False
            if not obj_apartment['is_qty_updated']:
                obj_apartment.create_onhand_qty()  # Set Apartment Onhand Qty is 1 when edit Apartment in Room
                obj_apartment['is_qty_updated'] = True
            if obj_apartment['is_room']:
                obj_apartment['room_ids'] = [(4, self.id)]

        # """ Partition : Method to Create new Room based on  editing room field in Partition Form view  """
        if values.get('partition_room_id'):
            obj_room = self.browse(values.get('partition_room_id'))
            obj_room['rent_ok'] = obj_room['is_room'] = True
            obj_room['sale_ok'] = obj_room['purchase_ok'] = False
            if not obj_room['is_qty_updated']:
                obj_room.create_onhand_qty()  # Set Room Onhand Qty is 1 when edit Room in Partition
                obj_room['is_qty_updated'] = True
            if obj_room['is_partition']:
                obj_room['room_partition_ids'] = [(4, self.id)]

        # """ Bed Space :Method to Create new Room based on  editing room field in bedspace Form view  """
        if values.get('room_id'):
            obj_bed_room = self.browse(values.get('room_id'))
            obj_bed_room['rent_ok'] = obj_bed_room['is_room'] = True
            obj_bed_room['sale_ok'] = obj_bed_room['purchase_ok'] = False
            if not obj_bed_room['is_qty_updated']:
                obj_bed_room.create_onhand_qty()  # Set Room Onhand Qty is 1 when edit Room in Bedspace
                obj_bed_room['is_qty_updated'] = True
            if obj_bed_room['is_bed_space']:
                obj_bed_room['bed_space_ids'] = [(4, self.id)]

        return res

    # Restrict to Change is_lease and lease based onChange bed space,partition and Room in ROOM form view
    @api.onchange('leasing_based_on', 'leasing_method')
    def _check_bed_partition_sold(self):
        quotations = []
        # Based onChange Bed Space
        for rec in self.bed_space_ids:
            obj = self.env['sale.order.line'].search([('product_id', '=', rec.product_variant_id.ids[0])])
            for object in obj:
                # To check if any sale quotation  have bed space product
                if object.order_id.rental_status in ['draft',
                                                     'cancel'] and not object.order_id.rental_status == 'returned':
                    if object.order_id.name not in quotations:
                        quotations.append(object.order_id.name)
                if object.order_id.rental_status in ['pickup',
                                                     'return'] and not object.order_id.rental_status == 'returned':
                    raise UserError(
                        _("Please Don't Change Leasing Method, Currently The Bed space is Running and Confirmed sale order are %s",
                          quotations))

        # Onchange Partition
        for rec in self.room_partition_ids:
            obj = self.env['sale.order.line'].search([('product_id', '=', rec.product_variant_id.ids[0])])
            for object in obj:
                if object.order_id.rental_status in ['draft',
                                                     'cancel'] and not object.order_id.rental_status == 'returned':
                    if object.order_id.name not in quotations:
                        quotations.append(object.order_id.name)
                if object.order_id.rental_status in ['pickup',
                                                     'return'] and not object.order_id.rental_status == 'returned':
                    raise UserError(
                        _("Please Don't Change Leasing Method, Currently the Partition is Running and Confirmed sale order are %s",
                          quotations))

        # Onchange Based on is for leasing False
        for rec in self:
            obj = self.env['sale.order.line'].search([('product_id', '=', rec.product_variant_id.id)])
            for object in obj:
                if object.order_id.rental_status in ['draft',
                                                     'cancel'] and not object.order_id.rental_status == 'returned':
                    if object.order_id.name not in quotations:
                        quotations.append(object.order_id.name)
                if object.order_id.rental_status in ['pickup',
                                                     'return'] and not object.order_id.rental_status == 'returned':
                    raise UserError(_("Please Don't Change, Currently The Room is Running."))

        # List Out the Draft Stage Quotation when leasing method changing time
        if quotations:
            raise UserError(_("Please Don't Change Leasing Method,Please Check the Quotations are %s", quotations))

    """
        TO CHANGE THE KANBAN VIEW Background Color Based On  QTY AVAILABILITY
        if the on hand qty is zero the kanban view shows as red
        and ON HAND qty is 1 then kanban view as Green
    """
    product_kanban_color = fields.Integer(string='Color Index', compute='_compute_color')

    @api.depends('qty_available')
    def _compute_color(self):
        for product in self:
            product.product_kanban_color = 0
            """ Background Color Changes Based on the Stages in Kanban View
                    if the deadline is overdue the background color changed to Red
                    and the stage is closed then the background color red changed to white    """
            if product.qty_available == 1:
                product.product_kanban_color = 10
            else:
                product.product_kanban_color = 6
