import telepot
import time
import pymysql
import json
import requests
from telepot.loop import MessageLoop
from pprint import pprint

db = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    db='siparma_db'
)
cursor = db.cursor()

# auth
bot = telepot.Bot('1786482522:AAEKQOpHgMgtWV_IVpGv9Ldz6c_j57Eal04')
chatid = ('-478142407')
# auth


bot.sendMessage(
    chatid, 'Selamat datang di SIParmaBot \nSiParma Siap Membantu anda! 😉 ')


def handle(msg):
    sender_id = msg['from']['id']
    sender_username = msg['from']['username']
    text = msg['text']
    args = text.split()
    command = args[0]
    status = ('open')

    if command == '/start':
        bot.sendMessage(
            chatid, 'Selamat datang di SIParmaBot \nSiParma Siap Membantu anda! 😉 ')

    if command == '/moban':
        host = str(args[1]), str(args[2]), str(
            args[3]), str(args[4]), str(sender_id), str(sender_username), str(status)
        cursor.execute(
            "INSERT INTO reports(report_type,report_number,report_value,report_detail,report_idsender,report_usernamesender,report_status) VALUE('%s','%s','%s','%s','%s','%s','%s')" % (host))
        db.commit()
        bot.sendMessage(
            chatid, 'Moban Diterima! 👍' + '\n' + '\nID Moban : ' + str(cursor.lastrowid) + '\nID Pengirim : ' + str(sender_id) + '\nUsername Pengirim : ' + '@'+sender_username + '\nStatus : ' + status)

    if command == '/cek':
        host = str(args[1])
        cursor.execute(
            "SELECT * FROM reports WHERE id = '%s'" % (host))
        hasil = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in hasil:
                output = "Data Ditemukan 😉" + '\n' + "\nID Moban : " + \
                    str(row[0]) + "\nJenis Order : " + row[1] + "\nNo Order : " + row[2] + \
                    '\nUsername Pelapor : ' + '@' + \
                    row[6] + '\nStatus : ' + row[7]
        else:
            output = "Data ID Moban " + host + " Tidak ditemukan ☹️"

        bot.sendMessage(
            chatid, output)

    if command == '/test':
        bot.sendMessage(
            chatid, 'ID Pengirim : ' + str(sender_id) + '\nUsername Pengirim : ' + sender_username)


MessageLoop(bot, handle).run_as_thread()

# RUNN
while 1:
    time.sleep(10)
# RUNN
