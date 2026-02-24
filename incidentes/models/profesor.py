# -*- coding: utf-8 -*-
from odoo import fields, models

class Profesor(models.Model):
    _name = 'profesor'
    _description = 'Ficha del Profesor'

    name = fields.Char(string="Nombre completo", required=True)
    dni = fields.Char(string="DNI / Identificación")