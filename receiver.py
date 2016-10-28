# coding=utf-8
import subprocess
import os
import signal
import socket
from SSHconfigure import configure_ssh

__author__ = 'Ujjwal'

host = ""
port = 9999
s = None
F_NULL = open(os.devnull, 'w')

try:
    __USER__ = os.environ.copy()['SUDO_USER']
    if __USER__ == 'root':
        __USER__ = '../root'

except KeyError:
    print('Run as root')
    exit(0)

# Functions


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


def receive_file():
    if 'sshd' not in str(subprocess.check_output(['ls', '/usr/sbin'])):
        configure_ssh()
    if 'arcfour' not in str(subprocess.check_output(['cat', '/etc/ssh/sshd_config'])):
        configure_ssh()

    ssh_server = subprocess.Popen(['sudo', '/usr/sbin/sshd', '-p', '2222', '-D'], preexec_fn=os.setsid)

    # Creates and binds the socket
    socket_create()
    socket_bind()

    # Waits for a connection
    print('Waiting...')
    try:
        conn, address = s.accept()
    except (KeyboardInterrupt, EOFError):
        # Kill sshd on KeyboardInterrupt or EOFError
        print('Keyboard Interrupt')
        os.killpg(os.getpgid(ssh_server.pid), signal.SIGTERM)
        return

    print(str(conn.recv(1024), encoding='utf-8'))

    # Confirmation
    confirmation = input("Do you want to accept the connection? ")
    if str(confirmation).lower() == "y":
        conn.send(str.encode("Yes"))
    else:
        conn.close()
        os.killpg(os.getpgid(ssh_server.pid), signal.SIGTERM)
        return

    # Get the public key
    public_key = str(conn.recv(2048), encoding='utf-8')

    # .ssh/authorized_keys already exists, make an empty backup file
    if (subprocess.call(['cp', "/home/{}/.ssh/authorized_keys".format(__USER__), "/home/{}/.ssh/authorized_keys_Backup".format(__USER__)],
                        stdout=F_NULL, stderr=subprocess.STDOUT)):

        subprocess.call(['touch', "/home/{}/.ssh/authorized_keys_Backup".format(__USER__)])

    # Add the received key to .ssh/authorized_keys
    with open('/home/' + __USER__ + '/.ssh/authorized_keys', 'a') as f:
        f.write(public_key)

    try:
        # Send the user name and close the socket
        conn.send(str.encode(__USER__.lstrip('../')))
        conn.recv(256)
        conn.close()

    except socket.error:
        # Abandon the connection
        try:
            conn.close()
        except socket.error:
            pass

        print('Error encountered')
    finally:
        # Remove the public key file and revert it back to previous state
        os.remove("/home/{}/.ssh/authorized_keys".format(__USER__))
        os.rename("/home/{}/.ssh/authorized_keys_Backup".format(__USER__), "/home/{}/.ssh/authorized_keys".format(__USER__))

        # Kill the sshd server
        os.killpg(os.getpgid(ssh_server.pid), signal.SIGTERM)


if __name__ == '__main__':
    receive_file()
