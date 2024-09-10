from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Offers"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity(days)", default =7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_from_validity", inverse='_compute_validity_from_deadline')

    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)', 'The offer price must be positive')
    ]

    @api.depends("validity")
    def _compute_deadline_from_validity(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _compute_validity_from_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        accepted_offer =  self.env['estate.property.offer'].search([('status','=','accepted'), ('property_id', '=', self.property_id.id)], limit=1)
        if accepted_offer:
            raise UserError("You can't accept more than one offer per property")
        else:
            self.status = 'accepted'
            self.property_id.buyer = self.partner_id.id
            self.property_id.selling_price = self.price

    def refuse_offer(self):
        self.status = 'refused'