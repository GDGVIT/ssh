import os
from shutil import copyfile

from shareinator.utils.SSHconfigure import ssh_config


def ssh_server_check():
    if not os.path.exists('/usr/sbin/sshd'):
        ssh_config()
    elif not os.path.exists('/etc/ssh/shareinator'):
        ssh_config()
    elif 'arcfour' not in open('/etc/ssh/shareinator').read():
        ssh_config()


def ssh_dir_check():
    if not os.path.exists(os.path.expanduser('~/.ssh')):
        os.makedirs(os.path.expanduser('~/.ssh'))
    try:
        copyfile(os.path.expanduser('~/.ssh/authorized_keys'), os.path.expanduser('~/.ssh/authorized_keys_backup'))
    except FileNotFoundError:
        open(os.path.expanduser('~/.ssh/authorized_keys_backup'), 'w').close()
