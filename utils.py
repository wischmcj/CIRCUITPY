# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython I2C Device Address Scan"""
import struct
import time
import board
from micropython import const
from adafruit_bus_device import i2c_device

try:
    from typing import List
    from typing_extensions import Literal
    from circuitpython_typing import WriteableBuffer, ReadableBuffer
    from busio import I2C
except ImportError:
    pass

# To create I2C bus on specific pins
# import busio
# i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040
def get_devices(i2c_in):
    while not i2c_in.try_lock():
        pass

    try:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c_in.scan()],
        )
        time.sleep(2)

    finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
        i2c_in.unlock()# Write your code here :



# _HTU31D_READSERIAL = const(0x0A)  # Read Out of Serial Register
# _HTU31D_SOFTRESET = const(0x1E)
# _HTU31D_CONVERSION = const(0x40)  # Start a conversion
# _HTU31D_READSERIAL = const(0x0A)  # Read Out of Serial Register
_CHANNEL_MAX = 4

_DEFAULT_ADDRESS = const(0x70)
#_DEFAULT_ADDRESS = const(0x40)

class Ixc_channel(i2c_device.I2CDevice):
    """Helper class to represent a Stemma QT port recieving the end of a daisy chain
      Takes care of the necessary I2C commands for channel switching. This class needs to
    behave like an I2CDevice."""

    def __init__(self, ixc: str , address: int) -> None:
        self.ixc = ixc
        self.reset()
        self.super().__init__(self.ixc.i2c, address)
        self.buffer = bytearray(6)
        # self.channel_switch = bytearray([1 << channel])

    def reset(self) -> None:
        """Perform a soft reset of the sensor, resetting all settings to their power-on defaults"""
        # self._buffer[0] = _HTU31D_SOFTRESET
        self.write(self.buffer, end=1)
        time.sleep(0.015)

    # def try_lock(self) -> bool:
    #     """Pass through for try_lock."""
    #     while not self.ixc.i2c.try_lock():
    #         time.sleep(0)
    #     self.ixc.i2c.writeto(self.ixc.address, self.channel_switch)
    #     return True

    # def unlock(self) -> bool:
    #     """Pass through for unlock."""
    #     self.ixc.i2c.writeto(self.ixc.address, b"\x00")
    #     return self.ixc.i2c.unlock()

    # def readfrom_into(self, address: int, buffer: ReadableBuffer, **kwargs):
    #     """Pass through for readfrom_into."""
    #     if address == self.ixc.address:
    #         raise ValueError("Device address must be different than Ixc_channel address.")
    #     return self.ixc.i2c.readfrom_into(address, buffer, **kwargs)

    # def writeto(self, address: int, buffer: WriteableBuffer, **kwargs):
    #     """Pass through for writeto."""
    #     if address == self.ixc.address:
    #         raise ValueError("Device address must be different than Ixc_channel address.")
    #     return self.ixc.i2c.writeto(address, buffer, **kwargs)

    # def writeto_then_readfrom(
    #     self,
    #     address: int,
    #     buffer_out: WriteableBuffer,
    #     buffer_in: ReadableBuffer,
    #     **kwargs
    # ):
    #     """Pass through for writeto_then_readfrom."""
    #     # In linux, at least, this is a special kernel function call
    #     if address == self.ixc.address:
    #         raise ValueError("Device address must be different than Ixc_channel address.")
    #     return self.ixc.i2c.writeto_then_readfrom(
    #         address, buffer_out, buffer_in, **kwargs
    #     )

    # def scan(self) -> List[int]:
    #     """Perform an I2C Device Scan"""
    #     return self.ixc.i2c.scan()


class Multi_qt:
    """Class which provides interface to Ixc I2C multiplexer."""

    def __init__(self, i2c: I2C, addresses: int ) -> None:
        self.i2c = i2c
        self.addresses = addresses
        self.channels = [None] * (_CHANNEL_MAX+1)
        # for idx, addr in enumerate(addresses):
        #     self[addr]

    def __len__(self) -> Literal[4]:
        return len(self.channels)

    def __getitem__(self, key: Literal[0, 1, 2, 3]) -> "Ixc_channel":
        if not 0 <= key <= len(self.addresses):
            raise IndexError(f"Channel must be an integer in the range: 0-{_CHANNEL_MAX}")
        addr = self.addresses[key]
        if addr is None:
            raise ValueError(f"Channel {key} is not enabled.")
        # if self.channels[key] is None:
        self.channels[key] = Ixc_channel(self, addr)
        return self.channels[key]
            
    def scan(self) -> List[int]:
        for channel in range(8):
            if self[channel].try_lock():
                print("Channel {}:".format(channel), end="")
                addresses = self[channel].scan()
                print([hex(address) for address in addresses if address != 0x70])
                self[channel].unlock()