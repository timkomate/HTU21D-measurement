#!/usr/bin/python
import datetime
import sys
import time
import board
import busio
from adafruit_htu21d import HTU21D

# Sampling frequency
dt = 3

i2c = busio.I2C(board.SCL, board.SDA)
sensor = HTU21D(i2c)

while True:
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    print(f"temperature: {temperature:.2f}, humidity: {humidity:.2f}")
    time.sleep(dt)
