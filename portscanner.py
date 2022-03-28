import sys
import socket
from IPy import IP

def option_list():
    print('\n\n                       --OPTIONS--')
    print('-i, --ipaddress......provide target ip from command line\n')
    print('-l, --list........provide a list or .csv of IPs or hosts\n')
    print('-h, --help................................prints options\n\n')

def check_ip(ipaddress):
    try:
        IP(ipaddress)
        return(ipaddress)
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

def try_ports(ipaddress):
    converted_ip = check_ip(ipaddress)
    print('\nIP: ' + str(converted_ip))
    for port in (20, 21, 22, 23,25,53, 80, 110, 119,
                 123, 143, 161, 194, 443):
        scan_port(converted_ip, port)

arglst = iter(sys.argv)

for option in arglst:
    if str(option) == '-h' or str(option) == '--help':
        option_list()
        exit()
    elif str(option) == '-i' or str(option) == '--ipaddress':
        try: 
            try_ports(next(arglst))
        except StopIteration:
            print('Please enter a valid IP or hostname\n')
        exit()
    elif str(option) == '-l' or str(option) == '--list':
        while arglst:
            try:
                try_ports(next(arglst))
            except StopIteration:
                break
                


