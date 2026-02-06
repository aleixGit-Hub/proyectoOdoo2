# -*- coding: utf-8 -*-
{
    'name': "Gestión de Partes de Incidentes",
    'version': '1.2',
    'category': 'Educación',
    'author': "Aleix, Jorge y Adam",
    'website': "https://foremp.edu.gva.es/",
    'summary': 'Gestión de incidencias y partes de expulsión',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',        # 1º Se crean los grupos
        'security/ir.model.access.csv', # 2º Se dan permisos a esos grupos
        'views/views.xml',              # 3º Se pintan las vistas
    ],
    'application': True,
    'installable': True,
}