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
    @http.route('/view/category/products', type='json', auth="public", cors='*', method=['POST'])
    def view__category_propducts(self, **kw):
        payload = json.loads(request.httprequest.data)
        data = []
        product = request.env['product.template'].sudo().search(["&",("categ_id.id",'=',payload['category_id']),("name",'ilike',payload['name'])], limit=12)
        [data.append({"productName": x.name,"productId": x.id,"productPrice": x.list_price,"productCategory": x.categ_id.name,"productImage": x.image_1920,"productDescription": x.description})for x in product]
        response = data
        return response
    @http.route('/view/category/information', type='json', auth="public", cors='*', method=['POST'])
    def view__category_information(self, **kw):
        payload = json.loads(request.httprequest.data)
        data = []
        category = request.env['product.category'].sudo().search([('is_advert', "=", True),("id","=",payload['category_id'])])
        [data.append({"categoryName":x.name,"categoryId":x.id,"categoryImage":x.attachment,"categoryDescription":x.description})for x in category]
        response = data
        return response
    @http.route('/view/raw/products', type='json', auth="public", cors='*', method=['POST'])
    def view__raw_products(self,**kw):
        payload = json.loads(request.httprequest.data)
        data1 = []
        data2 = []
        product = request.env['product.template'].sudo().search(["&",("is_advert","=",False),('sale_ok', "=", True),("name","ilike",payload["name"])],limit=12)
        product2 = request.env['product.template'].sudo().search(["&",("is_advert","=",True),('sale_ok', "=", True),("name","ilike",payload["name"])],limit=12)
        [data1.append({"productName": x.name,"productId": x.id,"productPrice": x.list_price,"productCategory": x.categ_id.name,"productImage": x.image_1920,"productDescription": x.description})for x in product]
        [data2.append({"productName": x.name,"productId": x.id,"productPrice": x.list_price,"productCategory": x.categ_id.name,"productImage": x.image_1920,"productDescription": x.description})for x in product2]
        response = {
            "code": 200,
            "status": "Successfully",
            "item1": data1,
            "item2": data2
        }
        return response


    @http.route("/search_read",type='json', auth="public", cors='*', method=['POST'])
    def search_products(self,**kw):
        payload = json.loads(request.httprequest.data)
        data = []
        domain=["|",("sale_ok", "=",True),("name", "ilike",payload['name'])]
        product = request.env['product.template'].sudo().search(domain, limit=12)
        [data.append({"productName": x.name,"productId": x.id,"productPrice": x.list_price,"productCategory": x.categ_id.name,"productImage": x.image_1920,"productDescription": x.description})for x in product]
        response = data
        return response

    @http.route('/view/category', type='json', auth="public", cors='*', method=['POST'])
    def view__raw_category(self,**kw):
        payload = json.loads(request.httprequest.data)
        data = []
        category = request.env['product.category'].sudo().search(["&",('is_advert', "=", True),("name","ilike",payload["name"])])
        [data.append({"imgView":x.attachment,"categView":x.id,"categName":x.name}) for x in category]
        response = {
            "code": 200,
            "status": "Successfully",
            "items": data
        }
        return response











# SINGLE PAGE SECTION ENDPOINTS
    @http.route("/related_products",type="json", auth="public", cors="*", method=["POST"])
    def view_related_product_reviews(self,**kw):
        payload = json.loads(request.httprequest.data)
        data = []
        products = request.env['product.template'].sudo().search(["&",("categ_id.id", "=", payload['categ_id']),('name',"ilike",payload['name'])],limit=28)
        [data.append({
            "productName": x.name,
                "productId": x.id,
                "productPrice": x.list_price,
                "productCategory": x.categ_id,
                "productRating": x.rating,
                "productImage": x.image_1920,
                "categoryName": x.categ_id.name,
                "productDescription": x.description}) for x in products]
        return data
    @http.route("/my/review",type="json", auth="public", cors="*", method=["POST"])
    def view_single_product_reviews(self,**kw):
        payload = json.loads(request.httprequest.data)
        data = []
        reviews = request.env['product.reviews'].sudo().search([("product_id.id", "=", payload['product_id'])])
        [data.append({"reviewAuthor": y.name, "reviewMessage": y.message, "reviewRate": int(y.rate)}) for y in reviews]
        return data
    @http.route('/new/review', type="json", auth="public", cors="*", method=["POST"])
    def new_review(self, **kw):
        data = json.loads(request.httprequest.data)
        author = data['name']
        star = data['rate']
        message = data['message']
        productId = data['product_id']
        if not productId:
            response = {
                'code': 400,
                'message': 'Product Id cannot be empty cannot be empty'
            }
            return response
        if not author:
            response = {
                'code': 400,
                'message': 'Name cannot be empty cannot be empty'
            }
            return response
        if not star:
            response = {
                'code': 400,
                'message': 'Rating cannot be empty'
            }
            return response
        if not message:
            response = {
                'code': 400,
                'message': 'Message cannot be empty'
            }
            return response
        rating = request.env['product.reviews'].sudo().create({
            'name': author.lower(),
            'message': message.lower(),
            'rate': star,
            'product_id': productId
        })
        if rating:
            return {
                "code": 200,
                "status": "Success",
                "message": "You Have created a review"
            }

    @http.route('/view/details/products', type='json', auth="public", cors='*', method=['POST'])
    def view__details_products(self, **kw):
        payload = json.loads(request.httprequest.data)
        data = []
        product = request.env['product.template'].sudo().search([("id", "=", payload['product_id'])])
        [data.append(
            {
                "productName": x.name,
                "productId": x.id,
                "productRating": x.rating,
                "productPrice": x.list_price,
                "productCategory": x.categ_id.id,
                "productImage": x.image_1920,
                "categoryName": x.categ_id.name,
                "productDescription": x.description}) for x in product]
        return data
