#!/usr/bin/env python3

from lotto_bot import LottoBot

if __name__ == '__main__':
    import sys
    bot = LottoBot(sys.argv[1])
    bot.run()
