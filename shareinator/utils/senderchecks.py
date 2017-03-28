import os


def ssh_dir_check():
    if not os.path.exists(os.path.expanduser('~/.ssh')):
        os.makedirs(os.path.expanduser('~/.ssh'))
