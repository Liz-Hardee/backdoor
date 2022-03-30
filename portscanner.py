import sys
import socket
import datetime
import dns.reversename, dns.resolver
from IPy import IP
from os.path import exists

from sympy import O

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

def get_dns(ipaddress):
    address = dns.reversename.from_address(str(ipaddress))
    return (str(dns.resolver.resolve(address, 'PTR')[0]))

def write_ports(ipaddress, dnsname, portlist):
    if exists('scanlog.log'):
        access = 'a'
    else:
        access = 'w'
    with open('scanlog.log', access) as wfile:
        wfile.writelines(['Hostname: ' + dnsname + '\n', 
                         'IP: ' + str(ipaddress) + '\n', 
                         'Date Scanned: ' + str(datetime.datetime.now()) + 
                         '\n', 'Open Ports: '])
        for port in portlist:
            wfile.write(str(port) + ', ')
        wfile.write('\n\n')



def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.2)
        sock.connect((ipaddress, port))
        if '-v' in sys.argv:
            print('Port ' + str(port) + ' is open')
            return port
    except:
        if '-v' in sys.argv:
            print('Port ' + str(port) + ' is closed')
            return 0

def try_ports(ipaddress):
    openports = []
    converted_ip = check_ip(ipaddress)
    converted_dns = get_dns(converted_ip)
    if '-v' in sys.argv:
        print('\nHostname: ' + converted_dns)
        print('\nIP: ' + str(converted_ip))
    for port in (20, 21, 22, 23,25,53, 80, 110, 119,
                 123, 143, 161, 194, 443, 32400):
        currport = scan_port(converted_ip, port)
        if currport != 0: 
            openports.append(currport)
    if '-o' in sys.argv:
        try:
            write_ports(converted_ip, converted_dns, openports)
            if '-v' in sys.argv:
                print('File successfully written\n')
        except:
            print('Error: Unable to write to file\n')

arglst = iter(sys.argv)

for option in arglst:
    if (str(option) == '-h' or str(option) == '--help' or
        len(sys.argv) == 1):
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
                


