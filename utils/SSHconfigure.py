import subprocess
import os

FNULL = open(os.devnull, 'w')


def ssh_config():
    subprocess.call(['sudo', 'apt-get', 'install', 'openssh-server', '-y'], stdout=FNULL, stderr=subprocess.STDOUT)
    subprocess.call(['sudo', 'cp', '/etc/ssh/sshd_config', '/etc/ssh/sshd_config.factory-defaults'], stdout=FNULL,
                    stderr=subprocess.STDOUT)
    if subprocess.call(['sudo', 'service', 'sshd', 'stop'], stdout=FNULL, stderr=subprocess.STDOUT):
        print('Could not install ssh server. Check your repositories.')
        exit(0)
    subprocess.call(['sudo', 'cp', '/etc/ssh/fireshare', '/etc/ssh/sshd_config.factory-defaults'], stdout=FNULL,
                    stderr=subprocess.STDOUT)
    lines = [
        "Ciphers 3des-cbc,aes128-cbc,aes192-cbc,aes256-cbc,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,"
        "aes256-gcm@openssh.com,arcfour,arcfour128,arcfour256,blowfish-cbc\n",
    ]
    with open('/etc/ssh/fireshare', 'a') as f:
        f.writelines(lines)
