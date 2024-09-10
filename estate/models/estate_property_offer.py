from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Offers"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity(days)", default =7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_from_validity", inverse='_compute_validity_from_deadline')

    @api.depends("validity")
    def _compute_deadline_from_validity(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _compute_validity_from_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days