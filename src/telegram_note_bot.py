# *****************************************************************************
# Задание 7. Подключите бота к Telegram
# Используйте Telegram API, чтобы создать бота в Telegram.
# Вынес в отдельный исходник, так как от notepad2 почти ничего не остается =о)
# *****************************************************************************

import logging
import os
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

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# шаги ввода данных
NAME, TEXT, READ = range(3)

# глобалки для передачи значений
note_name, note_text = '', ''


# todo Добавить во все функции обработчики ошибок и дописать варианты конкретных ошибок


# создаем заметку по полученным данным
def build_note(lc_note_text, lc_note_name) -> str:
    """получает название и текст заметки, а затем создает текстовый файл с этим названием и текстом"""
    try:
        if lc_note_text == '':
            logger.error("Текст заметки не может быть пустым.")
            return "Текст заметки не может быть пустым."
        else:
            with open(f"{lc_note_name}.txt", "w", encoding="utf-8") as file:
                file.write(lc_note_text)
            logger.info(f"Заметка {lc_note_name} создана.")
            return f"Заметка {lc_note_name} создана."
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# запуск ввода данных для создания заметок
def create_note_handler(update: Update, context: CallbackContext) -> int:
    """Запрос имени заметки."""
    try:
        update.message.reply_text('Введите имя заметки: ')
        return NAME
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# получение имени заметки для создания
def get_name_note_create(update: Update, context: CallbackContext) -> int:
    """Запрос текста заметки."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Имя создаваемой заметки: {update.message.text}.")
        global note_name
        note_name = update.message.text
        update.message.reply_text('Введите текст заметки: ')
        return TEXT
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# получение текста заметки + создание заметки
def get_text_note(update: Update, context: CallbackContext) -> int:
    """Выход из опроса."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Текст создаваемой заметки: {update.message.text}")
        global note_text
        note_text = update.message.text
        update.message.reply_text(build_note(note_text, note_name))  # создаем заметку и выводим сообщение о результате
        return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


def cancel(update: Update, context: CallbackContext) -> int:
    """Выход из диалога по команде /cancel."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь {user.first_name} вышел из диалога.")
        update.message.reply_text('Запрос данных прерван пользователем.')
        return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# обработчик для команды /start
def create_start_handler(update, context):
    try:
        msg_start = """ Бот для работы с заметками.
        Команды:
        /start - запуск бота
        /create - создание заметки
        /cancel - выход из диалога
        /read - чтение заметки
        /edit - замена текста заметки
        /delete - удаление заметки
        /display - вывод списка заметок
        /display_sorted - вывод списка заметок в порядке уменьшения длинны
        /keyb_on - включение виртуальной клавиатуры
        /keyb_off - выключение виртуальной клавиатуры
        """
        context.bot.send_message(chat_id=update.message.chat_id, text=msg_start)
    except Exception as err:
        # Отправить пользователю сообщение об ошибке
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {err}")


def read_note(lc_note_name) -> str:
    """Читает заметку. Если файл с таким названием существует, функция считывает содержимое
    файла и выводит его на экран. Если файла не существует, функция выводит сообщение, что заметка не найдена.
    Для проверки наличия файла используйте функцию os.path.isfile из модуля os.
    Не забудьте импортировать этот модуль."""
    try:
        if os.path.isfile(lc_note_name + ".txt"):
            with open(f"{lc_note_name}.txt", "r", encoding="utf-8") as file:
                return file.read()
        else:
            logger.error(f"Заметка {lc_note_name} не найдена.")
            return f"Заметка {note_name} не найдена."
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# получение имени заметки для чтения и вывод в чат если есть, если нет сообщение нет
def get_name_note_read(update, context) -> int:
    """Запрос имени заметки для чтения."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Имя заметки для чтения : {update.message.text}.")
        global note_name
        note_name = update.message.text
        update.message.reply_text(read_note(note_name))  # создаем заметку и выводим сообщение о результате
        return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# получение имени заметки для редактирования и вывод в чат если есть, если нет сообщение нет
