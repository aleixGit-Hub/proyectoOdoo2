# -*- coding: utf-8 -*-
from odoo import fields, models

class Profesor(models.Model):
    _name = 'profesor'
    _description = 'Ficha del Profesor'

    name = fields.Char(string="Nombre completo", required=True)
    dni = fields.Char(string="DNI / Identificación")
    
    # NUEVO: Enlace con el usuario del sistema para los permisos
    user_id = fields.Many2one('res.users', string="Usuario de Odoo")