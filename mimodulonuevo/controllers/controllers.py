# -*- coding: utf-8 -*-
# from odoo import http


# class Mimodulonuevo(http.Controller):
#     @http.route('/mimodulonuevo/mimodulonuevo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mimodulonuevo/mimodulonuevo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mimodulonuevo.listing', {
#             'root': '/mimodulonuevo/mimodulonuevo',
#             'objects': http.request.env['mimodulonuevo.mimodulonuevo'].search([]),
#         })

#     @http.route('/mimodulonuevo/mimodulonuevo/objects/<model("mimodulonuevo.mimodulonuevo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mimodulonuevo.object', {
#             'object': obj
#         })
