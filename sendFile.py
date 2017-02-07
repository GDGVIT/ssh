from PyQt4.QtGui import *
from PyQt4.QtCore import *	
import sys

import sender2

class sendfile(QWidget,sender2.Ui_Form):
	def __init__(self, parent=None):
		super(sendfile, self).__init__(parent)
		self.setupUi(self)
'''
app = QApplication(sys.argv)
From = sendfile()
From.show()
app.exec_()'''