import utime

class HCSR04():
    def __init__(self, trig, echo):
        self.trig=trig
        self.echo=echo

    def getDistance(self):
        self.trig.high()
        utime.sleep_us(20)
        self.trig.low()
        
        while self.echo.value() == 0:
            pass
        off = utime.ticks_us()
        while self.echo.value() == 1:
            pass
        on = utime.ticks_us()

        diff = on - off
        dist = (diff * 0.0343) / 2
        return dist
