from odoo import fields, models

class Parte(models.Model):
    _name = 'parte'
    _description = 'Modelo para gestionar partes de incidentes'

    name = fields.Char(string='Nombre', required=True)

    descripcion = fields.Char(string='Descripción')
    lugar = fields.Char(string='Lugar del incidente')
    observaciones = fields.Char(string='Observaciones adicionales')

    estado = fields.Selection(
        [
            ('procesado', 'Procesado'),
            ('en_proceso', 'En proceso')
        ],
        string='Estado',
        default='en_proceso'
    )

    motivo_sancion = fields.Char(string='Motivo de la sanción')

    fecha_hora = fields.Datetime(
        string='Fecha y hora',
        default=fields.Datetime.now
    )

    testigos = fields.Char(string='Testigos del incidente')

    grupo_id = fields.Many2one(
        'grupo',
        string='Grupo',
        required=True
    )
    