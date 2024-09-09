from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Modelo de prueba"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Gareden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientarion",
        selection = [('north', 'North'),('south','South'),('east','East'), ('west','West')]
    )
    active= fields.Boolean(default=True)
    state= fields.Selection(
        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True,
        copy=False
    )

    date_availability = fields.Date(string="Available From", default=fields.Date.add(fields.Date.today(), months=3), copy=False)

    property_type_id = fields.Many2one('estate.property.type',string="Property type")

    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer(readonly=True, string="Total Area (sqm)", compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area