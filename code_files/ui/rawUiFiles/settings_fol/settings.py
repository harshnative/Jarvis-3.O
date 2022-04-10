# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setStyleSheet("background-color: rgb(18, 18, 18);")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 778, 471))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
#         self.verticalLayout_3 = QtWidgets.QVBoxLayout()
#         self.verticalLayout_3.setObjectName("verticalLayout_3")
#         self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
#         self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
# "font: 63 20pt \"FreeSans\";\n"
# "color: rgb(255, 255, 255);\n"
# "padding: 8px;\n"
# "margin: 8px;")
#         self.label.setObjectName("label")
#         self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignVCenter)
#         self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
#         self.lineEdit.setStyleSheet("background-color: rgb(85, 87, 83);\n"
# "font: 63 20pt \"FreeSans\";\n"
# "color: rgb(255, 255, 255);\n"
# "padding: 8px;\n"
# "margin: 8px;")
#         self.lineEdit.setObjectName("lineEdit")
#         self.verticalLayout_3.addWidget(self.lineEdit)
        # self.verticalLayout_2.addLayout(self.verticalLayout_3)
        # self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        # self.verticalLayout_4.setObjectName("verticalLayout_4")
        # self.verticalLayout_2.addLayout(self.verticalLayout_4)

        # add in veritical layout two
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setStyleSheet("background-color: rgb(1, 135, 134);\n"
"font: 81 20pt \"FreeSans\";\n"
"color: rgb(255, 255, 255);\n"
"padding: 16px;\n"
"margin: 16px;")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setStyleSheet("background-color: rgb(55, 0, 179);\n"
"font: 81 20pt \"FreeSans\";\n"
"color: rgb(255, 255, 255);\n"
"padding: 16px;\n"
"margin: 16px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout_5.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        # self.label.setText(_translate("Form", "TextLabel"))
        # self.lineEdit.setPlaceholderText(_translate("Form", "placeholder"))
        self.pushButton.setText(_translate("Form", "BACK"))
        self.pushButton_2.setText(_translate("Form", "SAVE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
