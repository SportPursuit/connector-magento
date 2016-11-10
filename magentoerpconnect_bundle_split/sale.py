# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Chafique Delli
#    Copyright 2014 Akretion SA
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

from openerp.addons.magentoerpconnect import sale
from openerp.addons.magentoerpconnect.backend import magento


@magento(replacing=sale.BundleLineStrategy)
class BundleLineStrategy(sale.BundleLineStrategy):
    _model_name = 'magento.sale.order.line'

    def price_is_zero(self, record):
        product_binder = self.get_binder_for_model('magento.product.product')
        magento_product_id = product_binder.to_openerp(record['product_id'])
        magento_product = self.session.browse('magento.product.product',
                                              magento_product_id)
        if magento_product.price_type == 'dynamic':
            return True


@magento(replacing=sale.BundleLineLinker)
class BundleLineLinker(sale.BundleLineLinker):
    _model_name = ['magento.sale.order']

    def link_lines(self, record):
        line_binder = self.get_binder_for_model('magento.sale.order.line')
        for item in record['items']:
            if item['parent_item_id']:
                line_id = line_binder.to_openerp(item['item_id'], unwrap=True)
                line = self.session.browse('sale.order.line', line_id)
                parent_id = line_binder.to_openerp(item['parent_item_id'],
                                                   unwrap=True)
                line.write({'line_parent_id': parent_id})