__author__ = 'Ujjwal'

import os
import subprocess
import socket
from scanner import scan_ports


__PORT__ = 2222
try:
    __USER__ = os.environ.copy()['SUDO_USER']
    if __USER__=='root':
        __USER__='../root'
except:
    print('Run as sudo')
    exit(0)


def send():
    hosts = scan_ports()
    while True:
        print('ft> ', end='')
        try:
            cmd = input()
        except:
            print('')
            exit(0)

        if cmd == 'list':
            print('-----HOSTS-----')
            for i, host in enumerate(hosts, start=1):
                print(str(i) + ': ' + str(host[0]) + '@' + host[1])

        elif 'select' in cmd:
            host = int(cmd.replace('select ', '')) - 1
            if host >= len(hosts) or host < 0:
                print('Invalid selection')
                continue
            else:
                transfer(hosts[host][1])

        elif cmd == 'refresh':
            hosts = scan_ports()

        elif cmd == 'quit':
            exit(0)

        else:
            print('You wrote ' + cmd + ' moron!')


def transfer(host):
    file = input('Enter file path: ')
    try:
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error " + str(msg))
        return
    try:
        s.connect((host, port))
    except socket.error as msg:
        print("socket connect error: " + str(msg) + "\n")
        return
    a = str(__USER__.strip('../')) + '@' + str(s.getsockname()[0]) + ' wants to connect with you'
    s.send(str.encode(a))
    try:
        response = str(s.recv(1024), encoding='utf-8')
        if response == '':
            raise Exception
    except:
        print("Receiver declined")
        return

    subprocess.call(['ssh-keygen', '-t', 'rsa', '-q', '-f', '/home/' + __USER__ + '/.ssh/temp_id', '-N', ''])
    public_key = subprocess.check_output(['cat', '/home/' + __USER__ + '/.ssh/temp_id.pub'])

    try:
        s.send(public_key)
        uname = str(s.recv(256), encoding='utf-8')
        subprocess.call(['scp', '-P', str(__PORT__), '-i', '/home/' + __USER__ + '/.ssh/temp_id', '-o', 'StrictHostKeyChecking=no', file,
                         uname + '@' + str(host) + ':/home/' + uname + '/Downloads/'])
        s.send(str.encode("close"))
        os.remove('/home/' + __USER__ + '/.ssh/temp_id')
        os.remove('/home/' + __USER__ + '/.ssh/temp_id.pub')
    except:
        os.remove('/home/' + __USER__ + '/.ssh/temp_id')
        os.remove('/home/' + __USER__ + '/.ssh/temp_id.pub')
        print("Error while sending file")


if __name__ == '__main__':
    send()
