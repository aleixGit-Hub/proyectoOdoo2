from odoo import fields, models, api

class Empresa(models.Model):
    _name = 'empresas'
    name = fields.Char()