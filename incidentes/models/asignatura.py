from odoo import fields, models, api

class Asignatura(models.Model):
    _name = 'asignatura'
    name = fields.Char()