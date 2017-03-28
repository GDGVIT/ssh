import socket
import threading
import ipaddress
import subprocess

PORT = 2222
DELAY = 2


def TCP_connect(ip, port_number, delay, hosts):
    host_name = 'Unknown'
    TCPsock = socket.socket()
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        host_name = socket.gethostbyaddr(ip)[0]
        # print(host_name)
    except socket.herror:
        pass
    try:
        TCPsock.connect((ip, port_number))
        if 'SSH' in str(TCPsock.recv(256)):
            hosts.append((host_name, ip))
            # print(host_name,ip)
    except (OSError, ConnectionRefusedError):
        pass


def scan_ports():
    threads = []
    hosts = []

    network = str(subprocess.check_output(['ip', 'route']), encoding='utf-8').split('\n')[-2].split()[0]
    if '/' not in network:
        print('Could not determine gateway')
        return

    print("Scanning...")
    for host_ip in ipaddress.IPv4Network(network):
        # print(host_ip)
        t = threading.Thread(target=TCP_connect, args=(str(host_ip), PORT, DELAY, hosts))
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
    # for host in hosts:
    #    print(host)
    return hosts


def main():
    print(scan_ports())


if __name__ == "__main__":
    main()
