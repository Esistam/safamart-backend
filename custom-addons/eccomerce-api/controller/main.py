from odoo.http import request
from odoo import http
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import random
import json
import math

import logging

_logger = logging.getLogger(__name__)
today = datetime.today()
class MainController(http.Controller):
    @http.route('/view/catgory/products', type='json', auth="public", cors='*', method=['POST'])
    def view__category_propducts(self,**kw):
        payload = json.loads(request.httprequest.data)
        data=[]
        category = request.env['product.category'].sudo().search([('is_advert', "=", True)],limit=2)
        product = request.env['product.template'].sudo().search([('is_advert', "=", True)],limit=16)
        [data.append({"nameView":x.name,"descView":x.description,"titleView":x.title,"imageView":x.attachment,"lines":[{
        "productName":y.name,
        "productId":y.id,
        "productPrice":y.list_price,
        "productCategory":y.categ_id.name,
        "productImage":y.image_1920,
        "productDescription":y.description
        } for y in product if y.categ_id.name == x.name]})for x in category]
        response={
            "code":200,
            "status":"Successfull",
            "items":data
        }
        return response
    @http.route('/view/raw/products', type='json', auth="public", cors='*', method=['POST'])
    def view__raw_products(self):
        data=[]
        product = request.env['product.template'].sudo().search([('sale_ok', "=", True),('is_advert',"=",True)],limit=20)
        for res in product:
            vals={
                "productName":res.name,
                "productId":res.id,
                "productPrice":res.list_price,
                "productCategory":res.categ_id.name,
                "productImage":res.image_1920,
                "productDescription":res.description
            }
            data.append(vals)
        response={
            "code":200,
            "status":"Successfull",
            "items":data
        }
        return response
    @http.route('/view/products', type='json', auth="public", cors='*', method=['POST'])
    def view__products(self):
        query = """select id,name,list_price,categ_id from product_template LIMIT 20"""
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
        query = """select id,name,list_price,categ_id from product_template where id=%s""" %product_id
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

    @http.route('/view/details/products', type='json', auth="public", cors='*', method=['POST'])
    def view__details_products(self,**kw):
        payload = json.loads(request.httprequest.data)
        data=[]
        product = request.env['product.template'].sudo().search([("id","=",payload['product_id'])])
        for res in product:
            vals={
                "productName":res.name,
                "productId":res.id,
                "productCategory":res.categ_id.name,
                "productPrice":res.list_price,
                "productImage":res.image_1920,
                "productDescription":res.description
            }
            data.append(vals)
        response={
            "code":200,
            "status":"Successfull",
            "items":data
        }
        return response