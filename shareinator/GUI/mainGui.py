from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import os

from shareinator.GUI import sender1
from shareinator.GUI import sender2
from shareinator.GUI import sendingfile
from shareinator.GUI import mainPAGE
from shareinator.GUI import receivingFile1

from shareinator.utils.scanner import scan_ports
from shareinator.GUI.sender import transfer
from shareinator.GUI.receiver import recvfile, econn

IP = '0'
File = '0'


class mainPage(QWidget, mainPAGE.Ui_Form):
    def __init__(self, parent=None):
        super(mainPage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Shareinator")
        self.setFixedSize(240,300)
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


class Window1(QWidget, sender1.Ui_Form):
    def __init__(self, parent=None):
        super(Window1, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Select receiver IP")
        self.setFixedSize(400,344)
        self.pushButton.clicked.connect(self.refresh)
        self.pushButton_2.clicked.connect(self.Close)
        self.pushButton_3.clicked.connect(self.back1)
        self.listWidget.itemClicked.connect(self.recIP)
        self.pushButton_4.clicked.connect(self.Connect)
        self.scanSignal = SCAN()
        # self.connect(self.scanSignal,SIGNAL("scanDone(PyQt_PyObject)"),self.UpdateList)
        self.scanSignal.scanDone.connect(self.UpdateList)

    def refresh(self):
        self.listWidget.clear()
        self.scanSignal.start()
        QMessageBox.information(self, "refresh", "scan started")

    def UpdateList(self, ite):
        self.listWidget.clear()
        QMessageBox.information(self, "completed", "scan completed")
        Hs = ite
        print('ft')
        for i, host in enumerate(Hs, start=1):
            self.listWidget.addItem(str(host))

    def Connect(self):
        global IP
        if IP == '0':
            QMessageBox.warning(self, "warning", "select receiver ip")
        else:
            self.close()
            self.window = sendfile()
            self.window.show()

    def recIP(self, ip):
        global IP
        print(str(ip.text()))
        op = str(ip.text()).split("'")
        IP = op[-2]
        print(IP)

    def back1(self):
        self.close()
        self.window = mainPage()
        self.window.show()

    def Close(self):
        sys.exit()


class SCAN(QThread):
    scanDone = pyqtSignal([list])

    def __init__(self, parent=None):
        super(SCAN, self).__init__(parent)

    def run(self):
        self.HostsP = scan_ports()
        # print (type(HostsP))

        self.scanDone.emit(self.HostsP)
        # self.scanDone.emit(Hs)


class sendfile(QWidget, sender2.Ui_Form):
    def __init__(self, parent=None):
        global IP, File
        super(sendfile, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Select File")
        self.setFixedSize(393,217)
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
        print(name)
        self.lineEdit.setText(name[0])
        File = name[0]

    def send(self):
        if not os.path.exists(os.path.expanduser(File)):
            QMessageBox.warning(self, "warning", "file path not valid")
        else:
            # sender2.Ui_Form.setDisabled (True)
            self.window = sendingFile()
            self.window.show()
            # self.window.SEND.start


class sendingFile(QDialog, sendingfile.Ui_Dialog):
    def __init__(self, parent=None):
        super(sendingFile, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Sending File")
        self.setFixedSize(393,217)
        self.progressBar.setRange(0, 0)
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.Close)
        self.SEND = SThread()
        # self.connect(self.SEND,SIGNAL("taskFinished"),self.onFinished)
        self.SEND.taskFinished.connect(self.onFinished)
        self.SEND.start()

    def onFinished(self):
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(1)
        self.pushButton.setEnabled(True)
        QMessageBox.information(self, "completed", "File Sent")

    def Close(self):
        self.close()


class SThread(QThread):
    taskFinished = pyqtSignal()

    def __init__(self, parent=None):
        super(SThread, self).__init__(parent)

    def run(self):
        global IP, File
        print(IP)
        print(File)
        transfer(IP, File)
        self.taskFinished.emit()


class ReceiverUI(QDialog, receivingFile1.Ui_Dialog):
    def __init__(self, parent=None):
        super(ReceiverUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Waiting For Sender")
        self.setFixedSize(393,217)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.cancle)
        self.pushButton_2.setEnabled(False)
        self.progressBar.setRange(5, 0)
        self.recvcon = RECV()
        # self.connect(self.recvcon,SIGNAL("request(PyQt_PyObject)"),self.accept)
        self.recvcon.request.connect(self.accept)
        self.recvcon.start()
        self.recvf = RECVF()
        # self.connect(self.recvf,SIGNAL("recvF"),self.onFinished)
        self.recvf.recvF.connect(self.onFinished)

    def accept(self, con):
        if (con):
            message = str(con) + " want to connect"
            reply = QMessageBox.question(self, "Connection Request", message, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.recvf.start()
                self.pushButton_2.setEnabled(True)
                self.setWindowTitle("Receiving File")
                self.label.setText = ("Receiving File")
            else:
                recvfile('n')
        else:
            QMessageBox.warning(self, "warning", "something went wrong")

    def onFinished(self):
        self.progressBar.setRange(0, 1)
        self.progressBar.setValue(1)
        QMessageBox.information(self, "completed", "File Received")
        reply = QMessageBox.question(self, "Continue", "Do You Want To Continue?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.label.setText = ("Waiting For Connection")
            self.setWindowTitle("Waiting For Sender")
        else:
            sys.exit()

    def close(self):
        sys.exit()

    def cancle(self):
        reply = QMessageBox.question(self, "Cancel", "Do You Want To cancel?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.No:
            self.recvf.exit()


class RECV(QThread):
    request = pyqtSignal([str])

    def __init__(self, parent=None):
        super(RECV, self).__init__(parent)

    def run(self):
        self.conn = econn()
        self.request.emit(self.conn)


class RECVF(QThread):
    recvF = pyqtSignal()

    def __init__(self, parent=None):
        super(RECVF, self).__init__(parent)

    def run(self):
        recvfile("y")
        self.recvF.emit()

def main():
    app = QApplication(sys.argv)
    From = mainPage()
    From.show()
    app.exec_()
