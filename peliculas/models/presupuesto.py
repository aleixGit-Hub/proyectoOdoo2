# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Presupuesto(models.Model):
    _name = "presupuesto"
    name = fields.Char()