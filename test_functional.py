import unittest
from telethon import InteractiveTelegramClient, TelegramClient
from telethon.utils import get_display_name, get_input_peer

# IMPORTANT: to make these tests work, you have to create the local_settings.py file,
# take local_settings_template as... template!
from local_settings import telegram_settings

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.client = InteractiveTelegramClient('session_id', telegram_settings['user_id'], api_id=telegram_settings['api_id'],
                                           api_hash=telegram_settings['api_hash'])

        # search bot in the last 10 chats
        dialogs, entities = self.client.get_dialogs(10)
        for i, entity in enumerate(entities):
            i += 1  # 1-based index for normies
            if get_display_name(entity) == telegram_settings['bot_name']:
                self.bot = get_input_peer(entity)

    def tearDown(self):
        self.client.disconnect()

    def send_message_to_bot(self, msg):
        self.client.send_message(self.bot, msg)
        total_count, messages, senders = self.client.get_message_history(self.bot, limit=10)
        for msg, sender in zip(messages, senders):
            if sender.first_name == 'LottoBot':
                return msg.message
                break

    def test_hello(self):
        output = self.send_message_to_bot('/hello')
        self.assertEqual('Hello ' + self.client.session.user.first_name, output)


