from odoo.http import request
from odoo import http
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
import json

_logger = logging.getLogger(__name__)
today = datetime.today()


class ProductController(http.Controller):
    @http.route('/view/products', type='json', auth="public", cors='*', method=['POST'])
    def view__products(self):
        query = """select id,is_popular,is_new_arrival,is_limited_offer,discounted_amt,is_trending,is_best_sale,name,list_price,categ_id from product_template where available_in_pos=True"""
        request.cr.execute(query)    
        products = request.cr.dictfetchall() 
        data={
            "code":200,
            "status":"success",
            "result":products
        }
        return data
    @http.route('/view/categories', type='json', auth="public", cors='*', method=['POST'])
    def view__categories(self):
        query = """select id,name from product_category where is_active=True"""
        request.cr.execute(query)    
        category = request.cr.dictfetchall() 
        data={
            "code":200,
            "status":"success",
            "result":category
        }
        return data

    @http.route('/view/prod_details', type='json', auth="public", cors='*', method=['POST'])
    def view__product_details(self,**kws):
        data = json.loads(request.httprequest.data)
        product_id = data['product_id']
        query = """select id,is_limited_offer,discounted_amt,name,list_price,categ_id from product_template where id=%s""" %product_id
        query2 = """select id,name,message,rate,product_id from product_reviews where product_id=%s""" %product_id
        request.cr.execute(query) 
        category = request.cr.dictfetchall()
        request.cr.execute(query2)    
        ratings = request.cr.dictfetchall() 
        data={
            "code":200,
            "status":"success",
            "result":category,
            "ratings":ratings
        }
        return data
        
    @http.route('/create/sale_order', type='json', auth="public", cors='*', method=['POST'])
    def view__product_details(self,**kws):
        data = json.loads(request.httprequest.data)
        pass