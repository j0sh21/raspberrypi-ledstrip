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
            brightChanged = True
            time.sleep(0.01)
            brightChanged = False
            bright = bright + BRIGHTNESS_STEPS
            print("Current brightness: %d" % bright)
            setLights(RED_PIN, bright)
            setLights(GREEN_PIN, bright)
            setLights(BLUE_PIN, bright)

        if c == '-' and bright > 0 and not brightChanged:
            brightChanged = True
            time.sleep(0.01)
            brightChanged = False
            bright = bright - BRIGHTNESS_STEPS
            print("Current brightness: %d" % bright)
            setLights(RED_PIN, bright)
            setLights(GREEN_PIN, bright)
            setLights(BLUE_PIN, bright)

        if c == 'p' and state:
            state = False
            print("Pausing...")
            time.sleep(0.1)
            setLights(RED_PIN, 0)
            setLights(GREEN_PIN, 0)
            setLights(BLUE_PIN, 0)

        if c == 'r' and not state:
            state = True
            print("Resuming...")

        if c == 'c' and not abort:
            abort = True
            break

def fadeLed():
    global r
    global g
    global b

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
    ###### CONFIGURE THIS ###########
    # The Pins. Use Broadcom numbers.
    RED_PIN = 17
    GREEN_PIN = 22
    BLUE_PIN = 24
    # Number of color changes per step
    # (more is faster, less is slower).
    # You also can use 0.X floats.
    STEPS = 0.01
    BRIGHTNESS_STEPS = 25
    ############## END ##############

    # initial brightness and color
    bright = 255
    r = 255.0
    g = 0
    b = 0

    # global variables needed
    brightChanged = False
    abort = False
    state = True

    pi = pigpio.pi()

    start_new_thread(checkKey, ())

    print("+ / - = Increase / Decrease brightness")
    print("p / r = Pause / Resume")
    print("c = Abort Program")

    setLights(RED_PIN, r)
    setLights(GREEN_PIN, g)
    setLights(BLUE_PIN, b)

    fadeLed()

    print("Aborting...")

    setLights(RED_PIN, 0)
    setLights(GREEN_PIN, 0)
    setLights(BLUE_PIN, 0)

    time.sleep(0.5)

    pi.stop()
