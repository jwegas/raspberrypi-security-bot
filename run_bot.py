#!/usr/bin/env python
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
from bot import Bot


if __name__ == "__main__":
    security_bot = Bot()
    security_bot.run()
    GPIO.cleanup()
