#!/usr/bin/env python3

from models import *
from sqlalchemy import and_

engine = get_engine()

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

session = Session()


def get_session():
    return session


def close_session():
    session.close()


def isAnoExistInDB(titulo, anos):
    pass
    flag = False
    for i in anos:
        if i.titulo == int(titulo):
            return True
    return flag


def add_annual(titulo, cota):
    ano = Annual(titulo=titulo, cota=cota)
    session.add(ano)
    session.commit()
    return ano


def annuals():
    return session.query(Annual).all()


def updateAnnualByTitulo(titulo, cota, corrente):
    ano = session.query(Annual).filter(Annual.titulo == titulo).first()
    ano.corrente = corrente
    ano.cota = cota
    session.commit()


def recuperar_ano(titulo):
    pass
    return session.query(Annual).filter(Annual.titulo == titulo).first()


def recuperar_ano_aberto():
    pass
    return session.query(Annual).filter(Annual.corrente == True).first()


# Associados
def proverAssociados():
    return session.query(Person).all()


def add_member(nome, endereco, ocupacao, email):
    associado = Person(nome=nome, endereco=endereco, ocupacao=ocupacao, email=email)
    session.add(associado)
    session.commit()
    return associado


def get_enrolled_members(annualID):
    pass
    return session.query(Person).filter(Person.annuals.any(id=annualID)).all()


def list_of_member_not_enrolled_yet(members, enrolled_members):
    lista = []
    for item in enrolled_members:
        assoc = retrieve_member_by_email(item.email)
        print(assoc)
        lista.append(retrieve_member_by_email(item.email))
    return set(members).difference(set(lista))


def retrieve_member_byId(id):
    pass
    return session.query(Person).filter(Person.id == id).first()


def retrieve_member_by_email(email):
    pass
    return session.query(Person).filter(Person.email == email).first()


def is_enrolled_member(item, list):
    return item in list


def make_enrollment(annualID, candidatesID):
    ano_aberto = recuperar_ano_aberto()
    candidates = []
    for identifier in candidatesID:
        candidate = retrieve_member_byId(identifier)
        if candidate not in candidates:
            candidates.append(candidate)
    for candidate in candidates:
        ano_aberto.associados.append(candidate)
    session.commit()
    return get_enrolled_members(annualID)


def get_enrolled_member_via_assoc_table(annualID):
    pass
    enrolled_members = session.query(AssociadoAnual).join(Annual).filter(Annual.id == annualID).all()
    return enrolled_members


def construir_mapa(id_):
    pass
    lista = []
    membros = get_enrolled_member_via_assoc_table(id_)
    for membro in membros:
        associado = retrieve_member_byId(membro.associadoId)
        lista.append(Mapeador(associado.nome, associado.email, membro.jan,
                             membro.fev, membro.mar, membro.abr, membro.mai,
                             membro.jun, membro.jul, membro.ago, membro.sep,
                             membro.oct, membro.nov, membro.dez))
    return lista


def update_member_enrollment_status(email, titulo, months_status):
    member = retrieve_member_by_email(email)
    year = recuperar_ano(titulo)
    member_enrollment_instance = session.query(AssociadoAnual).join(Annual).join(Person).\
        filter(and_(Annual.id == year.id, Person.id == member.id)).first()
    print("HHHHHHHHHHHHHHHHHHHHHHH", member_enrollment_instance)
    print("Month status", months_status)
    for month in months_status:
        month_integer = int(month)
        if month_integer == -1:
            member_enrollment_instance.jan = True
        elif month_integer == 1:
            member_enrollment_instance.jan = False
        elif month_integer == -2:
            member_enrollment_instance.fev = True
        elif month_integer == 2:
            member_enrollment_instance.fev = False
        elif month_integer == -3:
            member_enrollment_instance.mar = True
        elif month_integer == 3:
            member_enrollment_instance.mar = False
        elif month_integer == -4:
            member_enrollment_instance.abr = True
        elif month_integer == 4:
            member_enrollment_instance.abr = False
        elif month_integer == -5:
            member_enrollment_instance.mai = True
        elif month_integer == 5:
            member_enrollment_instance.mai = False
        elif month_integer == -6:
            member_enrollment_instance.jun = True
        elif month_integer == 6:
            member_enrollment_instance.jun = False
        elif month_integer == -7:
            member_enrollment_instance.jul = True
        elif month_integer == 7:
            member_enrollment_instance.jul = False
        elif month_integer == -8:
            member_enrollment_instance.ago = True
        elif month_integer == 8:
            member_enrollment_instance.ago = False
        elif month_integer == -9:
            member_enrollment_instance.sep = True
        elif month_integer == 9:
            member_enrollment_instance.sep = False
        elif month_integer == -10:
            member_enrollment_instance.oct = True
        elif month_integer == 10:
            member_enrollment_instance.oct = False
        elif month_integer == -11:
            member_enrollment_instance.nov = True
        elif month_integer == 11:
            member_enrollment_instance.nov = False
        elif month_integer == -12:
            member_enrollment_instance.dez = True
        elif month_integer == 12:
            member_enrollment_instance.dez = False
    session.commit()
