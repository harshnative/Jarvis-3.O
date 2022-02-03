
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
from ui import m_mainScreen

def handler(msg_type, msg_log_context, msg_string):
    pass

QtCore.qInstallMessageHandler(handler)

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = m_mainScreen.mainScreenWidget()
ui.setupUi(Form)
Form.show()
rc = app.exec_()

del app
del ui
del Form

sys.exit( rc )



