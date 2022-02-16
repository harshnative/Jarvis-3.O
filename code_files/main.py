import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.m_passwordManager import PasswordMainWidget as test
from ui.packages.log_module.logger import Logger

def handler(msg_type, msg_log_context, msg_string):
    pass

QtCore.qInstallMessageHandler(handler)
QtWidgets.QApplication.setStyle("fusion")
app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
ui = test("./test.db" , Logger("testLogs.log"))
ui.setupUi(Form)
Form.show()
rc = app.exec_()

print("DONE")

del app
del ui
del Form

sys.exit( rc )



