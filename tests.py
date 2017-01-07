#!/usr/bin/env python3

import unittest
from unittest.mock import patch, call
import start_bot

class TelegramTest(unittest.TestCase):

    @patch('telegram.ext.Updater')
    def test_bot_starts(self, updater):
        start_bot.start_bot('token')
        self.assertIn(call('token'), updater.mock_calls)
        self.assertIn(call().start_polling(), updater.mock_calls)
        self.assertIn(call().idle(), updater.mock_calls)


class TestNumberGiver(unittest.TestCase):

    def test_give_five_random_numbers(self):
        output = start_bot.get_numbers()
        self.assertEqual(5, len(output))
        for n in output:
            self.assertIsInstance(n, int)