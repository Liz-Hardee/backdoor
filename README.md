# Backdoor
A very simple backdoor program for practise.

## Modules
### Port Scanner
The port scanner module is currently the only module. The program takes options from the command line and either a single ip/hostname
or a list thereof. Multiple hosts/ips should be seperated by spaces. The program will check the address for open ports out of a list of
common port numbers.

### Syntax:

single scan by hostname:
python3 portscanner -i google.com

single scan by ip:
python3 portscanner -i 192.168.0.1

list scan by hostname:
python3 portscanner -l google.com yahoo.com youtube.com

list scan by ip
python3 portscanner -l 192.168.0.1 127.0.0.1
