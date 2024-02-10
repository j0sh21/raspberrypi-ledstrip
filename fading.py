#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------
# File        fading.py
# Authors     David Ordnung
#             (Modified in 2024 for python3 by the DoxBox Team)
# License     GPLv3
# Web         http://dordnung.de/raspberrypi-ledstrip/
# -----------------------------------------------------
#
# Copyright (C) 2014-2017 David Ordnung
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#
# This script needs running pigpio (http://abyz.co.uk/rpi/pigpio/)

import pigpio
import time
from _thread import start_new_thread


def updateColor(color, step):
    color += step

    if color > 255:
        return 255
    if color < 0:
        return 0
    return color

def setLights(pin, brightness):
    realBrightness = int(int(brightness) * (float(bright) / 255.0))
    pi.set_PWM_dutycycle(pin, realBrightness)

def getCh():
    ch = input("Input: ")
    return ch

def checkKey():
    global bright
    global brightChanged
    global state
    global abort

    while True:
        c = getCh()

        if c == '+' and bright < 255 and not brightChanged:
            bright = bright + BRIGHTNESS_STEPS

        if c == '-' and bright > 0 and not brightChanged:
            bright = bright - BRIGHTNESS_STEPS

        if c == 'p' and state:
            state = False
            print("Pausing...")
            bright = 0

        if c in("+","-","p"):
            brightChanged = True
            time.sleep(0.01)
            brightChanged = False
            print("Current brightness: %d" % bright)
            setLights(RED_PIN, bright)
            setLights(GREEN_PIN, bright)
            setLights(BLUE_PIN, bright)

        if c == 'r' and not state:
            state = True
            print("Resuming...")

        if c == 'c' and not abort:
            abort = True
            break

def fadeLed(r, g, b):
    global state
    global abort
    
    while not abort:
        if state and not brightChanged:
            if r == 255 and b == 0 and g < 255:
                g = updateColor(g, STEPS)
                setLights(GREEN_PIN, g)
            elif g == 255 and b == 0 and r > 0:
                r = updateColor(r, -STEPS)
                setLights(RED_PIN, r)
            elif r == 0 and g == 255 and b < 255:
                b = updateColor(b, STEPS)
                setLights(BLUE_PIN, b)
            elif r == 0 and b == 255 and g > 0:
                g = updateColor(g, -STEPS)
                setLights(GREEN_PIN, g)
            elif g == 0 and b == 255 and r < 255:
                r = updateColor(r, STEPS)
                setLights(RED_PIN, r)
            elif r == 255 and g == 0 and b > 0:
                b = updateColor(b, -STEPS)
                setLights(BLUE_PIN, b)

if __name__ == "__main__":
    # global variables needed
    brightChanged = False
    abort = False
    state = True
    # The Pins. Use Broadcom numbers.
    RED_PIN = 17
    GREEN_PIN = 22
    BLUE_PIN = 24
    # Number of color changes per step (more is faster, less is slower). You also can use 0.X floats.
    STEPS = 0.01
    # Change brightness 0-255 in steps (more is bigge change, up or down. less is smaller change)
    BRIGHTNESS_STEPS = 25
    # initial brightness
    bright = 255
    # initial color
    r, g, b = 255.0, 0, 0

    pi = pigpio.pi()
    start_new_thread(checkKey, ())
    print("+ / - = Increase / Decrease brightness\np / r = Pause / Resume\nc = Abort Program")

    setLights(RED_PIN, r)
    setLights(GREEN_PIN, g)
    setLights(BLUE_PIN, b)

    fadeLed(r, g, b)

    print("Aborting...")
    bright = 0
    setLights(RED_PIN, bright)
    setLights(GREEN_PIN, bright)
    setLights(BLUE_PIN, bright)
    time.sleep(0.5)
    pi.stop()
