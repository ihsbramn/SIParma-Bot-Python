import telepot
import time
import pymysql
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
chatid = ('CHATROOM_ID')
# auth


bot.sendMessage(
    chatid, 'Selamat datang di SIParmaBot \nSiParma Siap Membantu anda! 😉 ')


def handle(msg):
    text = msg['text']
    args = text.split()
    command = args[0]
    response = bot.getUpdates()
    status = ('open')

    if command == '/start':
        bot.sendMessage(
            chatid, 'Selamat datang di SIParmaBot \nSiParma Siap Membantu anda! 😉 ')

    if command == '/moban':
        host = str(args[1]), str(args[2]), str(status)
        cursor.execute(
            "INSERT INTO reports(report_title,report_value,report_status) VALUE('%s','%s','%s')" % (host))
        db.commit()
        bot.sendMessage(
            chatid, 'Moban Diterima! 👍\nDengan ID : ' + str(cursor.lastrowid) + '\nStatus : ' + status)

    if command == '/cek':
        host = str(args[1])
        cursor.execute(
            "SELECT * FROM reports WHERE id = '%s'" % (host))
        hasil = cursor.fetchall()

        if cursor.rowcount > 0:
            for row in hasil:
                output = "Data Ditemukan " + "\nTitle : " + \
                    row[1] + "\nIsi : " + row[2] + "\nStatus : " + row[3]
        else:
            output = "Title : " + host + " Tidak ditemukan"

        bot.sendMessage(
            chatid, output)

    if command == '/test':
        bot.sendMessage(
            chatid, response)


MessageLoop(bot, handle).run_as_thread()

# RUNN
while 1:
    time.sleep(10)
# RUNN
