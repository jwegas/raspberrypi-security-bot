#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import picamera
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)


class PIRSensor:
    def __init__(self, out_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(out_pin, GPIO.IN)
        GPIO.add_event_detect(out_pin, GPIO.RISING)

        self._out_pin = out_pin

    def get_output(self):
        return GPIO.event_detected(self._out_pin)


class Camera:
    def __init__(self):
        camera = picamera.PiCamera()
        camera.vflip = True
        camera.hflip = True
        self.camera = camera

        self.pic_path = 'media/tmp_photo.jpg'

    def capture(self):
        self.camera.capture(self.pic_path)
        return self.pic_path
