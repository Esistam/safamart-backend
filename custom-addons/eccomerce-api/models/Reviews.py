from odoo import models, fields, api,_
import datetime

today = datetime.date.today()

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

class ProductCatgory(models.Model):
        _inherit = 'product.category'

        attachment = fields.Binary(string="Attachment")    
        store_fname = fields.Char(string="File Name")
        description=fields.Char("Description")
        title=fields.Char("Title")
        is_offer=fields.Boolean(string="Has Offer")
        offer_value=fields.Float(string="rate %")
        is_advert=fields.Boolean(string="Is Advert")


class ProductTemplate(models.Model):
        _inherit = 'product.template'

        is_advert=fields.Boolean(string="Is Advert")