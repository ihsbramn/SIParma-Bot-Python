import telepot
import time
import pymysql
import json
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
bot = telepot.Bot('BOT_TOKEN')
chatid = ('ID_GROUP')
# auth

print('connect succeed at ' + str(db))

bot.sendMessage(
    chatid, 'Selamat datang di SIParmaBot \nSiParma Siap Membantu anda! 😉 ')


def handle(msg):
    sender_id = msg['from']['id']
    sender_username = msg['from']['username']
    sender_name = msg['from']['first_name']
    id_group = msg['chat']['id']
    text = msg['text']
    args = text.split()
    command = args[0]
    status = ('open')

    if command == '/start':
        bot.sendMessage(
            chatid, 'Selamat datang di SIParmaBot \nSiParma Siap Membantu anda! 😉 ')

    if command == '/moban':
        db.commit()
        host = str(args[1]), str(args[2]), str(
            args[3]), str(args[4]), str(sender_id), str(sender_username), str(sender_name), str(status)
        cursor.execute(
            "INSERT INTO reports(report_type,report_number,report_value,report_detail,report_idsender,report_sender,sender_name,report_status) VALUE('%s','%s','%s','%s','%s','%s','%s','%s')" % (host))
        db.commit()
        bot.sendMessage(
            chatid, 'Moban Diterima! 👍' + '\n' + '\nID Moban : ' + str(cursor.lastrowid) + '\nID Pengirim : ' + str(sender_id) + '\nUsername Pengirim : ' + '@'+sender_username + '\n \nStatus : ' + status)

    if command == '/cekid':
        db.commit()
        host = str(args[1])
        cursor.execute(
            "SELECT * FROM reports WHERE id = '%s'" % (host))
        hasil = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in hasil:
                output = "Data Ditemukan 😉" + '\n' + "\nID Moban : " + \
                    str(row[0]) + "\nJenis Order : " + row[1] + "\nSC ID : " + row[2] + \
                    '\nUsername Pelapor : ' + '@' + \
                    row[6] + '\nNama Pelapor : ' + \
                    row[7] + '\nKeluhan : '+row[3] + ' ' + \
                    row[4] + '\n\nUpdate by : ' + '\n\n(OPEN->OGP) : ' + str(row[9]) + '\n(OGP->ESKALASI) : ' + str(row[10]) + '\n(OGP->CLOSED) : ' + str(row[11]) + '\n(ESKALASI->CLOSED) : ' + str(row[12]) + '\n\nWaktu Terakhir Update : \n' + \
                    str(row[18]) + '\nStatus : ' + row[8]
        else:
            output = "Data ID Moban " + host + " Tidak ditemukan ☹️"

        bot.sendMessage(
            chatid, output)

    if command == '/ceksc':
        db.commit()
        host = str(args[1])
        cursor.execute(
            "SELECT * FROM reports WHERE report_number = '%s'" % (host))
        hasil = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in hasil:
                output = "Data Ditemukan 😉" + '\n' + "\nID Moban : " + \
                    str(row[0]) + "\nJenis Order : " + row[1] + "\nSC ID : " + row[2] + \
                    '\nUsername Pelapor : ' + '@' + \
                    row[6] + '\nNama Pelapor : ' + \
                    row[7] + '\nKeluhan : '+row[3] + ' ' + \
                    row[4] + '\nUpdate by : ' + '\n\n(OPEN->OGP) : ' + str(row[9]) + '\n(OGP->ESKALASI) : ' + str(row[10]) + '\n(OGP->CLOSED) : ' + str(row[11]) + '\n(ESKALASI->CLOSED) : ' + str(row[12]) + '\n\nWaktu Terakhir Update : \n' + \
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
            chatid, 'SIParma Bot \n \n- Format Moban \n /moban<spasi>#jenisorder<spasi>#(no-order)<spasi>#(deskripsi) \n Contoh : /moban #AO #SCxxxxx #fallout yyyyy \n \n- Format Cek Moban  \n /cekid (ID Moban)\n /ceksc (#NOSC)')

    # if command == '/kirimbukti':
    #     bot.sendMessage(chatid, 'silahkan kirim file nya ')
    #     response = bot.getUpdates()
    #     aw = (json.dumps(response, indent=4, sort_keys=True))
    #     print(aw)
    #     bot.sendMessage(chatid, aw)


MessageLoop(bot, handle).run_as_thread()

# RUNN
while 1:
    time.sleep(10)
# RUNN
