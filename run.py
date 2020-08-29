import argparse

from pyrandseqbot.api.bot import bot
from pyrandseqbot.configs import configs
from pyrandseqbot.orm.connection import db

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--configs', help='Path to configs file', default=None)
    args = arg_parser.parse_args()

    configs.load(config_path=args.configs)
    db.connect(connection_string=configs.orm.connection_string)
    bot.start(token=configs.api.token)
