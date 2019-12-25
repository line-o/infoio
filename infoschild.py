import datetime
import math
from functools import partialmethod
from itertools import repeat
from collections import deque
try:
    from rpi_ws281x import *
except ImportError:
    from ada_mock import Adafruit_NeoPixel
    from ada_mock import Color

def colorToList (color):
    r_result = divmod(color, 65536)
    red = r_result[0]
    g_result = divmod(r_result[1], 256)
    green = g_result[0]
    blue = g_result[1]
    return [red, green, blue]

def listToColor (list):
    return (list[0] << 16) | (list[1] << 8) | list[2]

class Infoschild(object):
    # LED strip configuration:
    LED_COUNT      = 240      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    framelength = 0.10       # seconds between each frame (wobbles between 12.9 and 20.1)
    tick = 0                 # each frame adds one tick - (may be useful for syncing multiple clients)
    LED_INFOTEXT_START = 0
    LED_RAUMSTATION_START = 139
    GREEN = [0, 187, 49]
    ORANGE = [254, 80, 0]
    WHITE = [240, 240, 240]
    MAX_VOTES = 10

    def __init__ (self):
        self.delta = 0
        self.blinkState = 0
        self.votes = deque(repeat(0, Infoschild.MAX_VOTES), Infoschild.MAX_VOTES)
        self.hope = sum(self.votes) / Infoschild.MAX_VOTES
        self.last_time = datetime.datetime.now()
        self.strip = Adafruit_NeoPixel(Infoschild.LED_COUNT, Infoschild.LED_PIN, Infoschild.LED_FREQ_HZ, Infoschild.LED_DMA, Infoschild.LED_INVERT, Infoschild.LED_BRIGHTNESS, Infoschild.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def mixChannel(self, ca, cb, v):
        return round(ca + v * (cb - ca))

    def mixColor(self, a, b, v):
        return [
            self.mixChannel(a[0], b[0], v),
            self.mixChannel(a[1], b[1], v),
            self.mixChannel(a[2], b[2], v)
        ]

    def getTextColor(self):
        # hope > 0.5 : mix(orange, white, )
        # Hope > 0.5 : mix( white, green, (x-0.5) *2)
        # TODO mix with current color
        if self.hope == 0:
            return Infoschild.WHITE
        if self.hope > 0:
            return self.mixColor(Infoschild.WHITE, Infoschild.GREEN, self.hope)
        if self.hope < 0:
            return self.mixColor(Infoschild.ORANGE, Infoschild.WHITE, self.hope * -1)

    def blink(self):
        color = Infoschild.WHITE
        if (self.blinkState % 2 == 1): color = [255,255,255]

        for i in range(Infoschild.LED_RAUMSTATION_START, Infoschild.LED_COUNT):
            self.strip.setPixelColor(i, listToColor(color))
        
        if (self.blinkState > 0): self.blinkState -= 1


    def setHope(self, hope):
        self.votes.append(hope)
        self.hope = sum(self.votes) / Infoschild.MAX_VOTES
        self.blinkState = 3

    def getHope(self):
        return self.hope

    def showHope(self):        
        c = listToColor(self.getTextColor())

        for i in range(Infoschild.LED_INFOTEXT_START, Infoschild.LED_RAUMSTATION_START):
            self.strip.setPixelColor(i, c)

    def show(self):
        # print(self.delta.microseconds)
        # print(self.blinkState)
        self.strip.show()

    def step(self, loop):
        # self.show()
        now = datetime.datetime.now()
        self.tick += 1
        self.delta = now - self.last_time
        self.last_time = now
        self.loop = loop
        self.blink()
        self.showHope()
        t = loop.time()
        o = t % Infoschild.framelength
        nextTick = t - o + Infoschild.framelength
        loop.run_in_executor(None, self.show)
        loop.call_at(nextTick, self.step, loop)
