from time import sleep
import board
from adafruit_htu31d import HTU31D


i2c = board.STEMMA_I2C()
def solo_htu(i2c):
    htu = HTU31D(i2c)
    print(dir(htu))
    print("Found HTU31D with serial number", hex(htu.serial_number))

    while True:
        temperature, relative_humidity = htu.measurements
        temp_f = "(%0.1f F)" % ((temperature*9/5)+32)
        temp_c = "%0.1f C" % (temperature)
        print(f"Temperature: {temp_c} {temp_f} ")
        print("Humidity: %0.1f %%" % relative_humidity)
        print("")
        sleep(1)