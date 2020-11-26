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


#  basic setup for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Bot:
    """Class describing Telegram-Bot behaviour."""

    def __init__(self):

        #  setup hardware (PIR sensor and Camera)
        self.pir_sensor = PIRSensor(sensor_pin=config.PIR_PIN)
        self.camera = Camera()

        #  create updater for bot - set all requred setting for connection
        requests_settings = config.REQUEST_KWARGS \
            if len(config.REQUEST_KWARGS) > 0 else None

        self.updater = Updater(
            token=config.TOKEN,
            use_context=True,
            request_kwargs=requests_settings)

        #  create atribute for dispatcher
        self.dispatcher = self.updater.dispatcher

        #  fill list of possible command for bot (types /<command> inside
        #  message field) and related methods which should be ran
        commands = [
            #  show main menu - command to interact with bot
            [['menu', 'start', 'hi', 'hey', 'hello'], self.show_menu],

            #  force bot to capture image and send it
            [['photo', 'capture'], self._capture_and_send],

            #  stop and start process of movement detection
            ['stop', self._stop_detection],
            ['start', self._start_detection],
        ]

        #  add handlers for every item in commands list
        for cmd_txt, cmd_func in commands:
            self.dispatcher.add_handler(CommandHandler(cmd_txt, cmd_func))

        #  build menu with buttons and linked commands
        self.menu = self._build_menu()
        self.dispatcher.add_handler(CallbackQueryHandler(self._menu_actions))

        #  create background job for movement detection process and ask to
        #  run it every 5 seconds
        self.j = self.updater.job_queue
        self.detection_job = self.j.run_repeating(
            self._detect_movement, 5, first=0)

        #  ID of person who own security system (YOUR ID :) )
        self.reciever_id = config.RECIEVER_ID

    def show_menu(self, update, context):
        """Send greetings message with Menu Buttons.

        Args:
            update (telegram.Update): This object represents an incoming update.
            context (telegram.ext.CallbackContext): context object
        """

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Hello, I\'m Your Security Bot. What would you like to do?',
            reply_markup=self.menu)

    def _menu_actions(self, update, context):
        """Link every command recieved from menu button to bot action.

        Args:
            update (telegram.Update): This object represents an incoming update.
            context (telegram.ext.CallbackContext): context object
        """
        query = update.callback_query
        if update.message.chat_id != self.reciever_id:
            self._access_denied(update, context)

        elif query.data == 'menu':
            self.show_menu(update, context)
        elif query.data == 'photo':
            self._capture_and_send(update, context)
        elif query.data == 'stop':
            self._stop_detection(update, context)
        elif query.data == 'start':
            self._start_detection(update, context)

    def _access_denied(self, update, context):
        """Send info message with rejection.

        Args:
            update (telegram.Update): This object represents an incoming update.
            context (telegram.ext.CallbackContext): context object
        """

        message_text = "You don't have permissions to communicate with this bot"
        logging.info(message_text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text)

    def _stop_detection(self, update, context):
        """Stop movement detection process.

        Args:
            update (telegram.Update): This object represents an incoming update.
            context (telegram.ext.CallbackContext): context object
        """

        #  delete job from job queue
        self.detection_job.schedule_removal()

        #  send to use and log info message
        message_text = "Motion Detection Disabled."
        logging.info(message_text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text)

    def _start_detection(self, update, context):
        """Run movement detection process.

        Args:
            update (telegram.Update): This object represents an incoming update.
            context (telegram.ext.CallbackContext): context object
        """

        #  recreate job for movement detection process
        self.detection_job = self.j.run_repeating(
            self._detect_movement, 5, first=0)

        #  send to use and log info message
        message_text = "Motion Detection Enabled."
        logging.info(message_text)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text)

    def run(self):
        """Run Telegram Bot"""

        self.updater.start_polling(poll_interval=0.1, timeout=60 * 10)
        self.updater.idle()

    def _build_menu(self):
        """Build menu with buttons and link to command.

        Returns:
            telegram.InlineKeyboardMarkup: Telegram menu.
        """

        button_list = [
            [InlineKeyboardButton('Show Menu', callback_data='menu')],
            [InlineKeyboardButton('Make Photo', callback_data='photo')],
            [InlineKeyboardButton('Start Detection', callback_data='stop')],
            [InlineKeyboardButton('Stop Detection', callback_data='start')],
        ]
        menu = InlineKeyboardMarkup(button_list)
        return menu

    def _capture_and_send(self, update, context):
        """Bot Action - capture image and send it with message.

        Args:
            update (telegram.Update): This object represents an incoming update.
            context (telegram.ext.CallbackContext): context object
        """

        #  make photo
        pic_path = self.camera.capture()

        #  send made photo
        context.bot.send_photo(
            chat_id=self.reciever_id,
            photo=open(pic_path, 'rb'))

    def _detect_movement(self, context):
        """Bot Action - check if movement was detected and \
           capture image and send it with message.

        Args:
            update (telegram.Update): This object represents an incoming update.
            context (telegram.ext.CallbackContext): context object
        """

        if self.pir_sensor.get_output():
            logging.info('Alarm! Motion detected!')
            self._capture_and_send(None, context)
        else:
            logging.debug('No movement detected. All clear.')
