from functools import wraps

from telegram import Update

from pyrandseqbot.processors import bot


def before_handler(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update: Update, *_, **__):
            bot.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update)

        return command_func

    return decorator
