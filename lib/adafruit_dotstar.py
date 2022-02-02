# SPDX-FileCopyrightText: 2016 Damien P. George
# SPDX-FileCopyrightText: 2017 Ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2017 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Roy Hooper
#
# SPDX-License-Identifier: MIT

"""
`adafruit_dotstar` - DotStar strip driver (for CircuitPython 5.0+ with _pixelbuf)
=================================================================================

* Author(s): Damien P. George, Limor Fried, Scott Shawcroft & Rose Hooper
"""

# pylint: disable=ungrouped-imports
import busio
import digitalio

try:
    import adafruit_pixelbuf
except ImportError:
    try:
        import _pixelbuf as adafruit_pixelbuf
    except ImportError:
        import adafruit_pypixelbuf as adafruit_pixelbuf

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DotStar.git"

START_HEADER_SIZE = 4

# Pixel color order constants
RBG = "PRBG"
"""Red Blue Green"""
RGB = "PRGB"
"""Red Green Blue"""
GRB = "PGRB"
"""Green Red Blue"""
GBR = "PGBR"
"""Green Blue Red"""
BRG = "PBRG"
"""Blue Red Green"""
BGR = "PBGR"
"""Blue Green Red"""


class DotStar(adafruit_pixelbuf.PixelBuf):
    """
    A sequence of dotstars.

    :param ~microcontroller.Pin clock: The pin to output dotstar clock on.
    :param ~microcontroller.Pin data: The pin to output dotstar data on.
    :param int n: The number of dotstars in the chain
    :param float brightness: Brightness of the pixels between 0.0 and 1.0
    :param bool auto_write: True if the dotstars should immediately change when
        set. If False, `show` must be called explicitly.
    :param str pixel_order: Set the pixel order on the strip - different
         strips implement this differently. If you send red, and it looks blue
         or green on the strip, modify this! It should be one of the values above.
    :param int baudrate: Desired clock rate if using hardware SPI (ignored if
        using 'soft' SPI). This is only a recommendation; the actual clock
        rate may be slightly different depending on what the system hardware
        can provide.

    Example for Gemma M0:

    .. code-block:: python

        import adafruit_dotstar
        import time
        from board import *

        RED = 0x100000

        with adafruit_dotstar.DotStar(APA102_SCK, APA102_MOSI, 1) as pixels:
            pixels[0] = RED
            time.sleep(2)

    .. py:method:: DotStar.show()

        Shows the new colors on the dotstars themselves if they haven't already
        been autowritten.

        The colors may or may not be showing after this function returns because
        it may be done asynchronously.

    .. py:method:: DotStar.fill(color)

        Colors all dotstars the given ***color***.

    .. py:attribute:: brightness

        Overall brightness of all dotstars (0 to 1.0)
    """

    def __init__(
        self,
        clock,
        data,
        n,
        *,
        brightness=1.0,
        auto_write=True,
        pixel_order=BGR,
        baudrate=4000000
    ):
        self._spi = None
        try:
            self._spi = busio.SPI(clock, MOSI=data)
            while not self._spi.try_lock():
                pass
            self._spi.configure(baudrate=baudrate)

        except (NotImplementedError, ValueError):
            self.dpin = digitalio.DigitalInOut(data)
            self.cpin = digitalio.DigitalInOut(clock)
            self.dpin.direction = digitalio.Direction.OUTPUT
            self.cpin.direction = digitalio.Direction.OUTPUT
            self.cpin.value = False

        # Supply one extra clock cycle for each two pixels in the strip.
        trailer_size = n // 16
        if n % 16 != 0:
            trailer_size += 1

        # Four empty bytes for the header.
        header = bytearray(START_HEADER_SIZE)
        # 0xff bytes for the trailer.
        trailer = bytearray(b"\xff") * trailer_size

        super().__init__(
            n,
            byteorder=pixel_order,
            brightness=brightness,
            auto_write=auto_write,
            header=header,
            trailer=trailer,
        )

    def deinit(self):
        """Blank out the DotStars and release the resources."""
        self.fill(0)
        self.show()
        if self._spi:
            self._spi.deinit()
        else:
            self.dpin.deinit()
            self.cpin.deinit()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    @property
    def n(self):
        """
        The number of dotstars in the chain (read-only)
        """
        return len(self)

    def _transmit(self, buffer):
        if self._spi:
            self._spi.write(buffer)
        else:
            self._ds_writebytes(buffer)

    def _ds_writebytes(self, buffer):
        for b in buffer:
            for _ in range(8):
                self.dpin.value = b & 0x80
                self.cpin.value = True
                self.cpin.value = False
                b = b << 1
        self.cpin.value = False