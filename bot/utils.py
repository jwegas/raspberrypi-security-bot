#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import picamera
import RPi.GPIO as GPIO
import time


class PIRSensor:

    """Setup PIR sensor.

    * Create instance for PIR sensor and connect it to pin on Raspberry Pi;
    * Setup kind of sensor signal

    Args:
        sensor_pin (int): pin number (according BCM mode) which PIR
        sensor is connected to.
    """

    def __init__(self, sensor_pin):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor_pin, GPIO.IN)
        GPIO.add_event_detect(sensor_pin, GPIO.RISING)

        self._sensor_pin = sensor_pin

    def get_output(self):
        """Get output of PIR sensor

        Returns:
            boolean: whether movement was detected (True) or not (False).
        """

        return GPIO.event_detected(self._sensor_pin)


class Camera:
    """Setup Raspberry Pi Camera

    * Create instance for Camera, setup cache path and some image properties
    * Capture pic

    """
    def __init__(self, vflip=True, hflip=True):

        camera = picamera.PiCamera()
        camera.vflip = vflip
        camera.hflip = hflip
        camera.led = False
        self.camera = camera
        self.pic_path = 'media/tmp_photo.jpg'

    def capture(self):
        """Capture one frame from Camera and return path where pic was saved in.

        Returns:
            str: Path where pic was saved in.
        """
        self.camera.capture(self.pic_path)
        return self.pic_path
