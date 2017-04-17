#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Oleg Dolgikh
#


import sys
import smtplib


DEBUG = False


def usage(shell):
    if shell == 'python':
        msg = '''Usage:
sendemail.send(mail_server,
               mail_from,
               mail_to,
               mail_subject,
               msg_body,
               mail_user,
               mail_pass,
               ssl_enable)'''
    elif shell == 'bash':
        msg = '''Usage:
echo ${msg} | ./sendemail.py ${mail_server} \\
                             ${mail_from} \\
                             ${mail_to1},${mail_to2} \\
                             ${mail_subject} \\
                             ${mail_user} \\
                             ${mail_pass} \\
                             ${ssl_enable}'''
    print(msg)


def send(mail_server, mail_from, mail_to, mail_subject, msg,
         mail_user=None, mail_pass=None, ssl_enable=False):
    if type(mail_to) == str:
        mail_to = mail_to.split()
    msg = ('From: {0}\r\n'
           'To: {1}\r\n'
           'Subject: {2}\r\n'
           '{3}'.format(mail_from, ",".join(mail_to), mail_subject, msg))
    smtp_connect = smtplib.SMTP(mail_server)
    try:
        if DEBUG is True:
            smtp_connect.set_debuglevel(2)
        if ssl_enable is True:
            smtp_connect.starttls()
        if mail_user is not None and mail_pass is not None:
            smtp_connect.login(mail_user, mail_pass)
        smtp_connect.sendmail(mail_from, mail_to, msg)
    finally:
        smtp_connect.quit()


if __name__ == '__main__':
    try:
        mail_server = sys.argv[1]
        mail_from = sys.argv[2]
        mail_to = sys.argv[3]
        mail_subject = sys.argv[4]
    except IndexError:
        usage('bash')
        exit()
    try:
        mail_user = sys.argv[5]
        if mail_user == 'None':
            mail_user = None
    except IndexError:
        mail_user = None
    try:
        mail_pass = sys.argv[6]
        if mail_pass == 'None':
            mail_pass = None
    except IndexError:
        mail_pass = None
    try:
        ssl_enable = bool(sys.argv[7])
    except IndexError:
        ssl_enable = False
    msg = ''
    for line in sys.stdin:
        msg += line
    if type(mail_to) == str:
        mail_to = mail_to.split(',')
    send(mail_server, mail_from, mail_to, mail_subject, msg,
         mail_user, mail_pass, ssl_enable)
