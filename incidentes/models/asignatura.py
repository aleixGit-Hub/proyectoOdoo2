from odoo import fields, models

class Asignatura(models.Model):
    _name = 'asignatura'
    _description = 'Asignaturas'

    name = fields.Char(string='Nombre de la asignatura', required=True)