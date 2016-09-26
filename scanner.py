__author__ = 'Ujjwal'

import socket
import threading

__PORT__ = 2222
__DELAY__ = 15
__NETWORKPREFIX__ = '172.16.'


def TCP_connect(ip, port_number, delay, hosts):
    host_name='Unknown'
    TCPsock = socket.socket()
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        host_name = socket.gethostbyaddr(ip)[0]
    except:
        pass
    try:
        TCPsock.connect((ip, port_number))
        if 'SSH' in str(TCPsock.recv(256)):
            hosts.append((host_name,ip))
    except:
        pass
def scan_ports():
    threads = []
    hosts = []

    print("Scanning...")
    for i in range(40, 44):
        for j in range(1, 256):
            host_ip = __NETWORKPREFIX__ + str(i) + '.' + str(j)
            t = threading.Thread(target=TCP_connect, args=(host_ip, __PORT__, __DELAY__, hosts))
            threads.append(t)


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
