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

    @classmethod
    def setUpClass(cls):
        # set bot
        cls.bot = LottoBot(telegram_settings['test_token'])
        cls.bot.run()

        # set up client
        cls.client = InteractiveTelegramClient('session_id', telegram_settings['user_id'], api_id=telegram_settings['api_id'],
                                           api_hash=telegram_settings['api_hash'])

        # set bot entity
        dialogs, entities = cls.client.get_dialogs(10)
        for i, entity in enumerate(entities):
            i += 1  # 1-based index for normies
            if get_display_name(entity) == cls.bot.updater.bot.first_name:
                cls.bot_entity = get_input_peer(entity)

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()
        cls.bot.updater.stop()

    def get_last_line(self, after=None):
        total_count, messages, senders = self.client.get_message_history(self.bot_entity, limit=10)
        for msg, sender in zip(messages, senders):
            if msg.date < after:
                break
            if sender.first_name == self.bot.updater.bot.first_name:
                return msg.message

    def get_line_after(self, after):
        total_count, messages, senders = self.client.get_message_history(self.bot_entity, limit=10)
        for msg, sender in zip(reversed(messages), reversed(senders)):
            if sender.first_name == self.bot.updater.bot.first_name and msg.date >= after:
                return msg.message

    def send_message_to_bot(self, msg):
        sending_time = datetime.now()
        sending_time = sending_time - timedelta(microseconds=sending_time.microsecond)
        self.client.send_message(self.bot_entity, msg)
        sleep(1)
        return self.get_line_after(sending_time)

    def test_start(self):
        output = self.send_message_to_bot('/start')
        self.assertEqual('Welcome!', output)

    def test_get_five_lotto_numbers(self):
        output = self.send_message_to_bot('/lotto').split()

        self.assertEqual(5, len(output))
        for n in output:
            self.assertTrue(n.isnumeric())
            self.assertTrue(1 <= int(n) <= 90)

if __name__ == '__main__':
    unittest.main()
