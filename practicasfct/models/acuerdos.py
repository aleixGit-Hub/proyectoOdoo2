from odoo import fields, models, api

class Acuerdo(models.Model):
    _name = 'acuerdos'
    name = fields.Char()