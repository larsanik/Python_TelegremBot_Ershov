import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import secrets

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# шаги ввода данных
NAME, TEXT = range(2)

# глобалки для передачи значений
note_name, note_text = '', ''


# todo Добавить во все функции обработчики ошибок
# todo Добавить надписи в поле ввода, как в примере с гендерами)
# todo Проверить работу преждевременного выхода по /cancel


# создаем заметку по полученным данным
def build_note(lc_note_text, lc_note_name) -> None:
    """получает название и текст заметки, а затем создает текстовый файл с этим названием и текстом"""
    try:
        if lc_note_text.strip() == '':
            logger.error("Текст заметки не может быть пустым.")
            return "Текст заметки не может быть пустым."
        else:
            return ''
        with open(f"{lc_note_name}.txt", "w", encoding="utf-8") as file:
            file.write(lc_note_text)
        logger.info(f"Заметка {lc_note_name} создана.")
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# запуск ввода данных для создания заметок
def create_note_handler(update: Update, context: CallbackContext) -> int:
    """Запрос имени заметки."""
    update.message.reply_text('Введите имя заметки: ')
    return NAME


def get_name_note(update: Update, context: CallbackContext) -> int:
    """Запрос текста заметки."""
    user = update.message.from_user
    logger.info(f"Пользователь:  {user.first_name}. Имя заметки: {update.message.text}.")
    global note_name
    note_name = update.message.text
    update.message.reply_text('Введите текст заметки: ')
    return TEXT


def get_text_note(update: Update, context: CallbackContext) -> int:
    """Выход из опроса."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Текст заметки: {update.message.text}")
        global note_text
        if build_note(note_text, note_name) != '':  # сообщение заметка не может быть пустая
            # todo никогда не сработает, telegram не дает отправить пустое сообщение
            update.message.reply_text(build_note(note_text, note_name))
        else:
            note_text = update.message.text
            build_note(note_text)  # создаем заметку
            update.message.reply_text(f'Заметка {note_name} создана.')
            return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


def cancel(update: Update, context: CallbackContext) -> int:
    """Выход из диалога по команде /cancel."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь {user.first_name} вышел из диалога .")
        update.message.reply_text('Запрос данных прерван пользователем')
        return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


def main() -> None:
    """Run the bot."""
    try:
        # Create the Updater and pass it your bot's token.
        updater = Updater(token=secrets.API_TOKEN)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # Add conversation handler with the states NAME, ТEXT
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('create', create_note_handler)],
            states={
                NAME: [MessageHandler(Filters.text, get_name_note)],
                TEXT: [MessageHandler(Filters.text, get_text_note)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )

        dispatcher.add_handler(conv_handler)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


if __name__ == '__main__':
    main()


