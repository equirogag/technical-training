from odoo import models, fields,api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property types"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer(string="Sequence", default=1)

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")

    offer_count = fields.Integer(string="Offer qty", compute="_compute_offer_qty")

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'The name must be unique')
    ]

    api.depends("offer_ids")
    def _compute_offer_qty(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
