# -*- coding: utf-8 -*-
{
    'name': "Gestión de Partes de Incidentes",
    'version': '1.7',
    'category': 'Educación',
    'author': "Aleix, Jorge y Adam",
    'website': "https://foremp.edu.gva.es/",
    'summary': 'Gestión de incidencias graves, partes de expulsión y estadísticas de convivencia',
    'depends': ['base', 'mail'],

    'data': [
        # 1. Seguridad primero
        'security/security.xml',
        'security/ir.model.access.csv',

        # 2. Vistas principales (árbol, formulario, menús base)
        'views/views.xml',

        # 3. Vistas extra: Kanban, Calendario, Gráficos, Búsqueda avanzada
        'views/views_extra.xml',

        # 4. Informes QWeb personalizados
        'reports/reports.xml',

        # 5. Datos precargados (grupos, profesores, alumnos, partes)
        'data/data.xml',
    ],

    'images': ['static/description/icon.png'],

    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}