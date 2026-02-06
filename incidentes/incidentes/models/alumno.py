from odoo import fields, models

class Alumno(models.Model):
    _name = 'alumno'
    _description = 'Ficha del Alumno'

    # Datos básicos del estudiante
    name = fields.Char(string="Nombre completo", required=True)
    grupo_id = fields.Many2one('grupo', string="Grupo al que pertenece")