from pymodbus.client import ModbusTcpClient
import time
import threading

def check(client):
    while True:
        result = client.read_holding_registers(130, 1)
        print(result.registers)
        time.sleep(0.1)


client = ModbusTcpClient('192.168.213.79')

t = threading.Thread(target=check, args=(client,))
t.start()
t.join()

client.close()