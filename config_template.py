#!/usr/bin/env python
# -*- coding: utf-8 -*-


TOKEN = 'xxx' #  put your telegram-bot token here
CHAT_ID = 0  #  put ID of chat between you and your chatbot
REQUEST_KWARGS={
    #  for example you can use your proxy here
    'proxy_url': 'http://user:password@<ip_address>:<port>/',
}
DEBUG = False  #  verbose level

#  raspberry pi settings
PIR_OUT = 18  # pin with logic signal from PIR Motion Sensor
