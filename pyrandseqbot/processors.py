from pyrandseqbot.app import Bot
from pyrandseqbot.configs import Configs
from pyrandseqbot.orm import Database

configs = Configs.from_package(__file__)
db = Database(configs=configs.db)
bot = Bot(configs=configs.bot)
