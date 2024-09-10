from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging
from odoo.tools.float_utils import float_is_zero
_logger = logging.getLogger(__name__)

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
        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
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

    best_price = fields.Float(readonly=True, string="Best Offer", compute="_compute_best_offer")

    _sql_contraints = [
        ('positive_expeceted_price', 'CHECK(expected_price >= 0.0)', 'The expected price must be postive'),
        ('positive_selling_price', 'CHECK(selling_price >= 0.0)', 'The selling price must be positive')
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < (record.expected_price * 0.9) and not float_is_zero(record.selling_price):
                raise ValidationError("The selling price cannot be lower than the 90% of the expected price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            price_list = record.offer_ids.mapped('price')
            if not price_list:
                record.best_price = 0.0
            else:
                record.best_price = max(price_list)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def cancel_property(self):
        if self.state == 'sold':
            raise UserError("Sold properties cannot be canceled")
        else:
            self.state = 'canceled'
            return True

    def sold_property(self):
        if self.state == 'canceled':
            raise UserError('Canceled properties cannot be sold')
        else:
            self.state = 'sold'
            return True


