# *****************************************************************************
# Основы объектно-ориентированного программирования
# Задание 8.
# Добавьте в приложение класс Calendar
# 1. Добавьте в приложение класс Calendar который будет содержать методы для создания, чтения, редактирования и
# удаления событий, а также отображения всех событий. Для работы с календарем вам потребуются библиотеки os и datetime.
# Импортируйте их в начале кода.
# 2. Добавьте и зарегистрируйте обработчики команд для создания, чтения, редактирования и удаления событий, а также
# отображения всех событий.
# 3. Затем включите этот класс в основную функцию приложения (функция main()), чтобы дать пользователю возможность
# создавать, читать, редактировать и удалять события, а также отображать весь список событий.
# *****************************************************************************
import logging
import datetime
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
ID = range(1)


def cancel(update, context) -> int:
    """Выход из диалога по команде /cancel."""
    try:
        user = update.message.from_user
        logger.info(f"Пользователь {user.first_name} вышел из диалога.")
        update.message.reply_text('Запрос данных прерван пользователем.')
        return ConversationHandler.END
    except AttributeError as err:
        logger.error(f'Произошла ошибка: {err}')


# обработчик для команды /start
def create_start_handler(update, context):
    """Формирование сообщения пользователю по команде start."""
    try:
        msg_start = """ Бот для работы с событиями календаря.
        Команды:
        /start - запуск бота
        /cancel - выход из диалога
        /key_on - включение виртуальной клавиатуры
        /key_off - выключение виртуальной клавиатуры
        /create_event <название события> - создание события
        /read_event <номер события> - чтение события
        /edit_event <номер события> - редактирование события
        /delete_event <номер события> - удаление события
        /display_event - вывод списка событий
        /help - выводит справку по командам
        """
        context.bot.send_message(chat_id=update.message.chat_id, text=msg_start)
    except AttributeError as err:
        # Отправить пользователю сообщение об ошибке
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Произошла ошибка: {err}")


