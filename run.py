from pyrandseqbot.processors import bot, db

if __name__ == '__main__':
    db.connect()
    bot.run()
