#!/usr/bin/env python3

import unittest
from unittest.mock import patch, call
from start_bot import start_bot

class TelegramTest(unittest.TestCase):

    @patch('telegram.ext.Updater')
    def test_bot_starts(self, updater):
        start_bot('token')
        self.assertIn(call('token'), updater.mock_calls)
        self.assertIn(call().start_polling(), updater.mock_calls)
        self.assertIn(call().idle(), updater.mock_calls)