def key_on(update, context) -> None:
    """Добавляет виртуальную клавиатуру с командами"""
    reply_keyboard = [['/start'],
                      ['/key_off'],
                      ['/help'],
                      ['/create_event'],
                      ['/read_event'],
                      ['/edit_event'],
                      ['/delete_event'],
                      ['/display_event']]

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
        /cancel - выход из диалога
        /key_on - включение виртуальной клавиатуры
        /key_off - выключение виртуальной клавиатуры
        /create_event <название события> - создание события
        /read_event <номер события> - чтение события
        /edit_event <номер события> - редактирование события
        /delete_event <номер события> - удаление события
        /display_event - вывод списка событий
        /help - выводит справку по командам
        """
                              )


# ******** Задание 8 Календарь ********
# Создать класс Calendar
class Calendar:
    def __init__(self):
        self.events = {}

    # метод create_event
    def create_event(self, event_name, event_date, event_time, event_details) -> int:
        event_id = len(self.events) + 1
        event = {
            "id": event_id,
            "name": event_name,
            "date": event_date,
            "time": event_time,
            "details": event_details
        }
        self.events[event_id] = event
        return event_id

    # метод read_event
    def read_event(self, id_event) -> str:
        str_out = ''
        for key, val in self.events[id_event].items():
            str_out = str_out + str(key) + ': ' + str(val) + ' | '
        return str_out

    # метод edit_event
    def edit_event(self, id_event, new_event_details) -> None:
        self.events[id_event]['details'] = new_event_details

    # метод delete_event
    def delete_event(self, id_event) -> str:
        del self.events[id_event]
        return f'Событие номер {id_event} удалено.'

    # метод display_event
    def display_event(self) -> str:
        str_out = ''
        for el in self.events.items():
            # print(el[1].items())
            for key, val in el[1].items():
                str_out = str_out + str(key) + ': ' + str(val) + ' | '
            str_out = str_out + '\n'
        return str_out



def main() -> None:
    """Запуск бота."""
    try:
        # создание обработчика с токеном
        updater = Updater(token=secrets.API_TOKEN)

        # получение диспетчера
        dispatcher = updater.dispatcher

        # обработка команды /start
        updater.dispatcher.add_handler(CommandHandler('start', create_start_handler))

        # обработка команды /key_on
        updater.dispatcher.add_handler(CommandHandler('key_on', key_on))

        # обработка команды /key_off
        updater.dispatcher.add_handler(CommandHandler('key_off', key_off))

        # обработка команды /help
        updater.dispatcher.add_handler(CommandHandler('help', help_view))

        # ***************************
        # глобально доступный объект календаря
        calendar = Calendar()

        # обработчик для создания событий
        def event_create_handler(update, context) -> None:
            try:
                # Взять данные о событии из сообщения пользователя
                event_name = update.message.text[14:]
                event_date = datetime.datetime.now().strftime('%Y-%m-%d')
                event_time = datetime.datetime.now().time().strftime('%H:%M')
                event_details = "Описание события"

                # Создать событие с помощью метода create_event класса Calendar
                event_id = calendar.create_event(event_name, event_date, event_time, event_details)

                # Отправить пользователю подтверждение
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f"Событие {event_name} создано и имеет номер {event_id}.")
            except AttributeError as error_info:
                # Отправить пользователю сообщение об ошибке
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'При создании события произошла ошибка {error_info}.')

        # Зарегистрировать обработчик, чтобы он вызывался по команде /create_event
        updater.dispatcher.add_handler(CommandHandler('create_event', event_create_handler))

        # обработчик для чтения событий
        def event_read_handler(update, context) -> None:
            try:
                text = update.message.text.replace('/read_event', '').replace(' ', '')  # оставляем только номер
                if text.isdigit():  # проверяем, что номер события число
                    id_event = int(text)
                else:
                    id_event = 0  # так как нумерация событий начинается с 1
                if id_event in calendar.events.keys():
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=calendar.read_event(id_event=id_event))
                else:
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=f'Событие с номером {text} не найдено. Формат команды: '
                                                  f'/read_event <номер события> ')
            except AttributeError as error_info:
                # Отправить пользователю сообщение об ошибке
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'При чтении события произошла ошибка {error_info}.')

        # Зарегистрировать обработчик, чтобы он вызывался по команде /read_event
        updater.dispatcher.add_handler(CommandHandler('read_event', event_read_handler))

        # обработчик для редактирования событий
        def event_edit_handler(update, context) -> int:
            try:
                text = update.message.text.replace('/edit_event', '').replace(' ', '')  # оставляем только номер
                if text.isdigit():  # проверяем, что номер события число
                    id_event = int(text)
                else:
                    id_event = 0  # так как нумерация событий начинается с 1
                if id_event in calendar.events.keys():
                    context.user_data['id_event'] = id_event
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text='Введите новое описание события.')
                    return ID
                else:
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=f'Событие с номером {text} не найдено. Формат команды: '
                                                  f'/edit_event <номер события> ')
            except AttributeError as error_info:
                # Отправить пользователю сообщение об ошибке
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'При редактировании события произошла ошибка {error_info}.')

        # редактирование события
        def edit_event(update, context) -> None:
            try:
                calendar.edit_event(context.user_data['id_event'], update.message.text)
                # Отправить пользователю подтверждение
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f"Событие {context.user_data['id_event']} отредактировано.")
            except AttributeError as error_info:
                # Отправить пользователю сообщение об ошибке
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'При редактировании события произошла ошибка {error_info}.')

        # диалог для редактирования события, шаги ID, ТEXT
        conv_handler_edit_event = ConversationHandler(
            entry_points=[CommandHandler('edit_event', event_edit_handler)],
            states={
                ID: [MessageHandler(Filters.text & ~Filters.command, edit_event)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],  # принудительный выход из диалога по команде /cancel
        )
        dispatcher.add_handler(conv_handler_edit_event)

        # обработчик для удаления событий
        def event_delete_handler(update, context) -> None:
            try:
                text = update.message.text.replace('/delete_event', '').replace(' ', '')  # оставляем только номер
                if text.isdigit():  # проверяем, что номер события число
                    id_event = int(text)
                else:
                    id_event = 0  # так как нумерация событий начинается с 1
                if id_event in calendar.events.keys():
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=calendar.delete_event(id_event=id_event))
                else:
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=f'Событие с номером {text} не найдено. Формат команды: '
                                                  f'/delete_event <номер события> ')
            except AttributeError as error_info:
                # Отправить пользователю сообщение об ошибке
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'При удалении события произошла ошибка {error_info}.')

        # Зарегистрировать обработчик, чтобы он вызывался по команде /delete_event
        updater.dispatcher.add_handler(CommandHandler('delete_event', event_delete_handler))

        # обработчик для вывода списка событий
        def event_display_handler(update, context) -> None:
            try:
                if calendar.events:
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=calendar.display_event())
                else:
                    context.bot.send_message(chat_id=update.message.chat_id,
                                             text=f'В календаре нет событий.')
            except AttributeError as error_info:
                # Отправить пользователю сообщение об ошибке
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=f'При удалении события произошла ошибка {error_info}.')

        # Зарегистрировать обработчик, чтобы он вызывался по команде /delete_event
        updater.dispatcher.add_handler(CommandHandler('display_event', event_display_handler))

        # запуск бота
        updater.start_polling()

        # для корректной остановки бота по запросу из ide
        updater.idle()

    except AttributeError as err:
        logger.error(f'Произошла ошибка: {err}')


if __name__ == '__main__':
    main()
