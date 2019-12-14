#!/usr/bin/env python
import sys
import logging
import logging.config
from slackbot import settings
from common import bot
import resource


def main():
  kw = {
    'format': '%(levelname)s [%(asctime)s] %(message)s',
    'datefmt': '%Y/%m/%d %H:%M:%S,000',
    'level': logging.DEBUG if settings.DEBUG else logging.INFO,
    'stream': sys.stdout,
  }
  logging.basicConfig(**kw)
  logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
  bot.run()


if __name__ == '__main__':
  main()
