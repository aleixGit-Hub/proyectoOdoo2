from odoo import fields, models, api

class Grupo(models.Model):
    _name = 'grupo'
    name = fields.Char()