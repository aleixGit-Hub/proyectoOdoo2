# -*- coding: utf-8 -*-
from odoo import fields, models

class Grupo(models.Model):
    _name = 'grupo'
    _description = 'Grupos/Clases'

    name = fields.Char(string='Nombre (Ej: 1º DAM)', required=True)
