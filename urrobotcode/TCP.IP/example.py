from pymodbus.client import ModbusTcpClient
import time
#write
client = ModbusTcpClient('192.168.213.79')

client.write_register(129, 32)

client.write_register(128, 14)

client.write_register(127, 15)

#read
while True:
    result = client.read_holding_registers(130, 1)
    print(result.registers)
    time.sleep(0.1)

client.close()