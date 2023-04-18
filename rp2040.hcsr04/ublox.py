# Wi-Fi AP Mode Example
#
# This example shows how to use Wi-Fi in Access Point mode.
import network, socket, sys, time, gc, _thread, select, re

SSID ='Nano_RP2040_1009'   # Network SSID
KEY  ='1234567890'  # Network key (must be 10 chars)
HOST = ''           # Use first available interface
PORT = 1009         # Arbitrary non-privileged port

# Init wlan module and connect to network
wlan = network.WLAN(network.AP_IF) # Create a WLAN network interface object
wlan.active(True) # Activate (“up”) or deactivate (“down”) network interface
wlan.config(essid=SSID, key=KEY, security=wlan.WEP, channel=2)
print("AP mode started. SSID: {} IP: {}".format(SSID, wlan.ifconfig()[0]))


class UBLOX:
    def __init__(self):
        self._client = None
        self._server = None
        self._poller = None
        self.starts()

    def starts(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind and listen
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._server.bind([HOST, PORT])
        except OSError as e:
            print('bind Error :', e)

            return False
        self._server.listen(1)

        # Set server socket to blocking
        #self._server.setblocking(True)

        _thread.start_new_thread(self.shuttle, ())
        return True

    def shuttle(self):
        print('Waiting for connections..')
        try:
            self._client, addr = self._server.accept()
        except OSError as e:
            print('accept Error :', e)
            return

        print('Connected to ' + addr[0] + ':' + str(addr[1]))

        self._poller = select.poll()  # polling for I/O events
        self._poller.register(self._client, select.POLLIN)

    def restarts(self):
        try:
            self._client.close()
            self._server.close()
        except AttributeError as e:
            print('close :', e)
        self._client = None
        self._server = None
        self._poller = None

        self.starts()

    def send(self, data):
        try:
            if self._client:
                self._client.send(f"sonarAlt: {data}" "\r\n")
        except OSError as e:
            print('send Error :', e)
            self.restarts()

    def read(self):
        data = bytes()
        while self._poller and self._client:
            try:
                if self._poller.poll(1):  # time in milliseconds
                    data += self._client.read(1)
                else:
                    break
            except OSError as e:
                print('recv Error :', e)
                self.restarts()
                break

        #print(data)
        #return re.sub(b'\r\n', b'', data)
        cmd = re.search(b'([0-9])\r\n', data)
        return cmd and cmd.group(1)
