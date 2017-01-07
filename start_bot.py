#!/usr/bin/env python3

import random

def start_bot(token):
    from telegram.ext import Updater, CommandHandler

    def start(bot, update):
        update.message.reply_text('Hello World!')

    def hello(bot, update):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))

    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('numbers', hello))

    updater.start_polling()
    updater.idle()

def get_numbers():
    output = set()
    while len(output) < 5:
        output.add(random.randrange(1,90))
    return output

if __name__ == '__main__':
    import sys
    start_bot(sys.argv[1])