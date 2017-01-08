import unittest
from datetime import datetime, timedelta
from time import sleep

from telethon import InteractiveTelegramClient, TelegramClient
from telethon.utils import get_display_name, get_input_peer

from lotto_bot import LottoBot

# IMPORTANT: to make these tests work, you have to create the local_settings.py file,
# take local_settings_template as... template!
from local_settings import telegram_settings

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        # set bot
        self.bot = LottoBot(telegram_settings['test_token'])
        self.bot.run()

        # set up client
        self.client = InteractiveTelegramClient('session_id', telegram_settings['user_id'], api_id=telegram_settings['api_id'],
                                           api_hash=telegram_settings['api_hash'])

        # set bot entity
        dialogs, entities = self.client.get_dialogs(10)
        for i, entity in enumerate(entities):
            i += 1  # 1-based index for normies
            if get_display_name(entity) == self.bot.updater.bot.first_name:
                self.bot_entity = get_input_peer(entity)

    def tearDown(self):
        self.client.disconnect()
        self.bot.updater.stop()

    def get_last_line(self, after=None):
        total_count, messages, senders = self.client.get_message_history(self.bot_entity, limit=10)
        for msg, sender in zip(messages, senders):
            if msg.date < after:
                break
            if sender.first_name == self.bot.updater.bot.first_name:
                return msg.message

    def send_message_to_bot(self, msg):
        sending_time = datetime.now()
        sending_time = sending_time - timedelta(microseconds=sending_time.microsecond)
        self.client.send_message(self.bot_entity, msg)
        sleep(1)
        return self.get_last_line(after=sending_time)

    def test_start(self):
        output = self.send_message_to_bot('/start')
        self.assertEqual('Welcome!', output)

    def _test_hello(self):
        output = self.send_message_to_bot('/hello')
        self.assertEqual('Hello ' + self.client.session.user.first_name, output)

if __name__ == '__main__':
    unittest.main()
