# coding=utf-8
import os
import subprocess
import socket
from scanner import scan_ports, PORT

__author__ = 'Ujjwal'

try:
    __USER__ = os.environ.copy()['SUDO_USER']
    if __USER__ == 'root':
        __USER__ = '../root'

except KeyError:
    print('Run as root')
    exit(0)


def send():
    hosts = scan_ports()

    # Infinitely
    while True:
        print('ft> ', end='')

        try:
            cmd = input()
        except EOFError:
            exit(0)

        if cmd == 'list':
            # List all hosts on the network
            print('-----HOSTS-----')
            for i, host in enumerate(hosts, start=1):
                print("{}: {}@{}".format(i, host[0], host[1]))

        elif 'select' in cmd:
            host = int(cmd.replace('select ', '')) - 1

            if host >= len(hosts) or host < 0:
                print('Invalid selection')
                continue
            else:
                transfer(hosts[host][1])

        elif cmd == 'refresh':
            # Refresh available hosts
            hosts = scan_ports()

        elif cmd == 'quit':
            # Exit the program
            exit(0)

        else:
            print('Invalid command')


def transfer(host):
    file = input('Enter file path: ')

    # Try creating a socket
    try:
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error {}".format(msg))
        return

    # Try connecting with the created socket
    try:
        s.connect((host, port))
    except socket.error as msg:
        print("Socket connect error: {}\n".format(msg))
        return

    a = "{}@{} wants to connect with you".format(__USER__.lstrip("../"), s.getsockname()[0])
    s.send(a.encode())


    try:
        response = str(s.recv(1024), encoding='utf-8')
        if not response:
            raise socket.error

    except socket.error:
        print("Receiver declined")
        return

    # Create the public key
    subprocess.call(['ssh-keygen', '-t', 'rsa', '-q', '-f', '/home/' + __USER__ + '/.ssh/temp_id', '-N', ''])
    public_key = subprocess.check_output(['cat', '/home/' + __USER__ + '/.ssh/temp_id.pub'])

    try:
        # Send the public key
        s.send(public_key)

        username = str(s.recv(256), encoding='utf-8')

        # Send the file to the appropriate directory
        if username == 'root':
            subprocess.call(['rsync', '-aHAXxv', '--append-verify', '--progress', '-e',
                            'ssh -p {} -T -c arcfour -o Compression=no -o StrictHostKeyChecking=no -x -i /home/{}/.ssh/temp_id'.format(PORT, __USER__),
                             file, "{}@{}:/root/Downloads/".format(username, host)])
        else:
            subprocess.call(['rsync', '-aHAXxv', '--append-verify', '--progress', '-e',
                            'ssh -p {} -T -c arcfour -o Compression=no -o StrictHostKeyChecking=no -x -i /home/{}/.ssh/temp_id'.format(PORT, __USER__),
                             file, username + '@' + str(host) + ':/home/' + username + '/Downloads/'])

        # Close the socket
        s.send("close".encode())

    except socket.error:
        print("Error while sending file")

    finally:
        # Remove the temporary public key file
        os.remove('/home/' + __USER__ + '/.ssh/temp_id')
        os.remove('/home/' + __USER__ + '/.ssh/temp_id.pub')

if __name__ == '__main__':
    send()
