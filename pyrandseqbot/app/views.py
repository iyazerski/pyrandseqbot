from telegram.chataction import ChatAction
from telegram.update import Update

from pyrandseqbot.app import controllers
from pyrandseqbot.app.utils import before_handler


@before_handler(ChatAction.TYPING)
def start(update: Update):
    controllers.start(update)


@before_handler(ChatAction.TYPING)
def mention(update: Update):
    controllers.mention(update)


@before_handler(ChatAction.TYPING)
def add_sequence(update: Update):
    controllers.add_sequence(update)


@before_handler(ChatAction.TYPING)
def get_random_sequence(update: Update):
    controllers.get_random_sequence(update)


@before_handler(ChatAction.TYPING)
def clear_sequence(update: Update):
    controllers.clear_sequence(update)
