# -*- coding: utf-8 -*-

from openerp import api, models


class ReportPricetag(models.AbstractModel):
    _name = 'report.sale_food.report_pricetag'

    @api.model
    def _get_products(self, products, fields):
        result = []
        if not products:
            return result
        products = list(self.env['product.product'].browse(products))
        return products

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        product_ids = data['form'].get('product_ids', [])
        fields = data['form'].get('fields', [])

        product_res = self.with_context(
            data['form'].get('used_context', {}))._get_products(
            product_ids, fields)
        pricetag_model = self.env['pricetag.model'].browse(
            data['form']['pricetag_model'])
        report_model = pricetag_model.report_model

        docargs = {
            'doc_ids': self.ids,
            'partner_id': self.env.user.partner_id,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'Products': product_res,
            'columns': pricetag_model.columns,
            'lines': pricetag_model.lines,
        }
        return self.env['report'].render(
            report_model, docargs)
