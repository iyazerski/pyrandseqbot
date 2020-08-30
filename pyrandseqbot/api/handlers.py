import logging
import random
from functools import wraps

from telegram.chataction import ChatAction

from pyrandseqbot.orm.crud import ChatCrud

_logger = logging.getLogger(__name__)


def before_handler(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            _logger.info(f'Received request from {update.message.from_user.name}')
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


@before_handler(ChatAction.TYPING)
def start(update, context):
    update.message.reply_text(
        'pyRandSeqBot случайным образом формирует очередь для введенного списка (например, очередность спикеров '
        'на выступлении). Введенные данные сохранятся для дальнейшего использования\n'
        '\nКоманды\n'
        '\n/start и /help - показать это сообщение\n'
        '@pyRandSeqBot элемент1, элемент2 - добавить данные (список элементов разделенных запятой)\n'
        '/get_random_sequence - перемешать данные\n'
        '/clear_sequence - удалить данные из бота'
    )


@before_handler(ChatAction.TYPING)
def mention(update, context):
    sequence = list(filter(None, [el.strip() for el in update.message.text.replace('@pyRandSeqBot', '').split(',')]))
    if sequence:
        crud = ChatCrud()
        chat = crud.read(chat_id=update.message.chat_id) or crud.create(chat_id=update.message.chat_id)
        chat.sequence = sequence
        crud.update(chat)
    return get_random_sequence(update, context)


@before_handler(ChatAction.TYPING)
def add_sequence(update, context):
    update.message.reply_text(
        'Чтобы добавить данные, отправьте ссобщение в следующем формате:\n'
        '\n@pyRandSeqBot элемент1, элемент2, элемент3'
    )


@before_handler(ChatAction.TYPING)
def get_random_sequence(update, context):
    chat = ChatCrud().read(chat_id=update.message.chat_id)
    if not chat or not chat.sequence:
        update.message.reply_text(
            'Сначала добавьте данные. Для этого отправьте ссобщение в следующем формате:\n'
            '\n@pyRandSeqBot элемент1, элемент2, элемент3'
        )
    else:
        random.shuffle(chat.sequence)
        update.message.reply_text('\n'.join(f'{i + 1}. {el}' for i, el in enumerate(chat.sequence)))


@before_handler(ChatAction.TYPING)
def clear_sequence(update, context):
    crud = ChatCrud()
    chat = crud.read(chat_id=update.message.chat_id)
    if not chat:
        update.message.reply_text('Удалять нечего, Вы еще ничего не добавляли :)')
    else:
        chat.sequence = None
        crud.update(chat)
        update.message.reply_text('Удалил все введенные Вами данные')
