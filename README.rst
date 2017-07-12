Shareinator
^^^^^^^^^^^  

Shareinator is a tool to easily transfer files over a network using ssh.

It uses ``openssh-server`` and ``rsync``. It currently requires root privileges 

Installation
------------
``$ pip3 install shareinator``

Usage
-----
``$ sudo -E ~/.local/bin/shareinator`` - This opens a GUI for shareinator. Click on Receive to receive a file or Send to send one.

You can also use CLI to send or receive files. 

``$ sudo -E ~/.local/bin/shareinator -r`` - This is used to receive a file. It will ask for confirmation when someone tries to send a file.

``$ sudo -E ~/.local/bin/shareinator -s -f FILEPATH`` -
To send a file. First it scans the network and gives a list of hostnames with their IP addresses. You have few options here.

Options:

+ list - Lists out all the online hosts
+ select NUMBER - Select the host to which the file is to transferred
+ refresh - Scan again for hosts
+ quit - Exit the program

Development Setup
-----------------
.. code-block::

  git clone https://github.com/GDGVIT/ssh.git
  cd ssh
  ./setup.sh
  source venv/bin/activate
