import utime

class HCSR04:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        
    def getDistance(self):
        self.trig.high()
        utime.sleep_us(20)
        self.trig.low()
        
        off = utime.ticks_us()
        while self.echo.value() == 0:
            if 500 < utime.ticks_us() - off:
                return -1
        off = utime.ticks_us()
        while self.echo.value() == 1:
            if 36000 < utime.ticks_us() - off:
                break
        on = utime.ticks_us()
        
        diff = on - off
        dist = (diff * 0.0343) / 2
        return dist