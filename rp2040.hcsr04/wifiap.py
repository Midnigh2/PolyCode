import network, socket, sys, time, gc

SSID = '' # 네트워크 SSID
KEY  = '' # 네트워크 키(10자)
HOST = '' # 사용 가능한 첫번째 인터페이스
PORT = 8080 # 포트번호

wlan = network.WLAN(network.AP_IF)
wlan.active(True)
wlan.config(essid=SSID, key=KEY, security=wlan.WEP, channel=2)
print("AP mode started. SSID: {} IP: {}".format(SSID, wlan.ifconfig()[0]))

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise OSError("Timeout")
        data.extend(packet)
    return data

def start_streaming(server):
    print ('Waiting for connections..')
    client, addr = server.accept()

    client.settimeout(5.0)
    print ('Connected to ' + addr[0] + ':' + str(addr[1]))

    clock = time.clock()
    while (True):
        try:
            # Read data from client
            data = recvall(client, 1024)
            # Send it back
            client.send(data)
        except OSError as e:
            print("start_streaming(): socket error: ", e)
            client.close()
            break

while (True):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind([HOST, PORT])
        server.listen(1)

        # 소켓차단
        server.setblocking(True)
        while (True):
            start_streaming(server)
    except OSError as e:
        server.close()
        print("Server socket error: ", e)
