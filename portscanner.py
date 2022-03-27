import socket
from IPy import IP

def check_ip(ipaddress):
    try:
        IP(ipaddress)
    except ValueError:
        return socket.gethostbyname(ipaddress)

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ipaddress, port))
        print('Port ' + str(port) + ' is open')
    except:
        print('Port ' + str(port) + ' is closed')

ipaddress = input('Enter IP Address: ')
converted_ip = check_ip(ipaddress)
print('IP: ' + str(converted_ip))

for port in (80, 22, 8080):
    scan_port(converted_ip, port)