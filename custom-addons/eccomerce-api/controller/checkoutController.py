from odoo.http import request
from odoo import http
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import requests as method
from requests.auth import HTTPBasicAuth
import random
import json
import math
import base64
import logging

_logger = logging.getLogger(__name__)
today = datetime.today()
consumer_key = 'IZGdEmTpEEYhZuBemBzHGCsrrU5eUpZO'
consumer_secret = 'fmuKG1ASKokiaZ2Z'
api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
Business_short_code = "600992"


# headers = {"Authorization": "Bearer %s" % validated_mpesa_access_token}

class CheckoutController(http.Controller):
    # def _prepare_mpesa_values(self):
    #     r = method.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    #     lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    #     data_to_encode = Business_short_code + passkey + lipa_time
    #     online_password = base64.b64encode(data_to_encode.encode())
    #     mpesa_access_token = json.loads(r.text)
    #     decode_password = online_password.decode('utf-8')
    #     headers = {"Authorization": "Bearer %s" % mpesa_access_token['access_token']}
    #     payload = {
    #         "BusinessShortCode": Business_short_code,
    #         "Password": passkey,
    #         "Timestamp": lipa_time,
    #         "TransactionType": "CustomerPayBillOnline",
    #         "Amount": 1,
    #         "PartyA": 254110037818,
    #         "PartyB": Business_short_code,
    #         "PhoneNumber": 254110037818,
    #         "CallBackURL": "https://e63d-105-163-156-76.eu.ngrok.io",
    #         "AccountReference": "KADWEKA LIMITED",
    #         "TransactionDesc": "Payment of purchase"
    #     }
    #     response = method.post(api_url, json=payload, headers=headers)
    #     _logger.error(mpesa_access_token['access_token'])
    #     _logger.error("TESTING THE REQUIRED AUTHORIZATIONS")

    # @http.route("/payment", type="json", auth="public", cors="*", method=["POST"])
    # def receive_payment(self):
    #     # mobile_number
    #     # account_reference
    #     # transaction_desc
    #     _logger.error(self)

    @http.route("/payment", type="json", auth="public", cors="*", method=["POST"])
    def new_payment(self):
        self._prepare_mpesa_values()

    def _customer_validation_creation(self, customer):
        new_customer = request.env['res.partner'].sudo().create({
            "email": customer['email'],
            "phone": customer['phone'],
            "name": customer['name'],
            "city": customer['city'],
            "street": customer['state'],
            "country_id": customer['country_id']
        })
        return {
            "code": 200,
            "customer": new_customer.id
        }

    @http.route('/new_saleorder', type='json', auth="public", cors='*', method=['POST'])
    def new_sale_order(self, **kw):
        payload = json.loads(request.httprequest.data)
        if not payload['phone']:
            response = {
                'code': 403,
                'message': 'Phone Cannot be Empty'
            }
            return response
        if not payload['method']:
            response = {
                'code': 403,
                'message': 'Payment Method cannot be empty'
            }
            return response
        if not payload['name']:
            response = {
                'code': 403,
                'message': 'Name Cannot be Empty'
            }
            return response
        if not payload['city']:
            response = {
                'code': 403,
                'message': 'City Cannot be Empty'
            }
            return response
        if not payload['state']:
            response = {
                'code': 403,
                'message': 'State Cannot be Empty'
            }
            return response
        if not payload['country_id']:
            response = {
                'code': 403,
                'message': 'Country Cannot be Empty'
            }
            return response
        if not payload['email']:
            response = {
                'code': 403,
                'message': 'Email Cannot be Empty'
            }
            return response
        if not payload['lines']:
            response = {
                'code': 403,
                'message': 'Cart Cannot be Empty'
            }
            return response
        check_email = request.env['res.partner'].sudo().search(
            ["|", ('email', "=", payload['email']), ('phone', "=", payload['phone'])])
        if check_email:
            new_sale_order = request.env['sale.order'].sudo().create({
                "partner_id": check_email.id,
                "validity_date": today,
                "date_order": today,
                "payment_term_id": 1,
            })
            [request.env['sale.order.line'].sudo().create({
                'order_id': new_sale_order.id,
                'product_id': x['productId'],
                'name': x['productName'],
                'price_unit': x['productPrice'],
                'product_uom_qty': x["productQuantity"],
            }) for x in payload['lines']]
            if payload['method'] == "POD":
                _logger.error("TESTING THE EMAIL NOTIFICATION")
                new_sale_order._action_send_mail()
                return {
                    "code": 200,
                    "message": "You have created a sale order",
                    "ref": new_sale_order.name
                }
            else:
                return {
                    "code": 200,
                    "message": "You have  not processed your payment",
                    # "ref": new_sale_order.name
                }
        else:
            customer_payload = {
                "email": payload['email'],
                "phone": payload['phone'],
                "name": payload['name'],
                "city": payload['city'],
                "state": payload['state'],
                "country_id": payload['country_id']
            }
            partner_id = self._customer_validation_creation(customer_payload)
            if partner_id:
                new_sale_order = request.env['sale.order'].sudo().create({
                    "partner_id": partner_id['customer'],
                    "validity_date": today,
                    "date_order": today,
                    "payment_term_id": 1,
                    "order_line": [(0, 0, {
                        "product_template_id": x['productId'],
                        "name": x['productName'],
                        "customer_lead": 12.03,
                        "product_uom_qty": x['productQuantity'],
                        "price_unit": x['productPrice'],
                    }) for x in payload['lines']]
                })
            if new_sale_order:
                return {
                    "code": 200,
                    "message": "You have created a sale order",
                    "ref": new_sale_order.name
                }
