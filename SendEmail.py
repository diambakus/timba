import smtplib
from email.mime.text import MIMEText
from configparser import ConfigParser

SUBJECT = '[FAGUIBB] Alerta de cota em atraso'


def read_database_config(filename='config.ini', section='email'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


# Envio de email a um inademplente
def send_email(email, data_limite_pagamento):
    config_db = read_database_config()
    gmailaddress = config_db['endereco']
    gmailpassword = config_db['senha']
    mailto = email
    content = 'Prezado(a) assoaciado(a)!\n\n Escrevemos para informar que a sua cota, referente a %s, estah em ' \
              'atraso. ' \
              'Por favor, pague a cota em atraso.\n\n  Cumprimentos, \n Gerencia' % data_limite_pagamento
    message = 'Subject: {}\n\n{}'.format(SUBJECT, content)
    mailServer = smtplib.SMTP(config_db['servidor'], config_db['porta'])
    mailServer.starttls()
    mailServer.login(gmailaddress, gmailpassword)
    mailServer.sendmail(gmailaddress, mailto, message)
    mailServer.quit()
