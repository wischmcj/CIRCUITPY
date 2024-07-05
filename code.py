from time import sleep
import board
from utils import get_devices, Multi_qt
from adafruit_htu31d import HTU31D
from dps310.basic import DPS310
from address_scanning import scan_valid_busses
# from adafruit_htu31d import HTU31D

i2c = board.STEMMA_I2C()
# For using the built-in STEMMA QT connector on a microcontroller
print(dir(i2c))

htu = HTU31D(i2c)
print(dir(htu))
print("Found HTU31D with serial number", hex(htu.serial_number))
htu.heater = True
print("Heater is on?", htu.heater)
htu.heater = False
print("Heater is on?", htu.heater)
if 1==1:
    temperature, relative_humidity = htu.measurements
    temp_f = "(%0.1f F)" % ((temperature*9/5)+32)
    temp_c = "%0.1f C" % (temperature)
    print(f"Temperature: {temp_c} {temp_f} ")
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    sleep(1)

dps = DPS310(i2c)
print(dir(dps))
print("Found HTU31D with serial number", hex(dps.serial_number))
# dps.heater = Trueq

dps.heater = False
print("Heater is on?", dps.heater)
while True:
    pressure = dps.pressure
    altitude = dps.altitude
    dps_temp = dps.temperature
    htu_temp, relative_humidity = htu.measurements

    htu_temp_f = "(%0.1f F)" % ((htu_temp*9/5)+32)
    htu_temp_c = "%0.1f C" % (htu_temp)

    dps_temp_c = "%0.1f C" % (dps_temp)
    dps_temp_f = "(%0.1f F)" % ((dps_temp*9/5)+32)
    
    print("DPS Pressure: %0.1f " % pressure)
    print("DPS Altitude: %0.1f " % altitude)
    print(f"DPS Temperature: {dps_temp_c} {dps_temp_f} ")

    print(f"HTU Temperature: {htu_temp_c} {htu_temp_f} ")
    print("HTU Humidity: %0.1f %%" % relative_humidity)

    print("")
    sleep(1)


    
# device_addrs = scan_valid_busses()

# mq = Multi_qt(i2c,device_addrs)
# print("Hello You")
# mq.scan()