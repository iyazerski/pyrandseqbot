import logging
import random

from pyrandseqbot.processors import db

_logger = logging.getLogger(__name__)


def start(update):
    update.message.reply_text(
        'pyRandSeqBot случайным образом формирует очередь для введенного списка (например, очередность спикеров '
        'на выступлении). Введенные данные сохранятся для дальнейшего использования\n'
        '\nКоманды\n'
        '\n/start и /help - показать это сообщение\n'
        '@pyRandSeqBot элемент1, элемент2 - добавить данные (список элементов разделенных запятой)\n'
        '/get_random_sequence - перемешать данные\n'
        '/clear_sequence - удалить данные из бота'
    )


def mention(update):
    sequence = ' '.join(list(filter(
        None,
        [el.strip() for el in update.message.text.replace('@pyRandSeqBot', '').split(',')]
    )))
    if sequence:
        with db.start_session() as session:
            chat = db.read(
                db.models.Chat.chat_id == update.message.chat_id,
                model=db.models.Chat,
                session=session
            ).first()
            if not chat:
                chat = db.create(
                    instance=db.models.Chat(chat_id=update.message.chat_id, sequence=sequence),
                    session=session
                )
            else:
                chat.sequence = sequence
                db.update(instance=chat, session=session)
            return get_random_sequence(update, chat)


def add_sequence(update):
    update.message.reply_text(
        'Чтобы добавить данные, отправьте сообщение в следующем формате:\n'
        '\n@pyRandSeqBot элемент1, элемент2, элемент3'
    )


def get_random_sequence(update, chat: db.models.Chat = None):
    def callback():
        if not chat or not chat.sequence:
            update.message.reply_text(
                'Сначала добавьте данные. Для этого отправьте сообщение в следующем формате:\n'
                '\n@pyRandSeqBot элемент1, элемент2, элемент3'
            )
        else:
            sequence = chat.sequence.split()
            random.shuffle(sequence)
            update.message.reply_text('\n'.join(f'{i + 1}. {el}' for i, el in enumerate(sequence)))

    if not chat:
        with db.start_session() as session:
            chat = db.read(
                db.models.Chat.chat_id == update.message.chat_id,
                model=db.models.Chat,
                session=session
            ).first()
            callback()
    else:
        callback()
    _logger.info(f'Generated random sequence for chat[{chat.chat_id}]')


def clear_sequence(update):
    with db.start_session() as session:
        chat = db.read(
            db.models.Chat.chat_id == update.message.chat_id,
            model=db.models.Chat,
            session=session
        ).first()
        if not chat:
            update.message.reply_text('Удалять нечего, Вы еще ничего не добавляли :)')
        else:
            chat.sequence = None
            db.update(instance=chat, session=session)
            update.message.reply_text('Удалил все введенные Вами данные')
    _logger.info(f'Cleared sequence for chat[{chat.chat_id}]')
