from odoo import fields, models

class Grupo(models.Model):
    _name = 'grupo'
    _description = 'Grupo'

    name = fields.Char(string='Nombre del grupo', required=True)
