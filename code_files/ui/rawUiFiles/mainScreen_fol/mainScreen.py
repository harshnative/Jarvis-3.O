# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setEnabled(True)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 128))
        self.pushButton.setStyleSheet("background-color: rgb(55, 0, 179);\n"
"color: rgb(238, 238, 236);\n"
"font: 85 24pt \"FreeSans\";\n"
"\n"
"\n"
"border-image: url(:/newPrefix/prev_button.svg);")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 128))
        self.pushButton_3.setStyleSheet("background-color: rgb(55, 0, 179);\n"
"color: rgb(238, 238, 236);\n"
"font: 85 24pt \"FreeSans\";\n"
"\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 128))
        self.pushButton_4.setStyleSheet("background-color: rgb(55, 0, 179);\n"
"color: rgb(238, 238, 236);\n"
"font: 85 24pt \"FreeSans\";\n"
"\n"
"")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 128))
        self.pushButton_5.setStyleSheet("background-color: rgb(55, 0, 179);\n"
"color: rgb(238, 238, 236);\n"
"font: 85 24pt \"FreeSans\";\n"
"\n"
"")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 128))
        self.pushButton_6.setStyleSheet("background-color: rgb(55, 0, 179);\n"
"color: rgb(238, 238, 236);\n"
"font: 85 24pt \"FreeSans\";\n"
"\n"
"")
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 128))
        self.pushButton_2.setStyleSheet("background-color: rgb(55, 0, 179);\n"
"color: rgb(238, 238, 236);\n"
"font: 85 24pt \"FreeSans\";\n"
"\n"
"\n"
"border-image: url(:/newPrefix/next_button.svg);")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "SAMPLE"))
        self.pushButton_4.setText(_translate("Form", "SAMPLE"))
        self.pushButton_5.setText(_translate("Form", "SAMPLE"))
        self.pushButton_6.setText(_translate("Form", "SAMPLE"))
        self.pushButton_6.styleSheet

        self.pushButton.setDisabled

from ..mainScreen_fol import mainScreen_resource


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
