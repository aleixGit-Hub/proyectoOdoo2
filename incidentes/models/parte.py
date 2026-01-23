from odoo import fields, models, api

class Parte(models.Model):
    _name = 'parte'
    name = fields.Char()

    _descripcion = 'Modelo para gestionar partes de incidentes'
    descripcion = fields.Char()

    _lugar = 'Lugar del incidente'
    lugar = fields.Char()

    _observaciones = 'Observaciones adicionales'
    observaciones = fields.Char()

    _estado = 'Estado del parte'
    estado = fields.Selection([
        ('procesado', 'Procesado'),
        ('en_proceso', 'En Proceso')
    ], default='en_proceso')

    _motivo_sancion = 'Motivo de la sanción'
    motivo_sancion = fields.Char()

    _fecha_hora = 'Fecha y hora del incidente'
    fecha_hora = fields.Datetime()

    _testigos = 'Testigos del incidente'
    testigos = fields.Char()