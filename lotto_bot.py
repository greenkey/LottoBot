from os import environ
from telegram.ext import Updater, CommandHandler


ENVIRONMENT = environ.get('LOTTO_BOT_ENV','TEST')

class LottoBot():

    def __init__(self, token):
        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.handle_start))

    def run(self):
        self.updater.start_polling()
        if ENVIRONMENT == 'PRODUCTION':
            self.updater.idle()

    def handle_start(self, bot, update):
        update.message.reply_text('Welcome!')
