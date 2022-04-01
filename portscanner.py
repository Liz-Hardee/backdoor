import sys
import socket
import datetime
import dns.reversename, dns.resolver
import re
from IPy import IP
from os.path import exists

def option_list():
    print('\n\n                       --OPTIONS--\n')
    print('-i, --ipaddress......provide target ip from command line\n')
    print('-l, --list........provide a list or .csv of IPs or hosts\n')
    print('-o...........................write scan  results to file\n')
    print('-v.........................print scan results to termial\n')
    print('-h, --help..............................prints this menu\n\n')

def check_ip(ipaddress):
    try:
        IP(ipaddress)
        return(ipaddress)
    except ValueError:
        try:
            return socket.gethostbyname(ipaddress)
        except:
            print('Invalid target/s. Check target/s for syntax errors.')

def get_dns(ipaddress):
    try:
        address = dns.reversename.from_address(str(ipaddress))
        return (str(dns.resolver.resolve(address, 'PTR')[0]))
    except:
        if re.search('.*\..*\..*\..*', str(ipaddress)):
            return 'none'
        else:
            return 'Invalid Host'

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
        if len(portlist) == 0:
            wfile.write('None')
        for port in portlist:
            wfile.write(str(port) + ', ')
        wfile.write('\n\n')
        wfile.close()

def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.1)
        sock.connect((ipaddress, port))
        if '-v' in sys.argv:
            print('Port ' + str(port) + ' is open')
            return port
    except:
        if '-v' in sys.argv:
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

def main_switch():
    for index, option in enumerate(sys.argv):
        if option == '-h' or option == '--help' or len(sys.argv) == 1:
            option_list()
            exit()
        elif option == '-i' or option =='--ipaddress':
            try: 
                try_ports(sys.argv[index + 1])
            except:
                print('Please enter a valid IP or hostname\n')
            exit()
        elif option == '-l' or option == '--list':
            try:
                rfile = open(sys.argv[index + 1])
                iplist = map(str.strip, rfile.readlines())
                for ip in iplist:
                    try_ports(ip)
            except FileNotFoundError:
                ip_iter = index
                while ip_iter < len(sys.argv) - 1:
                    ip_iter += 1
                    try_ports(sys.argv[ip_iter])
            exit()

main_switch()