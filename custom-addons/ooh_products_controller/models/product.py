from odoo import models, fields, api,_
import datetime

today = datetime.date.today()

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_popular=fields.Boolean(string="Popular",default=False)
    is_new_arrival=fields.Boolean(string="New Arrival",default=False)
    is_limited_offer=fields.Boolean(string="Has Limited Offer",default=False)
    is_best_sale=fields.Boolean(string="Best Sale",default=False)
    is_trending=fields.Boolean(string="Trending?",default=False)
    discounted_amt=fields.Float(string="New Price")
    rate_id=fields.One2many("product.reviews",'product_id',string="Product",readonly=True)
    rate=fields.Selection([
                ("1",1),
                ("1",2),
                ("1",3),
                ("1",4),
                ("1",5)
        ],string="Ratings",related="rate_id.rate",readonly=True)
    person=fields.Char(string="Review Message",related="rate_id.name",readonly=True)
    message=fields.Char(string="Review Message",related="rate_id.message",readonly=True)
class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_active=fields.Boolean(string="Is Active?")

class ProductReview(models.Model):
    _name = 'product.reviews'

    name=fields.Char(string="Name",readonly=True)
    message=fields.Char(string="Review Message",readonly=True)
    product_id=fields.Many2one("product.template",string="Product",readonly=True)
    rate=fields.Selection([
            ("1",1),
            ("1",2),
            ("1",3),
            ("1",4),
            ("1",5)
    ],string="Ratings",readonly=True)