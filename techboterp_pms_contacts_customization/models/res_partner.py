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
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    """ Tenant Details Master """
    is_tenant = fields.Boolean('Is tenant')
    proof_id = fields.Many2one('id.proof', string='ID proof Name')
    id_proof_documents = fields.Binary("ID proof")
    id_proof_filename = fields.Char("ID proof File name")
    bank_name_id = fields.Many2one('bank.details', string='Bank Name')
    cheque_book_available = fields.Boolean(string='Cheque Book Available')
    cheque_book_document = fields.Binary("Cheque Book ")
    cheque_book_document_filename = fields.Char("Cheque File name")

    dob = fields.Date("DOB")
    age = fields.Char(string='Age', compute='_compute_student_age', help='Enter Tenant age')  #
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male',
                              help='Select The gender')
    designation_id = fields.Many2one('job.designation', string='Designation', help='Job Designation')
    work_location_id = fields.Many2one('work.location', string='Work Location', help='Work Location ')
    blood_group_id = fields.Many2one('blood.group', help='Enter the blood group')
    instagram = fields.Char("Instagram ID")
    phone_details = fields.Selection([('android', 'Android'), ('iphone', 'iPhone')])
    medical_condition = fields.Selection([('no', 'No'), ('yes', 'Yes')], default='no', string='Any medical Condition')
    emergency_contact_name = fields.Char(string='Emergency Contact Person')
    emergency_contact_number = fields.Char(string='Contact Number')

    @api.depends('dob')
    def _compute_student_age(self):
        """ Method to calculate student age """
        for rec in self:
            required_age = 0
            current_dt = fields.Date.today()
            rec.age = 0
            if rec.dob and rec.dob < current_dt:
                start = rec.dob
                age_calc = int((current_dt - start).days / 365)
                #   Method to check age should be greater than 4
                if age_calc < required_age:
                    raise ValidationError(_("Age of student should be greater than %s years!" % required_age))
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    # @api.constrains('dob')
    # def _check_date(self):
    #     """ Method to Restrict DOB should not be Greater than Current Date """
    #     current_dt = fields.Datetime.today()
    #     for rec in self:
    #         if current_dt < rec.dob:
    #             raise ValidationError(_('The DOB Date cannot be Greater than the Current Date.'))
    # if rec.start_date > rec.end_date:
    #     raise ValidationError(_('Select Proper Start Date and End Date.'))

    # Tenant Documents Details

    ''' Tenant Agreement Details'''
    start_date = fields.Date('Start Date', default=fields.Date.today)
    end_date = fields.Date('End Date')

    # @api.constrains('start_date', 'end_date')
    # def _check_start_date(self):
    #     if self.start_date > self.end_date:
    #         raise ValidationError(_('The DOB Date cannot be Greater than the Current Date.'))

##########################################################################################################################
    """Owner Master Details"""
    building_count = fields.Integer(compute='_compute_building_count', string='Vehicles')

    def _compute_building_count(self):
        """         Override original method to Count Owner Buildings         """
        building_obj = self.env['property.management.system']
        for owner in self:
            owner.building_count = building_obj.search_count([('owner_id', '=', owner.id)])
            _logger.info("partner.building_count %s", owner.building_count)

    def get_owner_buildings(self):
        """
        Return an action that display Building records related for the given owner.
        """
        building_obj = self.env['property.management.system']
        building_ids = building_obj.search([('owner_id', '=', self.id)]).mapped('id')
        return {
            'domain': [('id', 'in', building_ids)],
            'name': _('Buildings'),
            'view_type': 'kanban',
            'view_mode': 'kanban,tree,form',
            'res_model': 'property.management.system',
            'view_id': False,
            'context': {'default_owner_id': self.id},
            'type': 'ir.actions.act_window'
        }


class BloodGroup(models.Model):
    _name = 'blood.group'
    _description = 'Blood Group'
    _rec_name = 'blood_group'

    blood_group = fields.Char('Blood Group', help='Enter student blood group')


class JobDesignation(models.Model):
    _name = 'job.designation'
    _description = 'job Designation'
    _rec_name = 'job_designation'

    job_designation = fields.Char('Work Location', help='Enter the Job Description')


class WorkLocation(models.Model):
    _name = 'work.location'
    _description = 'Work Location'
    _rec_name = 'work_location'

    work_location = fields.Char('Work Location', help='Enter the Work Location')


class IdProof(models.Model):
    _name = 'id.proof'
    _description = 'ID Proof'
    _rec_name = 'id_proof'

    id_proof = fields.Char('ID Proof Name', help='Enter the ID Proof Name')


class IdProof(models.Model):
    _name = 'bank.details'
    _description = 'Bank Details'
    _rec_name = 'bank_details'

    bank_details = fields.Char('Bank Name', help='Enter the Bank Name')
