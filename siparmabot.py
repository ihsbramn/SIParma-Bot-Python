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


bot.sendMessage(chatid, 'Selamat Datang! ')


def handle(msg):
    text = msg['text']
    args = text.split()
    command = args[0]
    response = bot.getUpdates()

    if command == '/start':
        bot.sendMessage(
            chatid, 'Selamat datang di SIParmaBot \nSiParma Siap Membantu anda! 😉 ')

    if command == '/moban':
        host = str(args[1]), str(args[2]), str(args[3])
        cursor.execute(
            "INSERT INTO moban(title,status,date) VALUE('%s','%s','%s')" % (host))
        db.commit()
        bot.sendMessage(
            chatid, 'Data Diterima!')

    if command == '/test':
        bot.sendMessage(
            chatid, response)


MessageLoop(bot, handle).run_as_thread()

# RUNN
while 1:
    time.sleep(10)
# RUNN
