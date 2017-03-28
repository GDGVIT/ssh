import os
from shutil import copyfile
import subprocess
import sys

FNULL = open(os.devnull, 'w')


def ssh_config():
    subprocess.call(['sudo', 'apt-get', 'install', 'openssh-server', '-y'], stdout=FNULL, stderr=subprocess.STDOUT)
    if not os.path.exists('/usr/sbin/sshd'):
        print('Could not install ssh server. Check your repositories.')
        sys.exit(0)
    copyfile('/etc/ssh/sshd_config', '/etc/ssh/sshd_config.factory-defaults')
    copyfile('/etc/ssh/sshd_config.factory-defaults', '/etc/ssh/shareinator')
    lines = [
        "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,"
        "aes256-gcm@openssh.com,arcfour,arcfour128,arcfour256,blowfish-cbc\n",
    ]
    with open('/etc/ssh/shareinator', 'a') as f:
        f.writelines(lines)
