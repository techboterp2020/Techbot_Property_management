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


def _get_default_color(self):
    return randint(1, 11)


class ProductInherit(models.Model):
    _inherit = 'product.template'

    building_id = fields.Many2one('property.management.system', string="Building Name",
                                  tracking=True)  # domain="[('is_room','=',True)]",
    apartment_type_id = fields.Many2one('property.apartment.type')
    parking_availability = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Parking Available')
    room_ids = fields.One2many('product.template', 'apartment_id', domain="[('is_room','=',True)]", string='Rooms')
    apartment_id = fields.Many2one('product.template', string="Apartment Name", domain="[('is_apartment','=',True)]",
                                   tracking=True)


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    is_owner = fields.Boolean('Is Owner')


class PropertyManagementSystem(models.Model):
    _name = "property.management.system"
    _description = 'Property Management System'
    _inherit = ['mail.thread']

    # Building Fields
    name = fields.Char("Building Name", tracking=True)
    building_image = fields.Image('Building Image')

    # Building Addres Details
    street = fields.Char('Street')
    street2 = fields.Char("Street2")
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True)
    city = fields.Char('City', readonly=False, store=True)
    state_id = fields.Many2one("res.country.state", string='State', readonly=False, store=True,
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', readonly=False, store=True)

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id.country_id:
            self.country_id = self.state_id.country_id

    phone = fields.Char('Phone ')
    mobile = fields.Char('Mobile')
    email = fields.Char('Email')

    apartment_ids = fields.One2many('product.template', 'building_id',
                                    string='Apartment')  # domain="[('is_apartment','=',True)]"
    owner_id = fields.Many2one('res.partner', string="Owner Name", domain="[('is_owner','=',True)]", tracking=True)
    #
    # """ Method to Onchange owner address based on select the owner """
    #
    # @api.onchange('owner_id')
    # def onchange_owner_address(self):
    #     for rec in self:
    #         rec.street = rec.street2 = rec.zip = rec.city = rec.state_id = rec.country_id = False
    #         rec.phone = rec.mobile = rec.email = False
    #         if rec.owner_id:
    #             rec.street = rec.owner_id.street
    #             rec.street2 = rec.owner_id.street2
    #             rec.zip = rec.owner_id.zip
    #             rec.city = rec.owner_id.city
    #             rec.state_id = rec.owner_id.state_id
    #             rec.country_id = rec.owner_id.country_id
    #             rec.phone = rec.owner_id.phone
    #             rec.mobile = rec.owner_id.mobile
    #             rec.email = rec.owner_id.email
    #
    """ Method To create Owner in Buildings Creation"""

    @api.model
    def create(self, vals):
        res = super(PropertyManagementSystem, self).create(vals)
        if vals.get('owner_id'):
            res['owner_id']['is_owner'] = True
        #         # Method To create Owner Details From Building
        #         res['owner_id']['street'] = res['street']
        #         res['owner_id']['street2'] = res['street2']
        #         res['owner_id']['zip'] = res['zip']
        #         res['owner_id']['state_id'] = res['state_id']
        #         res['owner_id']['country_id'] = res['country_id']
        #         res['owner_id']['phone'] = res['phone']
        #         res['owner_id']['mobile'] = res['mobile']
        #         res['owner_id']['email'] = res['email']
        return res

    #
    # Edit The Owner in Building
    def write(self, vals):
        res = super(PropertyManagementSystem, self).write(vals)
        if vals.get('owner_id'):
            obj = self.env['res.partner'].browse(vals.get('owner_id'))
            obj['is_owner'] = True
        #         obj['street'] = self.street
        #         obj['street2'] = self.street2
        #         obj['zip'] = self.zip
        #         obj['state_id'] = self.state_id
        #         obj['country_id'] = self.country_id
        #         obj['phone'] = self.phone
        #         obj['mobile'] = self.mobile
        #         obj['email'] = self.email
        return res

    # Building Details Page
    building_plan_document_ids = fields.One2many('property.documents', 'property_id')
    building_lease_document_ids = fields.One2many('property.documents', 'property_id')
    lease_start_date = fields.Date('From')
    lease_end_date = fields.Date('To')

    # Advance Payment Details
    no_of_units = fields.Char("Total No.Of Units")
    advance_payment_date = fields.Date('Date')
    advance_payment_amount = fields.Integer('Paid Amount')
    advance_payment_cheque_no = fields.Char('Cheque No')
    # Rent Payable Details
    rent_paid_date = fields.Date('Rent Paid Date')
    rent_payment_amount = fields.Integer('Rent Paid Amount')
    rent_payment_cheque_no = fields.Char('Cheque No.')


class PropertyManagementSystemDocuments(models.Model):
    _name = 'property.documents'

    property_id = fields.Many2one('property.management.system')

    building_plan_document = fields.Binary("Building Plan")
    building_plan_filename = fields.Char('Building Plan Document File name')
    ejari_name = fields.Char('Ejari Name')
    ejari_documents = fields.Binary("Ejari Document")
    ejari_filename = fields.Char('Ejari Document name')
    dewa_sewa_no = fields.Char('Dewa/Sewa no')
    dewa_sewa_document = fields.Binary("Dewa/Sewa Document")
    dewa_sewa_filename = fields.Char('Dewa/Sewa Document name')
    kyc = fields.Char('KYC ID')
    kyc_document = fields.Binary("KYC Document")
    kyc_filename = fields.Char('KYC File Name')

    lease_agreement_document = fields.Binary("Lease Agreement Document")
    lease_agreement_filename = fields.Char('Lease Agreement File Name')

    mou_agreement_document = fields.Binary("MOU Agreement Document")
    mou_agreement_filename = fields.Char('MOU Agreement File Name')
