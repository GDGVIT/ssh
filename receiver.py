import os
import subprocess
import signal
import socket
import sys

from utils.receiverchecks import ssh_server_check, ssh_dir_check

if os.getuid() != 0:
    print('Run as sudo')
    sys.exit(0)
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
    ssh_server_check()
    ssh_server = subprocess.Popen(['sudo', '/usr/sbin/sshd', '-p', '2222', '-f', '/etc/ssh/fireshare', '-D'],
                                  preexec_fn=os.setsid)
    socket_create()
    socket_bind()
    print('Waiting...')
    try:
        conn, address = s.accept()
    except (KeyboardInterrupt, EOFError):
        print(' Keyboard Interrupt')
        os.killpg(os.getpgid(ssh_server.pid), signal.SIGTERM)
        return
    print(str(conn.recv(1024), encoding='utf-8'))
    confirmation = input("Do you want to accept the connection? ")
    if confirmation.lower() == 'y':
        conn.send(str.encode("Yes"))
    else:
        conn.close()
        os.killpg(os.getpgid(ssh_server.pid), signal.SIGTERM)
        return
    public_key = str(conn.recv(2048), encoding='utf-8')

    ssh_dir_check()

    with open(os.path.expanduser('~/.ssh/authorized_keys'), 'a') as f:
        f.write(public_key)
    try:
        conn.send(str.encode(os.path.expanduser('~').split('/')[-1]))
        conn.recv(256)
        conn.close()
    except:
        print('Error encountered')
        try:
            conn.close()
        except:
            pass
    finally:
        os.remove(os.path.expanduser('~/.ssh/authorized_keys'))
        os.rename(os.path.expanduser('~/.ssh/authorized_keys_backup'), os.path.expanduser('~/.ssh/authorized_keys'))
        os.killpg(os.getpgid(ssh_server.pid), signal.SIGTERM)


if __name__ == '__main__':
    recvfile()
