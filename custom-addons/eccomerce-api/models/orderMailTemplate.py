from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Description'

    # -*- coding:utf-8 -*-
    def _action_send_mail(self):
        mail_obj = self.env['mail.mail']
        subject = f"Purchase Order ({self.name})"
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        email_to = self.partner_id.email
        body_html = f"""
            <table border="0" cellpadding="0" cellspacing="0" style="padding-top: 16px; background-color: #FFFFFF; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;">
            <tr>
                <td align="center">
                    <table border="0" cellpadding="0" cellspacing="0" width="590" style="padding: 16px; background-color: #FFFFFF; color: #454748; border-collapse:separate;">
                        <tr>
                            <td align="center" style="min-width: 590px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                                    <tr>
                                        <td valign="middle" align="middle">
                                            <img t-attf-src="{self.company_id.logo}" style="padding: 0px; margin: 0px; height: auto; width: 80px;" t-att-alt="object.company_id.name" />
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="text-align:center;">
                                            <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;" />
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                         <!-- CONTENT -->
                        <tr>
                            <td align="center" style="min-width: 590px;">
                                <table border="0" cellpadding="0" cellspacing="0"
                                    width="590"
                                    style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                                    <tr>
                                        <td valign="top" style="font-size: 13px;">
                                            <div> Dear <t t-out="object.name or ''">{self.partner_id.name}</t>,<br /><br />
                                           Your purchase order has been successful received</br>
                                           Order number is  <strong>{self.name}</strong>.
                                           <br/>
                                           One of our agent will contact you for further details
                                                    <div
                                                    style="margin: 16px 0px 16px 0px;">
                                                    <a href="{base_url}my/orders/{self.id}" target="_blank"
                                                        style="background-image: linear-gradient(#E9E7CD,#83D475); padding: 10px 16px 10px 16px; text-decoration: none; color: #fff; border-radius: 5px; font-size:15px;">
                                                        View My Order
                                                    </a>
                                                </div>
                                                Best Regards,
                                                    <br />
                                                   <br />{self.company_id.name}</t>
                                                </t>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="text-align:center;">
                                            <hr width="100%"
                                                style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;" />
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
            """
        mail = mail_obj.sudo().create({
            'body_html': body_html,
            'subject': subject,
            'email_to': email_to
        })
        mail.send()
        return {
            "code": 200,
            "state": "done"
            }