from machine import UART
import utime
import re

class ESP12S:
    def __init__(self, nPort, baudrate=115200):
        self.uart = UART(nPort, baudrate)
        print(self.uart)
        self.setup()

    def setup(self):
        self.uart.write("ATE0" "\r\n"), self.wait()
        self.uart.write("AT+CWMODE=3" "\r\n"), self.wait()
        #self.uart.write("AT+CWSAP=\"poly\",\"1234\",1,2" "\r\n"); delay(5)
        self.uart.write("AT+CIPMUX=1" "\r\n"), self.wait()
        self.uart.write("AT+CIPSERVER=1,1009" "\r\n"), self.wait()
        self.uart.write("AT+CIPSTO=0" "\r\n"), self.wait()
        #self.uart.write("AT+CIPMODE=0" "\r\n"), self.wait()
        print("setup...")

    def wait(self, outcode=(b'OK\r\n', b'ERROR\r\n'), timeout=5000):
        elp = utime.ticks_ms()
        rev, res = bytes(), 'None'
        while (utime.ticks_ms() - elp) < timeout:
            if self.uart.any():
                rev += self.uart.read(1)
                if any([code in rev for code in outcode]):
                    #print('out: break')
                    break
        try:
            res = str(rev or b'None', 'ascii')
        except Exception as e:
            res = str('[err1]' + str(e))

        print('resp:', res)

    def send(self,txt):
        #print('send:', txt)
        size = len(txt) + 12  ## len("AT+CIPSENDEX=0," "\r\n")
        #print('size:', size)
        self.uart.write(f"AT+CIPSENDEX=0,{size}" "\r\n"), utime.sleep_ms(2)
        self.uart.write(f"sonarAlt: {txt}" "\r\n"), utime.sleep_us(size)
        
    def read(self):
        elp = utime.ticks_ms()
        rev = bytes()
        while self.uart.any() > 0:
            rev += self.uart.read(1)  ## +IPD,1,3:9
        #print('rev:', rev)
        if rev:
            cmd = re.search('\+IPD,[0-9]+,[0-9]+:(\w+)\r\n', rev)
            if cmd:
                #print('cmd:', cmd.group(0))
                try:
                    return str(cmd.group(1), 'ascii')
                except Exception as e:
                    print('[err2]' + str(e))
