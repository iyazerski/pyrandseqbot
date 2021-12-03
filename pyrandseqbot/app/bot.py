import logging

from telegram import Bot as TelegramBot
from telegram.error import RetryAfter
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

    def start_webhook(self):
        self.updater.start_webhook(
            listen='0.0.0.0',
            port=self.configs.port,
            url_path=self.configs.token,
            webhook_url=self.configs.webhook_url
        )
        try:
            self.bot.set_webhook(self.configs.webhook_url)
        except RetryAfter:
            pass

    def run(self):
        from pyrandseqbot.app import views

        self.dp.add_handler(CommandHandler('start', views.start))
        self.dp.add_handler(CommandHandler('help', views.start))
        self.dp.add_handler(CommandHandler('get_random_sequence', views.get_random_sequence))
        self.dp.add_handler(CommandHandler('clear_sequence', views.clear_sequence))
        self.dp.add_handler(CommandHandler('add_sequence', views.add_sequence))
        self.dp.add_handler(MessageHandler(Filters.regex(r'^@pyRandSeqBot(.+)?'), views.mention))

        _logger.info(f'Telegram bot @{self.name} successfully started')
        if self.configs.env == 'prod':
            # enable webhooks for prod
            self.start_webhook()
        else:
            self.updater.start_polling()
        self.updater.idle()
