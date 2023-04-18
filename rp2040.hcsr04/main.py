from machine import Pin, Timer, UART
from time import sleep
from hcsr04 import HCSR04
from ublox import UBLOX

import gc

print('free:', str(gc.mem_free()))
print('allc:', str(gc.mem_alloc()))
gc.collect()

sonar = HCSR04(Pin(25, Pin.OUT), Pin(15, Pin.IN))
wifi = UBLOX()
uart = UART(0, 115200)

acts = {b'1': lambda: Pin(20, Pin.OUT).toggle(),
        b'2': lambda: Pin(19, Pin.OUT).toggle(),
        b'3': lambda: Pin(18, Pin.OUT).toggle(),
        b'4': lambda: Pin(17, Pin.OUT).toggle(),
        b'5': lambda: Pin(16, Pin.OUT).toggle()}

while True:
    distance = sonar.getDistance()
    print(str(distance) + ' cm')

    try:
        wifi.send(str(distance))
        uart.write(str(distance) + "\r\n")

        cmd = wifi.read()
        if cmd:
            print('cmd:', cmd)
            acts.get(cmd, lambda: None)()
        if uart.any():
            cmd = uart.read().split(b'\r')[0]
            print('uart:', cmd)
            acts.get(cmd, lambda: None)()
    except OSError as e:
        print('[err3]' + str(e))
        gc.collect()

    sleep(0.5)

    Pin(6, Pin.OUT).toggle()
