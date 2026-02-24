# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Parte(models.Model):
    _name = 'parte'
    _description = 'Parte de Incidencia Grave'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Referencia', required=True, default='Nuevo', tracking=True)

    profesor_id   = fields.Many2one('profesor',   string='Profesor que reporta', required=True)
    alumno_id     = fields.Many2one('alumno',     string='Alumno implicado',     required=True)
    grupo_id      = fields.Many2one('grupo',      string='Grupo',                required=True)
    asignatura_id = fields.Many2one('asignatura', string='Asignatura afectada')

    fecha_hora = fields.Datetime(string='Fecha y hora', default=fields.Datetime.now)

    ubicacion = fields.Selection([
        ('aula_materia', 'Aula Materia'),
        ('aula_grupo',   'Aula Grupo'),
        ('pasillo',      'Pasillo'),
        ('patio',        'Patio'),
        ('gimnasio',     'Gimnasio'),
        ('aseos',        'Aseos'),
        ('otro',         'Otro'),
    ], string='Ubicación del incidente', required=True, default='aula_materia', tracking=True)

    motivo = fields.Selection([
        ('indisciplina',    'Actos graves de indisciplina'),
        ('agresion_fisica', 'Agresión física grave'),
        ('insultos',        'Insultos y amenazas graves'),
        ('suplantacion',    'Suplantación de identidad'),
        ('sustraccion',     'Sustracción de documentos académicos'),
        ('acoso',           'Acoso o ciberacoso'),
        ('discriminacion',  'Discriminación por motivos protegidos'),
        ('otro',            'Otro motivo grave'),
    ], string='Motivo de la falta grave', required=True, tracking=True)

    testigos    = fields.Char(string='Testigos presentes')
    descripcion = fields.Text(string='Relato de los hechos')

    # Estado único — contacto con familia
    gravedad = fields.Selection([
        ('pendiente_llamar', 'Pendiente Contactar'),
        ('llamado',          'Contactado'),
        ('cerrado',          'Cerrado'),
    ], string='Estado', default='pendiente_llamar', tracking=True)

    tiene_expulsion = fields.Boolean(string='¿Conlleva Expulsión?', default=False, tracking=True)
    observaciones   = fields.Html(string='Observaciones / Documentación adjunta')

    llamada_ids = fields.One2many('parte.llamada', 'parte_id', string='Registro de llamadas')

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Importante'),
        ('2', 'Muy importante'),
        ('3', 'Urgente'),
    ], string='Prioridad', default='0', tracking=True)

    # --- Statinfo ---
    total_partes_alumno = fields.Integer(string='Partes del alumno', compute='_compute_total_partes_alumno', store=False)

    @api.depends('alumno_id')
    def _compute_total_partes_alumno(self):
        for rec in self:
            rec.total_partes_alumno = self.search_count([('alumno_id', '=', rec.alumno_id.id)]) if rec.alumno_id else 0

    def action_ver_partes_alumno(self):
        self.ensure_one()
        return {'name': 'Partes de ' + (self.alumno_id.name or ''), 'type': 'ir.actions.act_window',
                'res_model': 'parte', 'view_mode': 'tree,form', 'domain': [('alumno_id', '=', self.alumno_id.id)]}

    total_expulsiones_alumno = fields.Integer(string='Expulsiones', compute='_compute_total_expulsiones_alumno', store=False)

    @api.depends('alumno_id')
    def _compute_total_expulsiones_alumno(self):
        for rec in self:
            rec.total_expulsiones_alumno = self.search_count([('alumno_id', '=', rec.alumno_id.id), ('tiene_expulsion', '=', True)]) if rec.alumno_id else 0

    def action_ver_expulsiones_alumno(self):
        self.ensure_one()
        return {'name': 'Expulsiones de ' + (self.alumno_id.name or ''), 'type': 'ir.actions.act_window',
                'res_model': 'parte', 'view_mode': 'tree,form', 'domain': [('alumno_id', '=', self.alumno_id.id), ('tiene_expulsion', '=', True)]}

    total_pendientes_grupo = fields.Integer(string='Pendientes en grupo', compute='_compute_total_pendientes_grupo', store=False)

    @api.depends('grupo_id')
    def _compute_total_pendientes_grupo(self):
        for rec in self:
            rec.total_pendientes_grupo = self.search_count([('grupo_id', '=', rec.grupo_id.id), ('gravedad', '=', 'pendiente_llamar')]) if rec.grupo_id else 0

    def action_ver_pendientes_grupo(self):
        self.ensure_one()
        return {'name': 'Pendientes de ' + (self.grupo_id.name or ''), 'type': 'ir.actions.act_window',
                'res_model': 'parte', 'view_mode': 'tree,form', 'domain': [('grupo_id', '=', self.grupo_id.id), ('gravedad', '=', 'pendiente_llamar')]}

    _sql_constraints = [('unique_alumno_fecha', 'UNIQUE(alumno_id, fecha_hora)', 'Ya existe un parte para este alumno en esa misma fecha y hora exacta.')]

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

    @api.constrains('alumno_id', 'grupo_id')
    def _check_alumno_grupo(self):
        for rec in self:
            if rec.alumno_id and rec.grupo_id:
                if rec.alumno_id.grupo_id and rec.alumno_id.grupo_id != rec.grupo_id:
                    raise ValidationError('El alumno "%s" pertenece al grupo "%s", no al grupo "%s".' % (
                        rec.alumno_id.name, rec.alumno_id.grupo_id.name, rec.grupo_id.name))

    @api.constrains('tiene_expulsion', 'gravedad')
    def _check_expulsion_gravedad(self):
        for rec in self:
            if rec.tiene_expulsion and rec.gravedad == 'pendiente_llamar':
                raise ValidationError('Un parte con expulsión no puede quedar como "Pendiente Contactar". Márcalo como "Contactado" o "Cerrado".')


class ParteLlamada(models.Model):
    _name = 'parte.llamada'
    _description = 'Registro de llamadas a padres'
    _order = 'fecha desc'

    parte_id  = fields.Many2one('parte', string='Parte', required=True, ondelete='cascade')
    fecha     = fields.Datetime(string='Fecha y hora', default=fields.Datetime.now, required=True)
    resultado = fields.Selection([
        ('contactado',      'Contactado — familia notificada'),
        ('no_contesta',     'No contesta'),
        ('buzon',           'Saltó el buzón de voz'),
        ('cita_presencial', 'Cita presencial acordada'),
    ], string='Resultado', required=True)
    notas = fields.Char(string='Notas breves')

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if rec.resultado == 'contactado' and rec.parte_id:
            rec.parte_id.gravedad = 'llamado'
        return rec