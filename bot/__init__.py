#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import json
from functools import partial
import sys
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import NetworkError
import config

from .utils import PIRSensor, Camera


#  setup logging
logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Bot:
    def __init__(self):
        #  add hardware
        self.pir_sensor = PIRSensor(
            vcc_pin=config.PIR_VCC, out_pin=config.PIR_OUT)
        self.camera = Camera()

        #  create updater for bot
        self.updater = Updater(
            token=config.TOKEN,
            use_context=True,
            )

        self.dispatcher = self.updater.dispatcher

        commands = [
            [['menu', 'start'], self.show_menu],
            ['photo', self._capture_and_send],
            ['stop', self._stop_detection],
            ['start', self._start_detection],
        ]

        #  add handlers
        for cmd_txt, cmd_func in commands:
            self.dispatcher.add_handler(CommandHandler(cmd_txt, cmd_func))

        #  add menu
        self.menu = self._build_menu()
        self.dispatcher.add_handler(CallbackQueryHandler(self._menu_actions))

        #  add background jobs
        self.j = self.updater.job_queue
        self.detection_job = self.j.run_repeating(
            self._detect_movement, 5, first=0)

        self.chat_id = config.CHAT_ID

    def show_menu(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Hello, I\'m SmartHome Bot. What would you like to do?',
            reply_markup=self.menu)

    def _menu_actions(self, update, context):
        query = update.callback_query
        if query.data == 'hello':
            self.hello(update, context)
        elif query.data == 'menu':
            self.show_menu(update, context)
        elif query.data == 'photo':
            self._capture_and_send(update, context)
        elif query.data == 'stop':
            self._stop_detection(update, context)
        elif query.data == 'start':
            self._start_detection(update, context)

    def hello(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hello Boss!")

    def _stop_detection(self, update, context):
        # self.pir_sensor.turn_off()
        self.detection_job.schedule_removal()
        message_text = "Motion Detection Disabled."
        logging.info(message_text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text)

    def _start_detection(self, update, context):
        # self.pir_sensor.turn_on()
        self.detection_job = self.j.run_repeating(self._detect_movement, 5, first=0)
        message_text = "Motion Detection Enabled."
        logging.info(message_text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text)

    def run(self):
        self.updater.start_polling(poll_interval=0.1, timeout=60 * 10)
        self.updater.idle()

    def _build_menu(self):
        button_list = [
            [InlineKeyboardButton('show menu', callback_data='menu')],
            [InlineKeyboardButton('say hello', callback_data='hello')],
            [InlineKeyboardButton('make photo', callback_data='photo')],
            [InlineKeyboardButton('stop detection', callback_data='stop')],
            [InlineKeyboardButton('start detection', callback_data='start')],
        ]
        menu = InlineKeyboardMarkup(button_list)
        return menu

    def _capture_and_send(self, update, context):
        #  make photo
        pic_path = self.camera.capture()
        #  send made photo
        context.bot.send_photo(
            chat_id=self.chat_id,
            photo=open(pic_path, 'rb'))

    def _detect_movement(self, context):
        if self.pir_sensor.get_output():
            logging.info('Alarm! Motion detected!')
            self._capture_and_send(None, context)
        else:
            logging.debug('No movement detected. All clear.')
