__author__ = 'Ujjwal'

import subprocess
import os

FNULL = open(os.devnull, 'w')

def sshConfig():
    subprocess.call(['sudo', 'apt-get', 'install', 'openssh-server', '-y'],stdout=FNULL,stderr=subprocess.STDOUT)
    subprocess.call(['sudo', 'cp', '/etc/ssh/sshd_config', '/etc/ssh/sshd_config.factory-defaults'],stdout=FNULL,stderr=subprocess.STDOUT)
    subprocess.call(['sudo', 'service', 'sshd', 'stop'],stdout=FNULL,stderr=subprocess.STDOUT)
