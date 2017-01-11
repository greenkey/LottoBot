from os import environ
from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup
import random


ENVIRONMENT = environ.get('LOTTO_BOT_ENV','TEST')

class LottoBot():

    def __init__(self, token):
        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.handle_start))
        self.updater.dispatcher.add_handler(CommandHandler('lotto', self.handle_lotto))

    def run(self):
        self.updater.start_polling()
        if ENVIRONMENT == 'PRODUCTION':
            self.updater.idle()

    def handle_start(self, bot, update):
        update.message.reply_text('Welcome!')

        custom_keyboard = [['/lotto']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)

        bot.sendMessage(chat_id=update.message.chat_id,
                        text = "Custom Keyboard Test",
                        reply_markup = reply_markup)

    def handle_lotto(self, bot, update):
        update.message.reply_text(self.get_numbers())

    def get_numbers(self):
        numbers = set()
        while len(numbers)<5:
            numbers.add(random.randrange(1,90))
        return ' '.join([str(n) for n in sorted(numbers)])
