import os
import socket
import subprocess
import sys

from utils.scanner import scan_ports, PORT
from utils.senderchecks import ssh_dir_check

if os.getuid() != 0:
    print('Run as sudo')
    sys.exit(0)


def send():
    hosts = scan_ports()
    print('-----HOSTS-----')
    for i, host in enumerate(hosts, start=1):
        print(str(i) + ': ' + str(host[0]) + '@' + host[1])
    while True:
        print('ft> ', end='')
        try:
            cmd = input()
        except (KeyboardInterrupt, EOFError):
            print('')
            sys.exit(0)

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
            sys.exit(0)

        else:
            print('Invalid command')


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
    a = "%s@%s wants to connect with you" % (str(os.path.expanduser('~').split('/')[-1]), str(s.getsockname()[0]))
    s.send(str.encode(a))
    try:
        response = str(s.recv(1024), encoding='utf-8')
        if response is None:
            raise Exception
    except:
        print("Receiver declined")
        return

    ssh_dir_check()
    subprocess.call(['ssh-keygen', '-t', 'rsa', '-q', '-f', os.path.expanduser('~/.ssh/temp_id'), '-N', ''])
    with open(os.path.expanduser('~/.ssh/temp_id.pub')) as f:
        public_key = f.read()

    try:
        s.send(str.encode(public_key))
        uname = str(s.recv(256), encoding='utf-8')
        if uname == 'root':
            subprocess.call(['rsync', '-aHAXxv', '--append-verify', '--progress', '-e',
                             'ssh -p %s -T -c arcfour -o Compression=no -o StrictHostKeyChecking=no -x -i %s' %
                             (str(PORT), os.path.expanduser('~/.ssh/temp_id')), file,
                             '%s@%s:/root/Downloads/' % (uname, str(host))])
        else:
            subprocess.call(['rsync', '-aHAXxv', '--append-verify', '--progress', '-e',
                             'ssh -p %s -T -c arcfour -o Compression=no -o StrictHostKeyChecking=no -x -i %s' %
                             (str(PORT), os.path.expanduser('~/.ssh/temp_id')), file,
                             '%s@%s:/home/%s/Downloads/' % (uname, str(host), uname)])
        s.send(str.encode("close"))
    except Exception as e:
        print("Error while sending file "+str(e))
    finally:
        os.remove(os.path.expanduser('~/.ssh/temp_id'))
        os.remove(os.path.expanduser('~/.ssh/temp_id.pub'))


if __name__ == '__main__':
    send()
