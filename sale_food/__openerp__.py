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
{
    'name': 'Sale - Food Information for Products',
    'version': '9.0.0.0.0',
    'category': 'Sales',
    'description': """
Allow users to record compulsory information on products and print them on
pricetags
====================================================================

Functionnalities :
    * Add various information about origin, makers, etc...
    * Possibility to print price tags, with suggestion about wich products
    to print. (when price change for exemple) according to legal obligation.
    """,
    'author': 'GRAP - Sylvain LE GAL (https://twitter.com/legalsylvain),'
              'Akretion - Julien WESTE',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'product_to_print',
        'report',
    ],
    'data': [
        'data/report_paperformat.xml',
        'data/pricetag_model.xml',
        'security/ir_model_access.yml',
        'security/ir_module_category.yml',
        'security/res_groups.yml',
        'views/product_uom_categ_view.xml',
        'views/product_view.xml',
        'views/pricetag_model.xml',
        'views/product_category_print_view.xml',
        'wizard/product_pricetag_wizard_view.xml',
        'report/sale_food_report.xml',
        'report/report_pricetag.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'css': [
        'static/src/css/pricetag.css',
    ],
}
