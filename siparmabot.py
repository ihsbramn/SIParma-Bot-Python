from pprint import pprint
from telepot.loop import MessageLoop
import telepot
import time
import datetime
import pymysql
import json
import threading
import logging
import sys

db = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    db='siparma_db'
)
cursor = db.cursor()

# auth
bot = telepot.Bot('token')
chatid = ('chatid')
# auth

print('connect succeed at ' + str(db))

bot.sendMessage(
    chatid, 'Selamat datang di BMW-Semarang Bot \nBMW-Semarang  Siap Membantu anda! 😉 ')


def handle(msg):
    sender_id = msg['from']['id']
    sender_username = msg['from']['username']
    sender_name = msg['from']['first_name']
    id_group = msg['chat']['id']
    text = msg['text']
    args = text.split()
    command = args[0]
    status = ('open')
    msg_id = msg['message_id']

    if command == '/start':
        bot.sendMessage(
            chatid, 'Selamat datang di BMW-Semarang Bot \nBMW-Semarang  Siap Membantu anda! 😉 ')

    if command == '/moban':
        if args[1] == '#AO' or args[1] == '#MO' or args[1] == '#GGN' or args[1] == '#PDA' or args[1] == '#MIG':
            db.commit()
            host = str(args[1]), str(args[2]), str(
                args[3]), str(args[4]), str(sender_id), str(sender_username), str(sender_name), str(status), str(msg_id), str(id_group)
            cursor.execute(
                "INSERT INTO reports(report_type,report_number,report_value,report_detail,report_idsender,report_sender,sender_name,report_status,msg_id,id_group) VALUE('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (host))
            db.commit()
            bot.sendMessage(
                chatid, 'Moban Diterima! 👍' + '\n' + '\nID Moban : ' + str(cursor.lastrowid) + '\nID Pengirim : ' + str(sender_id) + '\nUsername Pengirim : ' + '@'+sender_username + '\n \nStatus : ' + status)
        else:
            bot.sendMessage(
                chatid, 'Format Salah ❗️ \n \nSilahkan input dengan format berikut : \n Contoh : /moban #MO #SC123456 #ganti router \n \n Jenis Order : \n-#AO\n-#GGN\n-#MO\n-#PDA\n-#MIG')

    if command == '/cekid':
        db.commit()
        host = str(args[1])
        cursor.execute(
            "SELECT * FROM reports WHERE id = '%s'" % (host))
        hasil = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in hasil:
                output = "Data Ditemukan 😉" + '\n' + "\nID Moban : " + \
                    str(row[0]) + "\nJenis Order : " + row[1] + "\nNo Order : " + row[2] + \
                    '\nUsername Pelapor : ' + '@' + \
                    row[6] + '\nNama Pelapor : ' + \
                    row[7] + '\nKeluhan : '+row[3] + ' ' + \
                    row[4] + '\n\nUpdate by : ' + '\n\n(OPEN->OGP) : ' + str(row[10]) + '\n(OGP->ESKALASI) : ' + str(row[11]) + '\n(OGP->CLOSED) : ' + str(row[12]) + '\n(ESKALASI->CLOSED) : ' + str(row[13]) + '\n\nWaktu Terakhir Update : \n' + \
                    str(row[18]) + '\nStatus : ' + row[8]
        else:
            output = "Data ID Moban " + host + " Tidak ditemukan ☹️"

        bot.sendMessage(
            chatid, output)

    if command == '/cekno':
        db.commit()
        host = str(args[1])
        cursor.execute(
            "SELECT * FROM reports WHERE report_number = '%s'" % (host))
        hasil = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in hasil:
                output = "Data Ditemukan 😉" + '\n' + "\nID Moban : " + \
                    str(row[0]) + "\nJenis Order : " + row[1] + "\nNo Order : " + row[2] + \
                    '\nUsername Pelapor : ' + '@' + \
                    row[6] + '\nNama Pelapor : ' + \
                    row[7] + '\nKeluhan : '+row[3] + ' ' + \
                    row[4] + '\nUpdate by : ' + '\n\n(OPEN->OGP) : ' + str(row[10]) + '\n(OGP->ESKALASI) : ' + str(row[11]) + '\n(OGP->CLOSED) : ' + str(row[12]) + '\n(ESKALASI->CLOSED) : ' + str(row[13]) + '\n\nWaktu Terakhir Update : \n' + \
                    str(row[18]) + '\nStatus : ' + row[8]
        else:
            output = "Data ID Moban " + host + " Tidak ditemukan ☹️"

        bot.sendMessage(
            chatid, output)

    if command == '/testid':
        db.commit()
        print(json.dumps(msg, indent=4, sort_keys=True))
        bot.sendMessage(
            chatid, 'ID Group : ' + str(id_group) + '\nID Pengirim : ' + str(sender_id) + '\nUsername Pengirim : ' + '@'+sender_username + '\nNama Pengirim : ' + str(sender_name))

    if command == '/help':
        bot.sendMessage(
            chatid, 'BMW-Semarang  Bot \n \n- Format Moban \n /moban<spasi>#jenisorder<spasi>#(no-order)<spasi>#(deskripsi) \n\n Contoh : /moban #MO #SC123456 #ganti router \n \n Jenis Order : \n-#AO\n-#GGN\n-#MO\n-#PDA\n-#MIG \n \n- Format Cek Moban  \n /cekid (ID Moban)\n /cekno (No Order / No SC)')


# get date
datetime.datetime.now()

# logging
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


# check db
def printit():

    threading.Timer(30.0, printit).start()
    print('Check DB Connection ' + str(db) +
          ' Time : ' + str(datetime.datetime.now()))


printit()

# bot msg loop
MessageLoop(bot, handle).run_as_thread()

# RUNN
while 1:
    time.sleep(10)
# RUNN
