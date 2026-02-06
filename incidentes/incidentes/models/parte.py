from odoo import fields, models, api

class Parte(models.Model):
    _name = 'parte'
    _description = 'Parte de Incidencia'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _rec_name = 'alumno_id' # Al buscar, busca por nombre del alumno

    # -------------------------------------------------------------------------
    # CAMPOS PRINCIPALES (CABECERA)
    # -------------------------------------------------------------------------
    name = fields.Char(
        string='Referencia', 
        required=True, 
        default='Nuevo', 
        tracking=True
    )
    
    estado = fields.Selection(
        [
            ('borrador', 'Borrador'),
            ('comunicado', 'Comunicado'),
            ('sancionado', 'Sancionado'),
            ('cerrado', 'Cerrado')
        ],
        string='Estado actual',
        default='borrador',
        tracking=True
    )

    # -------------------------------------------------------------------------
    # RELACIONES CON OTROS MODELOS
    # -------------------------------------------------------------------------
    profesor_id = fields.Many2one('profesor', string='Profesor que reporta', required=True)
    alumno_id = fields.Many2one('alumno', string='Alumno implicado', required=True)
    grupo_id = fields.Many2one('grupo', string='Grupo', required=True)
    asignatura_id = fields.Many2one('asignatura', string='Asignatura afectada')

    # -------------------------------------------------------------------------
    # DETALLES DEL INCIDENTE
    # -------------------------------------------------------------------------
    fecha_hora = fields.Datetime(string='Fecha y hora', default=fields.Datetime.now)
    lugar = fields.Char(string='Lugar de los hechos')
    testigos = fields.Char(string='Testigos presentes')
    descripcion = fields.Text(string='Relato de los hechos')

    # -------------------------------------------------------------------------
    # GRAVEDAD Y SANCIONES (CON WIDGETS ESPECIALES)
    # -------------------------------------------------------------------------
    gravedad = fields.Selection(
        [
            ('leve', 'Leve'),
            ('grave', 'Grave'),
            ('muy_grave', 'Muy Grave')
        ],
        string='Nivel de Gravedad',
        default='leve',
        tracking=True
    )

    # Activa la cinta roja en la vista si es True
    tiene_expulsion = fields.Boolean(string='¿Conlleva Expulsión?', default=False, tracking=True)
    
    motivo_sancion = fields.Char(string='Sanción aplicada')
    observaciones = fields.Html(string='Medidas cautelares / Observaciones')

    # Campo para recoger la firma en tablet/pantalla
    firma_profesor = fields.Binary(string='Firma Digital del Profesor')