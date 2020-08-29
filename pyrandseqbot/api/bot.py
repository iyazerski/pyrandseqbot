import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

_logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.dp = None
        self.updater = None

    def start(self, token: str):
        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher

        from pyrandseqbot.api import handlers
        self.dp.add_handler(CommandHandler('start', handlers.start))
        self.dp.add_handler(CommandHandler('help', handlers.start))
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handlers.start))
        _logger.info('Telegram bot successfully started')

        self.updater.start_polling()
        self.updater.idle()


bot = Bot()
