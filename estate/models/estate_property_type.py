from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property types"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'The name must be unique')
    ]
