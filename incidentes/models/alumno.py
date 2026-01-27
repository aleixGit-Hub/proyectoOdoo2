from odoo import models, fields

class Alumno(models.Model):
    _name = 'alumno'
    _description = 'Alumno'

    name = fields.Char(string='Nombre', required=True)
    grupo_id = fields.Many2one('grupo', string='Grupo')  