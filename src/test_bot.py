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

NAME, TEXT = range(2)


def get_name_note(update: Update, context: CallbackContext) -> int:
    """Запрос имени заметки."""
    update.message.reply_text('Введите имя заметки: ')
    return NAME


def get_text_note(update: Update, context: CallbackContext) -> int:
    """Запрос текста заметки."""
    update.message.reply_text('Введите текст заметки: ')
    return TEXT


def cancel(update: Update, context: CallbackContext) -> int:
    """Выход из диалога по команде /cancel."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=secrets.API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states NAME, ТEXT, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', get_name_note)],
        states={
            NAME: [MessageHandler(Filters.text, get_name_note)],
            TEXT: [MessageHandler(Filters.text, get_text_note)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-F2 or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


