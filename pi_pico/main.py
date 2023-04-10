from machine import Pin, Timer, UART
from time import sleep
from hcsr04 import HCSR04
from esp12s import ESP12S

#machine.freq(240000000)

import gc
print('여유:', str(gc.mem_free()))
print('배치:', str(gc.mem_alloc()))
#gc.collect()

led = Pin(25, Pin.OUT)
timer = Timer(period=2000, mode=Timer.PERIODIC, callback=lambda t: led.toggle())

sonar = HCSR04(Pin(15, Pin.OUT), Pin(14, Pin.IN))
wifi = ESP12S(1, 115200)

while True:
    distance = sonar.getDistance()
    #distance = ultra()
    print(str(distance) + ' cm')
    
    try:
        wifi.send(str(distance))
        
        cmd = wifi.read()
        if cmd:
            print('cmd:', cmd)
    except Exception as e:
        print(e)
        gc.collect()
    
    sleep(0.5)
