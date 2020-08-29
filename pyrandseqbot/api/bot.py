import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from pyrandseqbot.configs import configs
from pyrandseqbot.orm.connection import db

_logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        if not configs.loaded:
            configs.load()
        if not db.connected:
            db.connect(configs.orm.connection_string)

        self.updater = Updater(configs.api.token, use_context=True)
        self.dp = self.updater.dispatcher

        from pyrandseqbot.api import routes
        self.dp.add_handler(CommandHandler('start', routes.start))
        self.dp.add_handler(CommandHandler('help', routes.start))
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, routes.start))

        _logger.info('Telegram bot successfully started')


bot = Bot()
