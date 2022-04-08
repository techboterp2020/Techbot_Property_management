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
# from odoo.exceptions import UserError, Warning
from odoo.exceptions import Warning, UserError


class RentalSaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    _description = 'Rental Sale Order '

    rental_status = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('pickup', 'Confirmed'),
        ('return', 'Rented'),
        ('returned', 'Returned'),
        ('cancel', 'Cancelled'),
    ], string="Rental Status", compute='_compute_rental_status', store=True)

    rent_by = fields.Selection(
        [('apartment', 'Apartment'), ('room', 'Room'), ('partition', 'Partition'), ('bed_space', 'Bed Space'),
         ('bed_partition', 'Bed and Partition')])
    apartment_ids = fields.Many2many('product.template', 'sale_order_apartment_rel', string="Apartment Name",
                                     domain="[('is_apartment','=',True)]")

    room_ids = fields.Many2many('product.template', 'sale_order_rooms_rel', string="Room Name",
                                domain="[('is_room','=',True)]")
    rental_based_on = fields.Selection([('partition', "Partition"), ('bed_space', 'Bed Space')],
                                       related='room_ids.leasing_based_on')
    is_apartment = fields.Boolean('Is Apartment')
    is_room = fields.Boolean('Is Room')
    is_partition = fields.Boolean('Is Partition')
    is_bed_space = fields.Boolean('Is Bed')
    is_bed_partition = fields.Boolean('Is Bed and Partition')

    @api.onchange('rent_by')
    def onchange_rentby(self):
        for rec in self:
            rec.apartment_ids = rec.room_ids = rec.order_line = rec.is_apartment = rec.is_room = rec.is_bed_space = rec.is_partition = rec.is_bed_partition = False

            if rec.rent_by == 'apartment':
                rec.is_apartment = True
            #
            #             if rec.rent_by == 'room':
            #                 rec.is_room = True
            #                 return {'domain': {'apartment_ids': [('is_apartment', '=', True), ('apartment_leasing_method', '=', True),
            #                                                 ('apartment_leasing_based_on', '=', 'room')]}}

            if rec.rent_by == 'room':
                rec.is_room = True
                # return {'domain':{'apartment_ids':[('is_apartment', '=', True), ('apartment_leasing_method', '=', True)]}}

            if rec.rent_by == 'bed_space':
                rec.is_bed_space = True
                return {'domain': {'room_ids': [('is_room', '=', True), ('leasing_method', '=', True),
                                                ('leasing_based_on', '=', 'bed_space')]}}
            if rec.rent_by == 'partition':
                rec.is_partition = True
                return {'domain': {'room_ids': [('is_room', '=', True), ('leasing_method', '=', True),
                                                ('leasing_based_on', '=', 'partition')]}}

            if rec.rent_by == 'bed_partition':
                rec.is_bed_partition = True
                return {'domain': {'room_ids': [('is_room', '=', True), ('leasing_method', '=', True),
                                                ('leasing_based_on', 'in', ['bed_space', 'partition'])]}}

    # Method to Create Tenant(customer) in Sale Order
    @api.model
    def create(self, vals):
        res = super(RentalSaleOrderInherit, self).create(vals)
        if res['partner_id']:
            res['partner_id']['is_tenant'] = True
        return res

    # method to Edit existing Customer and create new customer its save in Tenant Master
    def write(self, vals):
        res = super(RentalSaleOrderInherit, self).write(vals)
        if vals.get('partner_id'):
            obj = self.env['res.partner'].browse(vals.get('partner_id'))
            obj['is_tenant'] = True
        return res

    # Restrict to Sale Rental Product when Restrict Zero Qty To Sale boolean is True
    def action_confirm(self):
        res = super(RentalSaleOrderInherit, self).action_confirm()
        restrict_confirm = self.env['ir.config_parameter'].sudo().get_param('module_restrict_sale_renting', False)
        if restrict_confirm == 'True':
            for rec in self.order_line:
                if rec.product_id.qty_available <= 0:
                    raise UserError(_("Already This Product is Allocated!. Please Check it."))
        return res

    def open_pickup(self):
        restrict_confirm = self.env['ir.config_parameter'].sudo().get_param('module_restrict_sale_renting', False)
        if restrict_confirm == 'True':
            for rec in self.order_line:
                if rec.product_id.qty_available <= 0:
                    raise UserError(_("Already This Product is Allocated !. Please Check it."))
        return super(RentalSaleOrderInherit, self).open_pickup()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_apartment = fields.Boolean('Is Room', related='product_id.is_apartment')
    is_room = fields.Boolean('Is Room', related='product_id.is_room')
    is_partition = fields.Boolean('Is Partition', related='product_id.is_partition')
    is_bed_space = fields.Boolean('Is Bed', related='product_id.is_bed_space')

    @api.onchange('is_rental')
    def on_change_is_rental(self):
        """Restrict to Show Products When the module_restrict_sale_renting boolean is True. or
        Prevent to show zero Qty Product in Sale Order Line(Prevent the product based on the restriction in Sale Order line)
        and only show product based on Apartment Name  and Room Name"""

        restrict_product = self.env['ir.config_parameter'].sudo().get_param('module_restrict_sale_renting', False)
        for rec in self:
            if rec.order_id and rec.order_id.is_apartment:
                domain = [('is_apartment', '=', True), ('apartment_leasing_method', '!=', True)]
                if restrict_product == 'True':
                    return {'domain': {'product_id': [('is_apartment', '=', True), ('apartment_leasing_method', '!=', True),
                                                      ('qty_available', '!=', 0)]}}
                else:
                    return {'domain': {'product_id': domain}}

            if rec.order_id and rec.order_id.is_room:
                domain = [('is_room', '=', True), ('leasing_method', '!=', True)]
                if restrict_product == 'True':
                    return {'domain': {'product_id': [('apartment_id', '=', rec.order_id.apartment_ids.ids), ('qty_available', '!=', 0)]}}
                    # return {'domain': {'product_id': [('is_room', '=', True), ('leasing_method', '!=', True),
                    #                                   ('qty_available', '!=', 0)]}}
                else:
                    # return {'domain': {'product_id': domain}}
                    return {'domain': {'product_id': [('apartment_id', '=', rec.order_id.apartment_ids.ids)]}}

            if rec.order_id and rec.order_id.is_partition:
                if restrict_product == 'True':
                    return {'domain': {'product_id': [('partition_room_id', '=', rec.order_id.room_ids.ids),
                                                      ('qty_available', '!=', 0)]}}
                else:
                    return {'domain': {'product_id': [('partition_room_id', '=', rec.order_id.room_ids.ids)]}}

            if rec.order_id and rec.order_id.is_bed_space:
                if restrict_product == 'True':
                    return {'domain': {
                        'product_id': [('room_id', '=', rec.order_id.room_ids.ids), ('qty_available', '!=', 0)]}}
                else:
                    return {'domain': {'product_id': [('room_id', '=', rec.order_id.room_ids.ids)]}}

            # Method to Show Multiple Products Based On Bed and Partition
            if rec.order_id and rec.order_id.is_bed_partition:
                domain = []
                #  For Bed Space and Partition Product
                for rooms in rec.order_id.room_ids:
                    if rooms.leasing_based_on == 'bed_space':
                        for beds in rooms.bed_space_ids:
                            bed_space = self.env['product.template'].browse(beds.ids[0])
                            domain.append(bed_space.product_variant_id.id)
                    if rooms.leasing_based_on == 'partition':
                        for partition in rooms.room_partition_ids:
                            partition_room = self.env['product.template'].browse(partition.ids[0])
                            domain.append(partition_room.product_variant_id.id)
                return {'domain': {'product_id': [('id', 'in', domain)]}}
