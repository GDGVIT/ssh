from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

from utils.scanner import scan_ports, PORT
from utils.senderchecks import ssh_dir_check

import sender1
from sendFile import sendfile
#from mainGui import mainPage
from sender import send, transfer

class Window1(QWidget,sender1.Ui_Form):
	def __init__(self, parent=None):
		super(Window1, self).__init__(parent)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.refresh)
		#self.pushButton_2.clicked.connect()
		#self.pushButton_3.clicked.connect()
		self.listWidget.itemClicked.connect(self.recIP)
		self.pushButton_4.clicked.connect(self.Connect)
		self.scanSignal = SCAN()
		self.connect(self.scanSignal,SIGNAL("scanDone(PyQt_PyObject)"),self.UpdateList)
		self.IP = '0'
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
		if self.IP == '0':
			QMessageBox.Warning(self,"warning","select receiver ip")
		else:
			self.window = sendfile()
			self.window.show()		
	def recIP(self,ip):
		self.IP = ip.text()
class SCAN(QThread):
    def __init__(self, parent = None):
        super(SCAN, self).__init__(parent)
        #self.scanDone=QtCore.pyqtSignal()

    def run(self):
        self.HostsP = scan_ports()
        #print (type(HostsP))
        self.emit(SIGNAL("scanDone(PyQt_PyObject)"),self.HostsP)
        #self.scanDone.emit(Hs)