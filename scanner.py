__author__ = 'Ujjwal'

import socket
import threading
import ipaddress
import subprocess

__PORT__ = 2222
__DELAY__ = 2


def TCP_connect(ip, port_number, delay, hosts):
    host_name='Unknown'
    TCPsock = socket.socket()
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        host_name = socket.gethostbyaddr(ip)[0]
        #print(host_name)
    except:
        pass
    try:
        TCPsock.connect((ip, port_number))
        if 'SSH' in str(TCPsock.recv(256)):
            hosts.append((host_name,ip))
        #print(host_name,ip)
    except:
        pass


def scan_ports():
    threads = []
    hosts = []

    gateway=str(subprocess.check_output(['route','-n']),encoding='utf-8')
    gateway=gateway.split('\n')
    mask=gateway[3].split()[1]+'/'+gateway[3].split()[2]
    gateway=gateway[3].split()[0]
    #print(gateway)
    #print(mask)
    prefix_len=ipaddress.IPv4Network(mask).prefixlen
    #print(prefix_len)
    print("Scanning...")
    for host_ip in ipaddress.IPv4Network(str(gateway)+'/'+str(prefix_len)):
        #print(host_ip)
        t = threading.Thread(target=TCP_connect, args=(str(host_ip), __PORT__, __DELAY__, hosts))
        threads.append(t)
        if len(threads)== 255:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads=[]
    if(threads !=[]):
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    #for host in hosts:
    #    print(host)
    return hosts


def main():
    scan_ports()


if __name__ == "__main__":
    main()
