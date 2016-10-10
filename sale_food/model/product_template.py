# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale - Food Module for Odoo
#    Copyright (C) 2012-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Constant Section
    _FRESH_CATEGORY_KEYS = [
        ('extra', 'Extra'),
        ('1', 'Category I'),
        ('2', 'Category II'),
        ('3', 'Category III'),
    ]

    _FRESH_RANGE_KEYS = [
        ('1', '1 - Fresh'),
        ('2', '2 - Canned'),
        ('3', '3 - Frozen'),
        ('4', '4 - Uncooked and Ready to Use'),
        ('5', '5 - Cooked and Ready to Use'),
        ('6', '6 - Dehydrated and Shelf'),
    ]

    # Columns section
    @api.depends('list_price', 'volume')
    @api.multi
    def _compute_price_volume(self):
        """Return the price by liter"""
        for pt in self:
            if pt.list_price and pt.volume:
                pt.price_volume = "%.2f" % round(pt.list_price / pt.volume, 2)
            else:
                pt.price_volume = ""

    @api.depends('list_price', 'weight_net')
    @api.multi
    def _compute_price_weight_net(self):
        """Return the price by kg"""
        for pt in self:
            if pt.list_price and pt.weight_net:
                pt.price_weight_net = "%.2f" % round(
                    pt.list_price / pt.weight_net, 2)
            else:
                pt.price_weight_net = ""

    @api.depends('origin_description', 'department_id', 'country_id')
    @api.multi
    def _compute_pricetag_origin(self):
        for pt in self:
            tmp = ''
            if pt.origin_description:
                tmp = pt.origin_description
            if pt.department_id:
                tmp = pt.department_id.name + \
                    (' - ' + tmp if tmp else '')
            if pt.country_id:
                tmp = pt.country_id.name + \
                    (' - ' + tmp if tmp else '')
            if pt.maker_description:
                tmp = (tmp and (tmp + ' - ') or '') + pt.maker_description
            pt.pricetag_origin = tmp

    @api.depends('fresh_category', 'fresh_range')
    @api.multi
    def _compute_extra_food_info(self):
        """Return extra information about food for legal documents"""
        for pt in self:
            tmp = ''
            if pt.fresh_range:
                tmp += _(' - Range: ') + pt.fresh_range
            if pt.fresh_category:
                tmp += _(" - Category: ") + pt.fresh_category
            pt.extra_food_info = tmp

    is_mercuriale = fields.Boolean(
        'Mercuriale Product', help="A product in mercuriale has price"
        " that changes very regularly.")
    weight_net = fields.Float('Net Weight', default=0)
    price_volume = fields.Char(
        compute=_compute_price_volume, string='Price by liter')
    price_weight_net = fields.Char(
        compute=_compute_price_weight_net, string='Price by kg')

    country_id = fields.Many2one(
        'res.country', 'Origin Country',
        help="Country of production of the product")
    department_id = fields.Many2one(
        'res.country.department', 'Origin Department',
        help="Department of production of the product")
    origin_description = fields.Char(
        'Origin Complement', size=64,
        help="Production location complementary information",)
    maker_description = fields.Char(
        'Maker', size=64, required=False)
    pricetag_origin = fields.Char(
        compute=_compute_pricetag_origin, string='Text about origin')
    fresh_category = fields.Selection(
        _FRESH_CATEGORY_KEYS, 'Category for Fresh Product',
        help="Extra - Hight Quality : product without default ;\n"
        "Quality I - Good Quality : Product with little defaults ;\n"
        "Quality II - Normal Quality : Product with default ;\n"
        "Quality III - Bad Quality : Use this option only in"
        " specific situation.")
    fresh_range = fields.Selection(
        _FRESH_RANGE_KEYS, 'Range for Fresh Product')
    extra_food_info = fields.Char(
        compute=_compute_extra_food_info,
        string='Extra information for invoices')

    # Constraints section
    @api.multi
    @api.constrains('seats_max', 'seats_available')
    def _check_origin_department_country(self):
        for pt in self:
            if pt.department_id.country_id and \
                    pt.department_id.country_id.id != \
                    pt.country_id.id:
                raise UserError(
                    _("Error ! Department %s doesn't belong to %s.")
                    % (pt.department_id.name, pt.country_id.name))

    # Views section
    @api.multi
    @api.onchange('department_id')
    def onchange_department_id(self):
        for pt in self:
            if pt.department_id:
                pt.country_id = pt.department_id.country_id
            else:
                pt.country_id = False

    @api.multi
    @api.onchange('country_id')
    def onchange_country_id(self):
        for pt in self:
            if pt.country_id:
                pt.department_id = False
