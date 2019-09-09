#!/usr/bin/env python3

from datetime import datetime
from DBConn import *
from sqlalchemy.orm import relationship, backref

Base = get_base()


class Person(Base):
    __tablename__ = "associados"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    nome = sqlalchemy.Column(sqlalchemy.String(length=100))
    endereco = sqlalchemy.Column(sqlalchemy.String(length=200))
    ocupacao = sqlalchemy.Column(sqlalchemy.String(length=60))
    email = sqlalchemy.Column(sqlalchemy.String(length=100), unique=True)
    ativo = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now())
    inativo = sqlalchemy.Column(sqlalchemy.Date)
    annuals = relationship("Annual", secondary="associadoanual", back_populates="associados")

    def __repr__(self):
        return "<Associado(id={0}, name='{1}', address='{2}', occupation='{3}', email='{4}', ativo='{5}')>".format(
            self.id, self.nome, self.endereco, self.ocupacao, self.email, self.ativo)


class Annual(Base):
    __tablename__ = 'anuario'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    titulo = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    cota = sqlalchemy.Column(sqlalchemy.DECIMAL)
    corrente = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    associados = relationship("Person", secondary="associadoanual", back_populates="annuals")

    def __repr__(self):
        return "<Anual(id={0}, titulo='{1}', cota='{2}', corrente='{3}')>".format(
            self.id, self.titulo, self.cota, self.corrente)


class AssociadoAnual(Base):
    __tablename__ = 'associadoanual'
    associadoId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('associados.id'), primary_key=True)
    anuarioId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('anuario.id'), primary_key=True)
    associado = relationship(Person, backref=backref("ano_assoc"))
    ano = relationship(Annual, backref=backref("associado_assoc"))
    jan = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    fev = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    mar = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    abr = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    mai = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    jun = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    jul = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    ago = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    sep = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    oct = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    nov = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    dez = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return "<AssociadoAnual(associadoId='{0}', anuarioId='{1}', jan='{2}', fev='{3}')>".format(
            self.associadoId, self.anuarioId, self.jan, self.fev)


class Mapeador(object):

    def __init__(self, nome, email, jan, fev, mar, abr, mai, jun, jul, ago, sep, out, nov, dez):
        self.nome = nome
        self.email = email
        self.jan = jan
        self.fev = fev
        self.mar = mar
        self.abr = abr
        self.mai = mai
        self.jun = jun
        self.jul = jul
        self.ago = ago
        self.sep = sep
        self.out = out
        self.nov = nov
        self.dez = dez

    def __repr__(self):
        return "<Mapeador(nome={0}, email={1}, jan={2}, fev={3}, mar={4}, abr={5}, mai={6}, jun={7}," \
               "jul={8}, ago={9}, sep={10}, out={11}, nov={12}, dec={13})>".format(
            self.nome, self.email, self.jan, self.fev, self.mar, self.abr, self.mai, self.jun,
            self.jul, self.ago, self.sep, self.out, self.nov, self.dez)

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_jan(self):
        return self.jan

    def set_jan(self, jan):
        self.jan = jan

    def get_fev(self):
        return self.fev

    def set_fev(self, fev):
        self.fev = fev

    def get_mar(self):
        return self.mar

    def set_mar(self, mar):
        self.mar = mar

    def get_abr(self):
        return self.abr

    def set_abr(self, abr):
        self.abr = abr

    def get_mai(self):
        return self.mai

    def set_mai(self, mai):
        self.mai = mai

    def get_jun(self):
        return self.jun

    def set_jun(self, jun):
        self.jun = jun

    def get_jul(self):
        return self.jul

    def set_jul(self, jul):
        self.jul = jul

    def get_ago(self):
        return self.ago

    def set_ago(self, ago):
        self.ago = ago

    def get_sep(self):
        return self.sep

    def set_sep(self, sep):
        self.sep = sep

    def get_out(self):
        return self.out

    def set_out(self, out):
        self.out = out

    def get_nov(self):
        return self.nov

    def set_nov(self, nov):
        self.nov = nov

    def get_dez(self):
        return self.dez

    def set_dez(self, dez):
        self.dez = dez