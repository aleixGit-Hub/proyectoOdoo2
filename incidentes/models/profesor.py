from odoo import fields, models, api

class Profesor(models.Model):
    _name = 'profesor'
    name = fields.Char()

    _dni = 'Documento Nacional de Identidad'
    dni = fields.Char()