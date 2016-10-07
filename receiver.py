__author__ = 'Ujjwal'

import subprocess
import os
import signal
import socket
from SSHconfigure import sshConfig


try:
    __USER__ = os.environ.copy()['SUDO_USER']
    if __USER__=='root':
        __USER__='../root'
except:
    print('Run as sudo')
    exit(0)
FNULL = open(os.devnull, 'w')


def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error:
        print("Socket creation error")


def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
    except socket.error:
        print("Socket binding error")
        exit(0)


def recvfile():
    if ('sshd' not in str(subprocess.check_output(['ls', '/usr/sbin']))):
        sshConfig()
    sshServ = subprocess.Popen(['sudo', '/usr/sbin/sshd', '-p', '2222', '-D'], preexec_fn=os.setsid)
    socket_create()
    socket_bind()
    print('Waiting...')
    try:
        conn, address = s.accept()
    except (KeyboardInterrupt,EOFError):
        print('Keyboard Interrupt')
        return
    print(str(conn.recv(1024), encoding='utf-8'))
    confirmation = input("Do you want to accept the connection? ")
    if confirmation == 'y' or confirmation == 'Y':
        conn.send(str.encode("Yes"))
    else:
        conn.close()
        os.killpg(os.getpgid(sshServ.pid), signal.SIGTERM)
        return
    public_key = str(conn.recv(2048), encoding='utf-8')

    if (subprocess.call(['cp', '/home/' + __USER__ + '/.ssh/authorized_keys', '/home/' + __USER__ + '/.ssh/authorized_keys_Backup'], stdout=FNULL,
                        stderr=subprocess.STDOUT)):
        subprocess.call(['touch', '/home/' + __USER__ + '/.ssh/authorized_keys_Backup'])

    with open('/home/' + __USER__ + '/.ssh/authorized_keys', 'a') as f:
        f.write(public_key)
    try:
        conn.send(str.encode(__USER__.lstrip('../')))
        conn.recv(256)
        conn.close()
        os.remove('/home/' + __USER__ + '/.ssh/authorized_keys')
        os.rename('/home/' + __USER__ + '/.ssh/authorized_keys_Backup', '/home/' + __USER__ + '/.ssh/authorized_keys')
        os.killpg(os.getpgid(sshServ.pid), signal.SIGTERM)
    except:
        try:
            conn.close()
        except:
            pass
        os.remove('/home/' + __USER__ + '/.ssh/authorized_keys')
        os.rename('/home/' + __USER__ + '/.ssh/authorized_keys_Backup', '/home/' + __USER__ + '/.ssh/authorized_keys')
        os.killpg(os.getpgid(sshServ.pid), signal.SIGTERM)
        print('Error encountered')


if __name__ == '__main__':
    recvfile()
