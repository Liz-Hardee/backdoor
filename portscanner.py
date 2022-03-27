import socket
from IPy import IP

ipaddress = input('Enter IP Address: ')

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.connect(ipaddress, port)
        print('Port ' + str(port) + ' is open')
    except:
        print('Port ' + str(port) + ' is closed')

for port in (22,80,8080):
    scan_port(ipaddress, port)