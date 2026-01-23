# -*- coding: utf-8 -*-
# from odoo import http


# class Incidentes(http.Controller):
#     @http.route('/incidentes/incidentes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/incidentes/incidentes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('incidentes.listing', {
#             'root': '/incidentes/incidentes',
#             'objects': http.request.env['incidentes.incidentes'].search([]),
#         })

#     @http.route('/incidentes/incidentes/objects/<model("incidentes.incidentes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('incidentes.object', {
#             'object': obj
#         })
