from odoo import fields, models, api

class Alumno(models.Model):
    _name = 'alumnos'
    name = fields.Char()