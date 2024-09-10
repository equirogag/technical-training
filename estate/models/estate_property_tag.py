from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Property tags"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name', 'UNIQUE(name)', 'The name must be unique')
    ]
