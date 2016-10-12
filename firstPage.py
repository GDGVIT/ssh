import sys
from PyQt4 import QtGui, QtCore
from sendgui import Window

class Window1(QtGui.QMainWindow):

    def __init__(self):
        super(Window1, self).__init__()
        self.setGeometry(50,50,300,230)
        self.home1()

    def home1(self):
        senderBtn = QtGui.QPushButton("send", self)
        senderBtn.clicked.connect(self.Sender)
        senderBtn.resize(senderBtn.minimumSizeHint())
        senderBtn.move(100,40)

        receiverBtn = QtGui.QPushButton("Receive", self)
        #receiverBtn.clicked.connect(self.receive)
        receiverBtn.resize(receiverBtn.minimumSizeHint())
        receiverBtn.move(100,120)
        self.show()
    def Sender(self):
        self.window = Window()
        self.window.show()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window1()
    sys.exit(app.exec_())

run()
