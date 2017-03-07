from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(240, 300)
        Form.setMaximumSize(QtCore.QSize(240, 300))
        Form.setStyleSheet("QPushButton {\n"
                           "  background: #3D4C53;\n"
                           "  width : 200px;\n"
                           "  height : 50px;\n"
                           "  overflow: hidden;\n"
                           "  text-align : center;\n"
                           "  border-radius: 10px;\n"
                           "  box-shadow: 0px 1px 2px rgba(0,0,0,.2);\n"
                           "color:white;\n"
                           "}")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 240, 300))
        self.frame.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.frame.setStyleSheet(
            "QWidget#frame_2{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.0135747, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "}\n"
            "QWidget#frame{\n"
            "    background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:0, stop:0 rgba(253, 165, 82, 254), stop:1 rgba(255, 255, 255, 255));\n"
            "}\n"
            "QPushButton {\n"
            "  background: #3D4C53;\n"
            "  width : 200px;\n"
            "  height : 50px;\n"
            "  overflow: hidden;\n"
            "  text-align : center;\n"
            "  border-radius: 10px;\n"
            "  box-shadow: 0px 1px 2px rgba(0,0,0,.2);\n"
            "color:white;\n"
            "}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 25, 221, 41))
        font = QtGui.QFont()
        font.setFamily("Tibetan Machine Uni")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(False)
        self.label_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.label_2.setStyleSheet("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(20, 100, 200, 140))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(40, 20, 110, 40))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 80, 111, 41))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setMouseTracking(True)
        self.pushButton_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_2.setAcceptDrops(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Welcome To File Transfer"))
        self.pushButton.setText(_translate("Form", "Send"))
        self.pushButton_2.setText(_translate("Form", "Receive"))
