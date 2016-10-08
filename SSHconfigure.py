__author__ = 'Ujjwal'

import subprocess
import os

FNULL = open(os.devnull, 'w')

def sshConfig():
    subprocess.call(['sudo', 'apt-get', 'install', 'openssh-server', '-y'], stdout=FNULL, stderr=subprocess.STDOUT)
    subprocess.call(['sudo', 'cp', '/etc/ssh/sshd_config', '/etc/ssh/sshd_config.factory-defaults'], stdout=FNULL, stderr=subprocess.STDOUT)
    if(subprocess.call(['sudo', 'service', 'sshd', 'stop'],stdout=FNULL,stderr=subprocess.STDOUT)):
        print('Could not install ssh server. Check your repositories.' )
        exit(0)
    with open('/etc/ssh/sshd_config', 'a') as f:
        f.writelines("Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com,arcfour,arcfour128,arcfour256,blowfish-cbc")
