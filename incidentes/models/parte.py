# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Parte(models.Model):
    _name = 'parte'
    _description = 'Parte de Incidencia'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    # -------------------------------------------------------------------------
    # CAMPOS PRINCIPALES
    # -------------------------------------------------------------------------
    name = fields.Char(
        string='Referencia',
        required=True,
        default='Nuevo',
        tracking=True
    )

    estado = fields.Selection(
        [
            ('borrador',   'Borrador'),
            ('comunicado', 'Comunicado'),
            ('sancionado', 'Sancionado'),
            ('cerrado',    'Cerrado'),
        ],
        string='Estado actual',
        default='borrador',
        tracking=True
    )

    # -------------------------------------------------------------------------
    # RELACIONES
    # -------------------------------------------------------------------------
    profesor_id   = fields.Many2one('profesor',   string='Profesor que reporta', required=True)
    alumno_id     = fields.Many2one('alumno',     string='Alumno implicado',     required=True)
    grupo_id      = fields.Many2one('grupo',      string='Grupo',                required=True)
    asignatura_id = fields.Many2one('asignatura', string='Asignatura afectada')

    # -------------------------------------------------------------------------
    # DETALLES DEL INCIDENTE
    # -------------------------------------------------------------------------
    fecha_hora = fields.Datetime(
        string='Fecha y hora',
        default=fields.Datetime.now
    )

    ubicacion = fields.Selection(
        [
            ('aula',       'Aula'),
            ('pasillo',    'Pasillo'),
            ('patio',      'Patio'),
            ('biblioteca', 'Biblioteca'),
            ('gimnasio',   'Gimnasio'),
            ('comedor',    'Comedor'),
            ('entrada',    'Entrada / Recepción'),
            ('aseos',      'Aseos'),
            ('otro',       'Otro'),
        ],
        string='Ubicación del incidente',
        required=True,
        default='aula',
        tracking=True
    )

    testigos    = fields.Char(string='Testigos presentes')
    descripcion = fields.Text(string='Relato de los hechos')

    # -------------------------------------------------------------------------
    # ESTADO DE LA LLAMADA
    # -------------------------------------------------------------------------
    gravedad = fields.Selection(
        [
            ('pendiente',  'Pendiente'),
            ('completado', 'Completado'),
            ('cerrado',    'Cerrado'),
        ],
        string='Estado de la llamada',
        default='pendiente',
        tracking=True
    )

    tiene_expulsion = fields.Boolean(
        string='¿Conlleva Expulsión?',
        default=False,
        tracking=True
    )

    observaciones = fields.Html(
        string='Observaciones / Documentación adjunta'
    )

    # -------------------------------------------------------------------------
    # WIDGET priority
    # -------------------------------------------------------------------------
    priority = fields.Selection(
        [
            ('0', 'Normal'),
            ('1', 'Importante'),
            ('2', 'Muy importante'),
            ('3', 'Urgente'),
        ],
        string='Prioridad',
        default='0',
        tracking=True
    )

    # -------------------------------------------------------------------------
    # WIDGET progressbar
    # -------------------------------------------------------------------------
    progreso_estado = fields.Integer(
        string='Progreso del parte (%)',
        compute='_compute_progreso_estado',
        store=True
    )

    @api.depends('estado')
    def _compute_progreso_estado(self):
        mapa = {
            'borrador':   10,
            'comunicado': 40,
            'sancionado': 75,
            'cerrado':    100,
        }
        for rec in self:
            rec.progreso_estado = mapa.get(rec.estado, 0)

    # -------------------------------------------------------------------------
    # WIDGET statinfo
    # -------------------------------------------------------------------------
    total_partes_alumno = fields.Integer(
        string='Partes del alumno',
        compute='_compute_total_partes_alumno',
        store=False
    )

    @api.depends('alumno_id')
    def _compute_total_partes_alumno(self):
        for rec in self:
            if rec.alumno_id and rec.alumno_id.id:
                rec.total_partes_alumno = self.search_count(
                    [('alumno_id', '=', rec.alumno_id.id)]
                )
            else:
                rec.total_partes_alumno = 0

    def action_ver_partes_alumno(self):
        self.ensure_one()
        return {
            'name': 'Partes de ' + (self.alumno_id.name or ''),
            'type': 'ir.actions.act_window',
            'res_model': 'parte',
            'view_mode': 'tree,form',
            'domain': [('alumno_id', '=', self.alumno_id.id)],
        }

    # -------------------------------------------------------------------------
    # CONSTRAINT SQL
    # -------------------------------------------------------------------------
    _sql_constraints = [
        (
            'unique_alumno_fecha',
            'UNIQUE(alumno_id, fecha_hora)',
            'Ya existe un parte para este alumno en esa misma fecha y hora exacta.'
        ),
    ]

    # -------------------------------------------------------------------------
    # ONCHANGE
    # -------------------------------------------------------------------------
    @api.onchange('alumno_id')
    def _onchange_alumno_id(self):
        if self.alumno_id and self.alumno_id.grupo_id:
            self.grupo_id = self.alumno_id.grupo_id

    @api.onchange('grupo_id')
    def _onchange_grupo_id(self):
        domain_alumno = []
        if self.grupo_id:
            if self.alumno_id and self.alumno_id.grupo_id != self.grupo_id:
                self.alumno_id = False
            domain_alumno = [('grupo_id', '=', self.grupo_id.id)]
        return {'domain': {'alumno_id': domain_alumno}}

    # -------------------------------------------------------------------------
    # CONSTRAINS PYTHON
    # -------------------------------------------------------------------------
    @api.constrains('alumno_id', 'grupo_id')
    def _check_alumno_grupo(self):
        for rec in self:
            if rec.alumno_id and rec.grupo_id:
                if rec.alumno_id.grupo_id and rec.alumno_id.grupo_id != rec.grupo_id:
                    raise ValidationError(
                        'El alumno "%s" pertenece al grupo "%s", no al grupo "%s".' % (
                            rec.alumno_id.name,
                            rec.alumno_id.grupo_id.name,
                            rec.grupo_id.name,
                        )
                    )

    @api.constrains('tiene_expulsion', 'gravedad')
    def _check_expulsion_gravedad(self):
        for rec in self:
            if rec.tiene_expulsion and rec.gravedad == 'pendiente':
                raise ValidationError(
                    'Un parte con expulsión no puede quedar en estado "Pendiente". '
                    'Márcalo como "Completado" o "Cerrado".'
                )
