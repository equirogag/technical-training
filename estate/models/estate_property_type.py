from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property types"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer(string="Sequence", default=1)

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'The name must be unique')
    ]
