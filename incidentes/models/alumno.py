from odoo import fields, models, api

class Alumno(models.Model):
    _name = 'alumno'
    name = fields.Char()

    _nia = 'Número de Identificación del Alumno'
    nia = fields.Char()