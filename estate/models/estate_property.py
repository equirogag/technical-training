from odoo import models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Modelo de prueba"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default='default_date_availability', copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('north', 'North'),('south','South'),('east','East'), ('west','West')]
    )
    active= fields.Boolean(default=True)
    state= fields.Selection(
        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True,
        copy=False
    )

    def default_date_availability(self):
        self.date_availability.add(fields.Date.today, months=3)