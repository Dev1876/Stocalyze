# -*- coding: utf-8 -*-
import config
import pytz
import telebot 
import logging
from telegram.ext import Updater, CommandHandler
#https://github.com/davidcjw/stockM
#https://levelup.gitconnected.com/how-to-code-a-telegram-bot-to-get-stock-price-updates-in-pure-python-c35d3c44b04c
P_TIMEZONE = pytz.timezone(config.TIMEZONE)