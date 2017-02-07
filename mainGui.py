from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import socket
import subprocess

import mainGUI
import sender1
import sender2
import sendingfile
import receiverUI

from utils.scanner import scan_ports, PORT
from utils.senderchecks import ssh_dir_check
from sender import transfer
from receiver import recvfile

#from chooseip import Window1
IP = 'local host'
File = '0'

class mainPage(QWidget,mainGUI.Ui_Form):
	def __init__(self, parent=None):
		super(mainPage, self).__init__(parent)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.Sender)
		self.pushButton_2.clicked.connect(self.Receive)
	def Sender(self):
		self.close()
		self.window1 = Window1()
		self.window1.show()

	def Receive(self):
		self.close()
		self.window2 = ReceiverUI()
		self.window2.show()

class Window1(QWidget,sender1.Ui_Form):
	def __init__(self, parent=None):
		super(Window1, self).__init__(parent)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.refresh)
		self.pushButton_2.clicked.connect(self.Close)
		self.pushButton_3.clicked.connect(self.back1)
		self.listWidget.itemClicked.connect(self.recIP)
		self.pushButton_4.clicked.connect(self.Connect)
		self.scanSignal = SCAN()
		self.connect(self.scanSignal,SIGNAL("scanDone(PyQt_PyObject)"),self.UpdateList)
	def refresh(self):
		self.listWidget.clear()
		self.scanSignal.start()
		QMessageBox.information(self,"refresh","scan started")
	def UpdateList(self,ite):
		self.listWidget.clear()
		QMessageBox.information(self,"completed","scan completed")
		Hs = ite
		print('ft')
		for i, host in enumerate(Hs, start=1):
			self.listWidget.addItem(str(host))
	def Connect(self):
		'''if self.IP == '0':
			QMessageBox.warning(self,"warning","select receiver ip")
		else:'''
		self.close()
		self.window = sendfile()
		self.window.show()		
	def recIP(self,ip):
		global IP
		IP = str(ip.text()).split('@')[-1]
	def back1(self):
			self.close()
			self.window = mainPage()
			self.window.show()
	def Close(self):
		sys.exit()			
class SCAN(QThread):
    def __init__(self, parent = None):
        super(SCAN, self).__init__(parent)
        #self.scanDone=QtCore.pyqtSignal()

    def run(self):
        self.HostsP = scan_ports()
        #print (type(HostsP))
        self.emit(SIGNAL("scanDone(PyQt_PyObject)"),self.HostsP)
        #self.scanDone.emit(Hs)


class sendfile(QWidget,sender2.Ui_Form):
	def __init__(self, parent=None):
		global IP, File
		super(sendfile, self).__init__(parent)
		self.setupUi(self)
		self.label_3.setText(IP)
		self.ip = self.label_3.text()
		self.pushButton.clicked.connect(self.Cancle)
		self.pushButton_2.clicked.connect(self.back)
		self.toolButton.clicked.connect(self.selfile)
		self.pushButton_3.clicked.connect(self.send)
	def Cancle(self):
		sys.exit()
	def back(self):
		self.close()
		self.window = Window1()
		self.window.show()
	def selfile(self):
		global File
		name = QFileDialog.getOpenFileName(self, 'Open File')
		self.lineEdit.setText(name)
		File = name
	def send(self):
		if not os.path.exists(os.path.expanduser(File)):
			QMessageBox.warning(self,"warning","file path not valid")
		else:
			#sender2.Ui_Form.setDisabled (True)
			self.window = sendingFile()
			self.window.show()


class sendingFile(QDialog,sendingfile.Ui_Dialog):
	def __init__(self, parent=None):
		super(sendingFile, self).__init__(parent)
		self.setupUi(self)
		self.progressBar.setRange(0,0)
		self.pushButton.setEnabled(False)
		self.pushButton.clicked.connect(self.Close)
		self.SEND = SThread()
		self.connect(self.SEND,SIGNAL("taskFinished"),self.onFinished)
		self.SEND.start

	def onFinished(self):
		self.progressBar.setRange(0,1)
		self.progressBar.setValue(1)
		self.pushButton.setEnabled(True)
		QMessageBox.information(self,"completed","File Sent")


	def Close(self):
		self.close()

class SThread(QThread):
	def __init__(self, parent = None):
		super(SThread, self).__init__(parent)
	def run(self):
		
		transfer(IP,File)
		self.emit(SIGNAL("taskFinished"))

class ReceiverUI(QWidget,receiverUI.Ui_Form):
	def __init__(self, parent=None):
		super(ReceiverUI, self).__init__(parent)
		self.setupUi(self)


app = QApplication(sys.argv)
From = mainPage()
From.show()
app.exec_()