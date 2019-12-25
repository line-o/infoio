from itertools import repeat

class Adafruit_NeoPixel(object):

    def __init__ (self, c, p, hz, dma, invert, brightness, ch):
        self._data = list(repeat(0, c))

    def begin(self):
        return None

    def show(self):
        print(self._data)
        return None

    def getPixelColor(self, n):
        return self._data[n]

    def setPixelColor(self, n, c):
        self._data[n] = c

def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue
