#!/usr/bin/python
import config
import telegram
import os
import subprocess
import sys
import shlex
import datetime
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload

from telegram.ext import Updater
updater = Updater(token=config.token)
dispatcher = updater.dispatcher

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    global textoutput
    textoutput = ''
    while True:
        global output
        output = process.stdout.readline()
        output = output.decode('utf8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())
        textoutput = textoutput + '\n' + output.strip()
    rc = process.poll()
    return rc

def start(update, context):
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Привет, Я бот мониторинг сервера.')

def help(update, context):
    reload(config)
    context.bot.sendMessage(chat_id=update.message.chat_id, text='''список доступных команд:
    /id - id пользователя
    /ifconfig - информация о конфигурации сети
    /vnstat - Статистика использвоания трафика
    /wgshow - Пользователи VPN
    /addwguser - Добавить пользователя VPN
    /reboot - Перезагрузить сервер
    ''')

#функция команады id
def myid(update, context):
    userid = update.message.from_user.id
    context.bot.sendMessage(chat_id=update.message.chat_id, text= 'Твой ID:' userid)

#функция команады ifconf
def ifconfig(update, context):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin: #Если в confog.py - id админа, то команда выполниться
        run_command("ifconfig")
        context.bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

ifconfig_handler = CommandHandler('ifconfig', ifconfig)
dispatcher.add_handler(ifconfig_handler)

myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

updater.start_polling()
