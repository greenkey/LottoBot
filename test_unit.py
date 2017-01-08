#!/usr/bin/env python3

import unittest
from unittest.mock import patch, call

import start_bot
from lotto_bot import LottoBot


class LottoBotTest(unittest.TestCase):

    @patch('lotto_bot.Updater')
    def test_bot_object_starts(self, updater):
        bot = LottoBot('token')
        bot.run()
        self.assertIn(call('token'), updater.mock_calls)
        self.assertIn(call().start_polling(), updater.mock_calls)

    @patch('lotto_bot.Updater')
    def test_handle_start(self, updater):
        bot = LottoBot('token')
        bot.handle_start(bot, updater())
        self.assertIn(call().message.reply_text('Welcome!'), updater.mock_calls)

    @patch('lotto_bot.Updater')
    def test_give_five_lotto_numbers(self, updater):
        bot = LottoBot('token')
        output = bot.get_numbers().split()
        self.assertEqual(5, len(output))
        for n in output:
            self.assertTrue(n.isnumeric())
            self.assertTrue(1 <= int(n) <= 90)
