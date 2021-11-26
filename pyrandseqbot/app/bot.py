import logging

from telegram import Bot as TelegramBot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from pyrandseqbot.configs import BotConfigs

_logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, configs: BotConfigs):
        self.updater = Updater(configs.token)
        self.dp = self.updater.dispatcher
        self.bot: TelegramBot = self.updater.bot
        self.name = configs.name
        self.configs = configs

    def run(self):
        from pyrandseqbot.app import views

        self.dp.add_handler(CommandHandler('start', views.start))
        self.dp.add_handler(CommandHandler('help', views.start))
        self.dp.add_handler(CommandHandler('get_random_sequence', views.get_random_sequence))
        self.dp.add_handler(CommandHandler('clear_sequence', views.clear_sequence))
        self.dp.add_handler(CommandHandler('add_sequence', views.add_sequence))
        self.dp.add_handler(MessageHandler(Filters.regex(r'^@pyRandSeqBot(.+)?'), views.mention))

        _logger.info(f'Telegram bot @{self.name} successfully started')

        self.updater.start_polling()
        self.updater.idle()
