# ssh
###A file transfer script

ssh is a Python sender and receiver for the ssh protocol.

This project requires `openssh-server` to be installed on the machine. You must also be able to access `sshd` and `ssh`.

---

##1. Sender
(sender.py)  
Options:  
* "list" - displays available hosts  
* "select" - used to select the target and transfer the file(s)  
* "refresh" - refreshes the host list  
* "quit" - quits  
  
---  
  
##2. Receiver  
(receiver.py)  
Required to receive the file. Upon attempted connection, you will be asked to approve/decline that connection.  
If transfer is successful, files will be copied to **/root/Downloads** (if root) or **/home/USERNAME/Downloads** .  
