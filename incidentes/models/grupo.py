# -*- coding: utf-8 -*-
from odoo import fields, models

class Grupo(models.Model):
    _name = 'grupo'
    _description = 'Grupos/Clases'

    name = fields.Char(string='Nombre (Ej: 1º DAM)', required=True)
    etapa = fields.Selection(
        [
            ('eso',        'ESO'),
            ('bachiller',  'Bachillerato'),
            ('fp_basica',  'FP Básica'),
            ('ciclos',     'Ciclos Formativos'),
        ],
        string='Etapa educativa',
        required=True,
        default='ciclos',
    )
    
    # NUEVO: El tutor se asigna a todo el grupo
    tutor_id = fields.Many2one('profesor', string='Tutor del Grupo')