# coding=utf-8
import socket
import threading
import ipaddress
import subprocess


__author__ = 'Ujjwal'

PORT = 2222
DELAY = 2


def tcp_connect(ip, port_number, delay, hosts):
    host_name = 'Unknown'

    # Create the socket
    tcp_socket = socket.socket()
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.settimeout(delay)

    # Connect
    try:
        host_name = socket.gethostbyaddr(ip)[0]

        tcp_socket.connect((ip, port_number))
        if 'SSH' in str(tcp_socket.recv(256)):
            hosts.append((host_name, ip))
    except socket.error:
        pass


def scan_ports():
    threads = []
    hosts = []

    network = str(subprocess.check_output(['ip', 'route']), encoding='utf-8').split('\n')[-2].split()[0]
    if '/' not in network:
        print('Could not determine gateway')
        return

    """
    gateway=str(subprocess.check_output(['route','-n']),encoding='utf-8')
    gateway=gateway.split('\n')
    mask=gateway[3].split()[1]+'/'+gateway[3].split()[2]
    gateway=gateway[3].split()[0]
    #print(gateway)
    #print(mask)
    prefix_len=ipaddress.IPv4Network(mask).prefixlen
    #print(prefix_len)
    """

    print("Scanning...")
    # Iterate though hosts (each one in a thread)
    for host_ip in ipaddress.IPv4Network(network):
        # Create a thread and add it to the list
        t = threading.Thread(target=tcp_connect, args=(str(host_ip), PORT, DELAY, hosts))
        threads.append(t)

        if len(threads) == 255:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads = []

    if threads:
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    return hosts


def main():
    print(scan_ports())


if __name__ == "__main__":
    main()
