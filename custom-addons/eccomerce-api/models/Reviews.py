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
            ("2",2),
            ("3",3),
            ("4",4),
            ("5",5)
    ],string="Ratings",readonly=True)

class ProductCatgory(models.Model):
        _inherit = 'product.category'

      
                
        attachment = fields.Binary(string="Attachment")    
        store_fname = fields.Char(string="File Name")
        description=fields.Char("Description")
        title=fields.Char("Title")
        is_offer=fields.Boolean(string="Has Offer")
        offer_value=fields.Float(string="rate %")
        is_advert=fields.Boolean(string="Is Advert",default=True)


class ProductTemplate(models.Model):
        _inherit = 'product.template'

        @api.depends('rate_ids')
        def _compute_product_ratings(self):
                totalRating=0
                items=len(self.rate_ids)
                for rec in self:
                    for res in rec.rate_ids:
                        totalRating+=int(res.rate)
                value=totalRating/items if len(self.rate_ids)>0 else 0
                self.rating=value
        is_advert=fields.Boolean(string="Is Advert")
        rate_ids=fields.One2many("product.reviews",'product_id',string="Product")
        rating=fields.Float(string="Ratings",compute='_compute_product_ratings')