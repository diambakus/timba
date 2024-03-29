#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from flask import Flask, render_template, request, url_for, redirect
from ControllerAction import *
from babel.numbers import format_currency
from utils import *
from SendEmail import *
from pyfladesk import init_gui

base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)
app = Flask(__name__,
        static_folder = os.path.join(base_dir, 'static'),
        template_folder = os.path.join(base_dir, 'templates'))

membros = proverAssociados()
annual_enrolled_members = {}
enrolled_members_status = {}


@app.route('/')
def main():
    ano_corrente = recuperar_ano_aberto()
    return render_template('dashboard.html', ano_corrente=ano_corrente)


@app.route('/dashboard')
def dashboard():
    return redirect(url_for('main'))


@app.route('/user/<name>')
def user(name):
    return '<h3>Halo, %s!</h3>' % name


@app.route('/create_annual_data', methods=['POST'])
def create_annual_data():
    ano_corrente = recuperar_ano_aberto()
    if ano_corrente:
        return render_template('dashboard.html', ano_corrente=ano_corrente, warning="Atenção! Por favor, "
                                                                                    "feche o anuário em aberto antes de abrir um novo.")
    else:
        todos_anos = annuals()
        titulo = request.form['titulo']
        cota = request.form['cota']
        anoFlag = isAnoExistInDB(titulo, todos_anos)
        if anoFlag is False:
            ano_corrente = add_annual(titulo, cota)
            return redirect(url_for('main'))
        else:
            return render_template('dashboard.html', ano_corrente=ano_corrente,
                                   warning="Atenção! Anuário %s já existe." % titulo)


@app.route('/update_ano/', methods=['POST'])
def update_ano():
    titulo = request.form['retitulo']
    ano = recuperar_ano(titulo)
    cota_aux = request.form['cota']
    corrente_aux = request.form['corrente']
    if corrente_aux == str('fechado'):
        status_flag = False
    else:
        status_flag = True
    if ano:
        if cota_aux and cota_aux != ano.cota:
            ano.cota = cota_aux
        if corrente_aux and status_flag != ano.corrente:
            outro_ano_corrente = recuperar_ano_aberto()
            if outro_ano_corrente.titulo == ano.titulo:
                ano.corrente = status_flag
        updateAnnualByTitulo(ano.titulo, ano.cota, ano.corrente)
    if status_flag == True:
        return redirect(url_for('display_ano', titulo=ano.titulo))
    else:
        return render_template('dashboard.html', success="A pasta correspondente ao ano %s foi fechada." % titulo)


@app.route('/ano/<titulo>')
def display_ano(titulo):
    ano_corrente = recuperar_ano_aberto()
    enrolled_members_status[ano_corrente.id] = construir_mapa(ano_corrente.id)
    membros_nao_inscritos = list_of_member_not_enrolled_yet(membros, enrolled_members_status[ano_corrente.id])
    return render_template('anuario.html', membros=membros, ano_corrente=ano_corrente,
                           membros_nao_inscritos=membros_nao_inscritos, membros_inscritos=
                           enrolled_members_status[ano_corrente.id],
                           total_monetario=format_currency(ano_corrente.montante, 'EUR', locale='de_DE'))


@app.route('/associados')
def associados():
    ano_corrente = recuperar_ano_aberto()
    return render_template('associados.html', membros=membros, ano_corrente=ano_corrente)


@app.route('/create_member', methods=['POST'])
def create_member():
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    ocupacao = request.form['ocupacao']
    email = request.form['email']
    membro = add_member(nome, endereco, ocupacao, email, telefone)
    membros.append(membro)
    return redirect(url_for('associados'))


@app.route('/annual_enrollment', methods=['POST', 'GET'])
def annual_enrollment():
    checked_members = request.form.getlist('check')
    titulo = request.form['titulo']
    ano = recuperar_ano(titulo)
    annual_enrolled_members[titulo] = make_enrollment(ano.id, checked_members)
    return redirect(url_for('display_ano', titulo=titulo))


@app.route('/update_member_portfolio', methods=['POST', 'GET'])
def update_member_portfolio():
    titulo = request.form['titulo']
    email = request.form['email']
    checked_months = request.form.getlist('check')
    update_member_enrollment_status(email, titulo, checked_months)
    return redirect(url_for('display_ano', titulo=titulo))


@app.route('/registrar_despesa/<titulo>', methods=['POST'])
def registrar_despesa(titulo):
    pass
    ano = recuperar_ano_aberto()
    if ano.titulo != int(titulo):
        return render_template('dashboard.html', warning="O ano(%) em URL é inválido" % titulo)
    else:
        valor_gasto = request.form['valor_despesa']
        nota = request.form['nota_despesa']
        data_da_despesa = request.form['data_despesa']
        despesa = add_expense(valor_gasto, nota, titulo, datetime.strptime(data_da_despesa, "%d/%m/%Y"))
        return redirect(url_for('display_ano', titulo=titulo))


@app.route('/despesas_do_ano/<titulo>')
def despesas_do_ano(titulo):
    despesas = get_expenses(titulo)
    ano_corrente = recuperar_ano_aberto()
    return render_template('despesas.html', despesas=despesas, ano_corrente=ano_corrente)


@app.route('/generate_excel/<titulo>')
def generate_excel(titulo):
    pass
    year = recuperar_ano(titulo)
    lista = construir_mapa(year.id)
    filename = "Members_Status_"+str(titulo)+".xls"
    output_to_excel(filename, lista, "Members Status")
    return redirect(url_for('display_ano', titulo=titulo))


@app.route('/send_email_reminder', methods=['POST'])
def send_email_reminder():
    pass
    titulo = request.form['titulo']
    email = request.form['email']
    checked_months = request.form.getlist('check')
    today = datetime.now().date()
    for month in checked_months:
        mes = int(month) * (-1)
        data_contruida_str = titulo+'/'+str(mes)+'/05'
        data_limite_pagamento = datetime.strptime(data_contruida_str, "%Y/%m/%d").date()
        if today > data_limite_pagamento:
            send_email(email, data_limite_pagamento)
    return redirect(url_for('display_ano', titulo=titulo))


@app.route('/anos')
def anos():
    pass
    lista_de_anos = annuals()
    ano_corrente = recuperar_ano_aberto()
    return render_template('anos.html', anos=lista_de_anos, ano_corrente=ano_corrente)


if __name__ == "__main__":
    #app.run(debug=True)
    init_gui(app)
