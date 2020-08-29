from pyrandseqbot.api.bot import bot

if __name__ == '__main__':
    bot.updater.start_polling()
    bot.updater.idle()
