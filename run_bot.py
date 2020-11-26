#!/usr/bin/env python
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
from bot import Bot


if __name__ == "__main__":

    #  create instance for Bot and run it
    security_bot = Bot()
    security_bot.run()

    #  clean PINs assigments after Bot is stopped
    GPIO.cleanup()
