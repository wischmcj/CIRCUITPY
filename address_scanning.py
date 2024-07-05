"""CircuitPython I2C Device Address Scan"""
import time
import board
import busio

# List of potential I2C busses
ALL_I2C = ("board.I2C()", "board.STEMMA_I2C()", "busio.I2C(board.GP1, board.GP0)")
def get_valid_buses():
    # Determine which busses are valid
    found_i2c = []
    for name in ALL_I2C:
        try:
            print("Checking {}...".format(name), end="")
            bus = eval(name)
            bus.unlock()
            found_i2c.append((name, bus))
            print("ADDED.")
        except Exception as e:
            print("SKIPPED:", e)
    return found_i2c

def scan_valid_busses():
    # Scan valid busses
    addrs = []
    found_i2c = get_valid_buses()
    if len(found_i2c):
        print("-" * 40)
        print("I2C SCAN")
        print("-" * 40)
        for bus_info in found_i2c:
            name = bus_info[0]
            bus = bus_info[1]

            while not bus.try_lock():
                pass
            addrs_found = [hex(device_address) for device_address in bus.scan()]
            print(
                name,
                "addresses found:",
                addrs_found,
            )
            addrs.extend(addrs_found)

            bus.unlock()

        time.sleep(2)   
    else:
        print("No valid I2C bus found.")
    return addrs