def get_name_note_read(update, context) -> int:
    """Запрос имени заметки для чтения."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Имя заметки для чтения : {update.message.text}.")
        global note_name
        note_name = update.message.text
        update.message.reply_text(read_note(note_name))  # создаем заметку и выводим сообщение о результате
        return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# обработчик для команды /read
def create_read_handler(update, context) -> None:
    try:
        update.message.reply_text('Введите имя заметки для чтения: ')
        return NAME
    except Exception as err:
        # Отправить пользователю сообщение об ошибке
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {err}")


def edit_note(lc_note_name, lc_note_text) -> str:
    """Обновляет содержимое файла. Если файла не
      существует, она выводит сообщение, что заметка не найдена."""
    try:
        if lc_note_name != '':
            with open(f"{lc_note_name}.txt", "w", encoding="utf-8") as file:
                file.write(lc_note_text)
            logger.info(f"Заметка {lc_note_name} обновлена.")
            return f"Заметка {lc_note_name} обновлена."
    except FileNotFoundError:
        logger.error(f'Невозможно создать файл с именем {note_name}')
    except Exception as err:
        logger.error(f'Произошла ошибка : {err}')


# получение имени заметки для редактирования
def get_name_note_edit(update: Update, context: CallbackContext) -> int:
    """Запрос нового текста заметки."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Имя редактируемой заметки: {update.message.text}.")
        global note_name
        note_name = update.message.text
        update.message.reply_text('Введите новый текст заметки: ')
        return TEXT
    except Exception as err:
        logger.error(f'Произошла ошибка : {err}')


# получение нового текста заметки + создание заметки
def get_text_note_edit(update: Update, context: CallbackContext) -> int:
    """Выход из опроса."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Текст редактируемой заметки: {update.message.text}")
        global note_text
        note_text = update.message.text
        update.message.reply_text(edit_note(note_name, note_text))  # создаем заметку и выводим сообщение о результате
        return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка : {err}')


# обработчик для команды /edit
def create_edit_handler(update, context) -> None:
    try:
        update.message.reply_text('Введите имя заметки для редактирования: ')
        return NAME
    except Exception as err:
        # Отправить пользователю сообщение об ошибке
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {err}")


def main() -> None:
    """Запуск бота."""
    try:
        # создание обработчика с токеном
        updater = Updater(token=secrets.API_TOKEN)

        # получение диспетчера
        dispatcher = updater.dispatcher

        # обработка команды /start
        updater.dispatcher.add_handler(CommandHandler('start', create_start_handler))

        # диалог для создания заметки, шаги NAME, ТEXT
        conv_handler_create = ConversationHandler(
            entry_points=[CommandHandler('create', create_note_handler)],
            states={
                NAME: [MessageHandler(Filters.text & ~Filters.command, get_name_note_create)],
                TEXT: [MessageHandler(Filters.text & ~Filters.command, get_text_note)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],  # принудительный выход из диалога по команде /cancel
        )
        dispatcher.add_handler(conv_handler_create)

        # диалог для чтения заметки, шаг NAME
        conv_handler_read = ConversationHandler(
            entry_points=[CommandHandler('read', create_read_handler)],
            states={
                NAME: [MessageHandler(Filters.text & ~Filters.command, get_name_note_read)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],  # принудительный выход из диалога по команде /cancel
        )
        dispatcher.add_handler(conv_handler_read)

        # диалог для редактирования заметки, шаги NAME, ТEXT
        conv_handler_edit = ConversationHandler(
            entry_points=[CommandHandler('edit', create_edit_handler)],
            states={
                NAME: [MessageHandler(Filters.text & ~Filters.command, get_name_note_edit)],
                TEXT: [MessageHandler(Filters.text & ~Filters.command, get_text_note_edit)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],  # принудительный выход из диалога по команде /cancel
        )
        dispatcher.add_handler(conv_handler_edit)

        # запуск бота
        updater.start_polling()

        # для корректной остановки бота по запросу из ide
        updater.idle()

    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


if __name__ == '__main__':
    main()


