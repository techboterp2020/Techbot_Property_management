# -*- coding: utf-8 -*-
from collections.abc import Iterable

import pytz, datetime
from odoo import api, fields, models, api, _
from odoo.exceptions import ValidationError,Warning

from odoo import SUPERUSER_ID


class PropertyDetails(models.Model):
    _name = 'property.details'
    _description = 'Property Details'

    sequence = fields.Integer(default=10)
    name = fields.Char(string="Property Name")
    property_image = fields.Binary(help="Select image here", attachment=True)
    address_name = fields.Char()
    street = fields.Char()
    township = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    property_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    property_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    date = fields.Datetime(string='Date')
    floor = fields.Integer('Floor')
    gfa_sqft = fields.Integer('GFA(sqfty)')
    gfa_m = fields.Integer('GFA(m)')
    # currency_id = fields.Many2one('res.currency', readonly=True)
    unit_price = fields.Float(string="Price Per Unit")
    # compute="_compute_base_unit_price")
    total_price = fields.Float(string='price Per Total')
    rent_type = fields.Char('Rent Type ')
    active = fields.Boolean('Active')

    parent_property = fields.Char("Parent Property")
    property_type = fields.Char("Property Type")
    property_manager = fields.Char('Property Manager')
    furnishing = fields.Char('Furnishing')
    bedrooms = fields.Char('Bedrooms')
    bathrooms = fields.Char('Bathrooms')

    currency = fields.Many2one("res.currency", string='Currency', tracking=True)
    #  readonly=True,
    # company_id = fields.Many2one('res.company', 'Company',  required=True)
    # readonly=True,
    # bedrooms = fields.Char('Bedrooms')
    # bathrooms = fields.Char('Bathrooms')

    # state_id = fields.Many2one('property.details.state', 'State',
    #                            # default=_get_default_pm_state, group_expand='_read_group_stage_ids',
    #                            tracking=True,
    #                            help='Current state of the Property', ondelete="set null")
    #
    # def _get_default_pm_state(self):
    #     state = self.env.ref('te_property_management.property_details_state_registered', raise_if_not_found=False)
    #     return state if state and state.id else False
