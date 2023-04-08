import telnetlib
import time

HOST = "192.168.212.220"
PORT = "7171"
tn = telnetlib.Telnet(HOST, PORT)
tn.mt_interact() #이 객체에 이미 print 기능 내장 되어 있어 별도의 print문이 필요 없다

# login
password = input("Enter password: ")
tn.read_until(b"\n")
tn.write(password.encode('ascii') + b'\n')
tn.read_until(b"End of commands")

# print(tn.read_all().decode('ascii'))

if __name__ == "__main__":
    r = tn('192.168.212.220')