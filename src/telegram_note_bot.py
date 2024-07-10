# *****************************************************************************
# Задание 7. Подключите бота к Telegram.
# Используйте Telegram API, чтобы создать бота в Telegram.
# Вынес в отдельный исходник, так как от notepad2 почти ничего не остается =о)
# *****************************************************************************

import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)
import secrets  # API_TOKEN = '<ТОКЕN>'

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# шаги ввода данных
NAME, TEXT, READ = range(3)

# Глобальные переменные для передачи значений
note_name, note_text = '', ''


# создаем заметку по полученным данным
def build_note(lc_note_text, lc_note_name) -> str:
    """Получает название и текст заметки, а затем создает текстовый файл с этим названием и текстом"""
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
def create_note_handler(update, context) -> int:
    """Запрос имени заметки."""
    try:
        update.message.reply_text('Введите имя заметки: ')
        return NAME
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# получение имени заметки для создания
def get_name_note_create(update, context) -> int:
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
def get_text_note(update, context) -> int:
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


def cancel(update, context) -> int:
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
        /display - вывод списка заметок в порядке уменьшения длинны
        /key_on - включение виртуальной клавиатуры
        /key_off - выключение виртуальной клавиатуры
        /help - выводит справку по командам
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
def get_name_note_edit(update, context) -> int:
    """Запрос нового текста заметки."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Имя редактируемой заметки: {update.message.text}.")
        global note_name
        note_name = update.message.text
        if os.path.isfile(note_name + '.txt'):
            update.message.reply_text('Введите новый текст заметки: ')
            return TEXT
        else:
            logger.error(f"Пользователь:  {user.first_name}. Заметка {note_name} не найдена.")
            update.message.reply_text(f'Заметка с именем {note_name} не найдена')
            update.message.reply_text('Введите имя заметки для редактирования еще раз:')
            return NAME
    except Exception as err:
        logger.error(f'Произошла ошибка : {err}')


# получение нового текста заметки + создание заметки
def get_text_note_edit(update, context) -> int:
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


def delete_note(lc_note_name) -> str:
    """Функция удаляет файл.
    Для удаления используйте функцию os.remove из модуля os. Если файла не существует, она выводит сообщение,
    что заметка не найдена."""
    try:
        if os.path.isfile(lc_note_name + '.txt'):
            os.remove(lc_note_name + '.txt')
            logger.info(f"Заметка {note_name} удалена.")
            return f"Заметка {lc_note_name} удалена."
        else:
            logger.error(f"Заметка  {lc_note_name} не найдена.")
            return f"Заметка  {lc_note_name} не найдена."
    except FileNotFoundError:
        logger.error(f'Файл с именем {note_name}.txt не найден.')
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# получение имени заметки для удаления
def get_name_note_delete(update, context) -> int:
    """Запрос имени заметки для удаления."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь:  {user.first_name}. Имя заметки для удаления : {update.message.text}.")
        global note_name
        note_name = update.message.text
        update.message.reply_text(delete_note(note_name))  # удаляем заметку и выводим сообщение о результате
        return ConversationHandler.END
    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


# обработчик для команды /delete
def create_delete_handler(update, context) -> int:
    try:
        update.message.reply_text('Введите имя заметки для удаления: ')
        return NAME
    except Exception as err:
        # Отправить пользователю сообщение об ошибке
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {err}")


def display_sorted_notes(update, context) -> None:
    """Выводит все заметки пользователя в порядке уменьшения длинны"""
    try:
        # формирование списка файлов с заметками
        notes = [note for note in os.listdir() if note.endswith(".txt")]
        # создание словаря с именем файла и длинной заметки
        dic_notes = {}
        for i in notes:
            with open(i, "r", encoding="utf-8") as file:
                dic_notes[i] = len(file.read())
        # сортировка заметок по уменьшению длинны
        sorted_notes = sorted(dic_notes.items(), key=lambda item: item[1], reverse=True)
        # вывод заметок в порядке уменьшения длинны
        for i in sorted_notes:
            with open(i[0], "r", encoding="utf-8") as file:
                update.message.reply_text(f'Заметка "{i[0]}".')
                update.message.reply_text(file.read())
    except Exception as err:  # не приходит в голову ситуация вызывающая ошибку =/
        logger.error(f'Произошла ошибка: {err}')


def key_on(update, context) -> None:
    """Добавляет виртуальную клавиатуру с командами"""
    reply_keyboard = [['/start'],
                      ['/create'],
                      ['/cancel'],
                      ['/read'],
                      ['/edit'],
                      ['/delete'],
                      ['/display'],
                      ['/key_off'],
                      ['/help']]

    update.message.reply_text(
        'Виртуальная клавиатура добавлена в бот.',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True,
            input_field_placeholder='Выберите команду или введите ответ на запрос'
        ),
    )


def key_off(update, context) -> None:
    """Убирает виртуальную клавиатуру с командами"""
    update.message.reply_text(
        'Виртуальная клавиатура убрана из бота.',
        reply_markup=ReplyKeyboardRemove(),
    )


def help_view(update, context) -> None:
    """Выводит справку по командам"""
    update.message.reply_text(""" Бот для работы с заметками.
        Команды:
        /start - запуск бота
        /create - создание заметки
        /cancel - выход из диалога
        /read - чтение заметки
        /edit - замена текста заметки
        /delete - удаление заметки
        /display - вывод списка заметок в порядке уменьшения длинны
        /key_on - включение виртуальной клавиатуры
        /key_off - выключение виртуальной клавиатуры
        /help - выводит справку по командам
        """
                              )


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

        # диалог для удаления заметки, шаг NAME
        conv_handler_delete = ConversationHandler(
            entry_points=[CommandHandler('delete', create_delete_handler)],
            states={
                NAME: [MessageHandler(Filters.text & ~Filters.command, get_name_note_delete)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],  # принудительный выход из диалога по команде /cancel
        )
        dispatcher.add_handler(conv_handler_delete)

        # обработка команды /display
        updater.dispatcher.add_handler(CommandHandler('display', display_sorted_notes))

        # обработка команды /key_on
        updater.dispatcher.add_handler(CommandHandler('key_on', key_on))

        # обработка команды /key_off
        updater.dispatcher.add_handler(CommandHandler('key_off', key_off))

        # обработка команды /help
        updater.dispatcher.add_handler(CommandHandler('help', help_view))

        # запуск бота
        updater.start_polling()

        # для корректной остановки бота по запросу из ide
        updater.idle()

    except Exception as err:
        logger.error(f'Произошла ошибка: {err}')


if __name__ == '__main__':
    main()
