# -*- coding: utf-8 -*-

import logging

from odoo import fields, models, api
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class Presupuesto(models.Model):
    _name = "presupuesto"
    _inherit = ['image.mixin']
    name = fields.Char(string='Pelicula')
    clasificacion = fields.Selection(selection=[
        ('General','G'),# Publico general
        ('PG','PG'),# Se recomienda compañia de adulto
        ('PG-13', 'PG-13'),#Mayores de 13 años
        ('R','R'),# En compañia de un adulto obligatorio
        ('NC-17', 'NC-17'),# Mayores de 18
    ], string='Clasificación')
    dsc_clasificacion = fields.Char(string='Descripción')
    fch_estreno=fields.Date(string='Fecha de estreno')
    puntuacion = fields.Integer(string='Puntuación', related="puntuacion2")
    puntuacion2 = fields.Integer(string='Puntuación2')
    active = fields.Boolean(string='Activo', default=True)
    director_id = fields.Many2one(
        comodel_name='res.partner',
        string='Director'
    )
    categoria_director_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Categoria Director',

        # primera version
        # default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')])
        # segunda version
        default=lambda self: self.env.ref('peliculas.category_director')

    )

    genero_ids=fields.Many2many(
        comodel_name='genero',
        string='Genero'
    )
    vista_general = fields.Text('Descripción')
    link_trailer = fields.Char(string='Trailer')
    es_libro = fields.Boolean (string='Version Libro')
    libro = fields.Binary (string='Libro')
    libro_filename = fields.Char(string='Nombre del libro')

    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),
        ], default='borrador', string='Estados', copy=False)
    fch_aprobado = fields.Datetime(string='Fecha aprobado', copy=False)

    def aprobar_presupuesto(self):
        logger.info('***************Entro a la función Aprobar presupuesto')
        self.state='aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        self.state = 'cancelado'

    def unlink(self):
        logger.info('*****************Se disparó el borrado de Ficha')
        if self.state == 'cancelado':
            super(Presupuesto, self).unlink()
        else:
            logger.info('******** no eliminar el registro porque no se encuentra en estado de Cancelado')
    