import sys
import socket
import datetime
import dns.reversename, dns.resolver
import re
import configparser
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

def check_writefile():
    for index, option in enumerate(sys.argv):
        if option == '-o':
            if not re.search('-.*', sys.argv[index + 1]):
                return sys.argv[index + 1]
    with open('backdoor.config', 'r') as cfile:
        config = configparser.ConfigParser()
        config.read_file(cfile)
    return config.get('portscanner', 'outfile')

def check_timeout():
    for index, option in enumerate(sys.argv):
        if option == '-t':
            if not re.search('-.*', sys.argv[index +1]):
                return sys.argv[index + 1]
    with open('backdoor.config', 'r') as cfile:
        config = configparser.ConfigParser()
        config.read_file(cfile)
    return config.get('portscanner', 'timeout')

def write_ports(banners, ipaddress, dnsname, portlist):
    outfile = check_writefile()
    if exists(outfile):
        access = 'a'
    else:
        access = 'w'
    with open(outfile, access) as wfile:
        wfile.writelines(['Hostname: ' + dnsname + '\n', 
                         'IP: ' + str(ipaddress) + '\n', 
                         'Date Scanned: ' + str(datetime.datetime.now()) + 
                         '\n', 'Open Ports: '])
        if len(portlist) == 0:
            wfile.write('None')
        for index, port in enumerate(portlist):
            wfile.write('\n' + str(port) + ': ' + banners[index])
        wfile.write('\n\n')
        wfile.close()

def get_banner(s):
    return s.recv(1024)

def scan_port(ipaddress):
    openports = []
    banners = []
    converted_ip = check_ip(ipaddress)
    converted_dns = get_dns(converted_ip)
    if '-v' in sys.argv:
        print('\nHostname: ' + converted_dns)
        print('\nIP: ' + str(converted_ip))
    for port in (20, 21, 22, 23, 25, 53, 80, 110, 119,
                 123, 143, 161, 194, 443, 32400):
        if '-v' in sys.argv:
            print('Scanning port ' + str(port) + '...')
        try:
            sock = socket.socket()
            sock.settimeout(float(check_timeout()))
            sock.connect((ipaddress, port))
            try:
                banner = str(get_banner(sock))
            except:
                banner = "no banner found"
            openports.append(port)
            if '-v' in sys.argv:
                print('Port ' + str(port) + ' is open')
                print(banner)
            banners.append(banner)
        except:
            pass
    if '-o' in sys.argv:
        try:
            write_ports(banners, converted_ip, converted_dns, openports)
            if '-v' in sys.argv:
                print('File sucessfully written\n')
        except:
            print('Error: Unable to write file\n')

def main_switch():
    for index, option in enumerate(sys.argv):
        if option == '-h' or option == '--help' or len(sys.argv) == 1:
            option_list()
            exit()
        elif option == '-i' or option =='--ipaddress':
            try: 
                scan_port(sys.argv[index + 1])
            except:
                print('Please enter a valid IP or hostname\n')
            exit()
        elif option == '-l' or option == '--list':
            try:
                rfile = open(sys.argv[index + 1])
                iplist = map(str.strip, rfile.readlines())
                for ip in iplist:
                    scan_port(ip)
            except FileNotFoundError:
                ip_iter = index
                while ip_iter < len(sys.argv) - 1:
                    ip_iter += 1
                    scan_port(sys.argv[ip_iter])
            exit()

if __name__ == '__main__':
    main_switch()