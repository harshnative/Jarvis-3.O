from .rawUiFiles.ftpServer_fol import ftpServer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalDicts
import pathlib
import pyperclip
import socket


# importing FTP module
from pyftpdlib.log import config_logging
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import errno
from contextlib import closing

class GlobalData:

    buttonValues = {}
    original_button_styleSheet = {}








# function to get the path from the relative path of file
# required when file is bundled with pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
















# function to clear all widgets in a layout
def clearLayout(layout):
    if(layout != None):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                    child.widget().deleteLater()




# function to clear a layout which contains layouts
def clearLayout2(layout):
    layout_item_list = []

    for i in range(layout.count()):
        layout_item = layout.itemAt(i)
        layout_item_list.append(layout_item)

    layout_item_list.reverse()

    for i in layout_item_list:
        clearLayout(i)
        layout.removeItem(i)
    










class NMethods:

    @classmethod
    def get_ip_address(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip




    @classmethod
    def getPort(cls , port):

        # checking if the port number passed is free or not
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # checking if port binds
        try:
            s.bind((cls.get_ip_address() , port))

        # if port does not bind it means that port is not free
        except socket.error as e:
            if(e.errno == errno.EADDRINUSE):

                try:
                    # you don't care just listen to that port
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((cls.get_ip_address() , port))
                except Exception as e:

                    # finding free port by assign port = 0 then system will auto bind the port
                    with closing(s) as s:
                        s.bind(('', 0))
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        
                        # assign the port to object
                        port = s.getsockname()[1]
                        
            s.close()

        return port
















# class containing main password screen ui
class FTPServerMainWidget(QtWidgets.QWidget , ftpServer.Ui_Form):

    # call the init
    def __init__(self , loggerObj , port , username , password , default_folder , anonymous , parent=None):
        
        # calling the parent init
        super(FTPServerMainWidget, self).__init__(parent)

        # setup logger obj
        self.loggerObj_store = loggerObj
        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        self.var_port = port
        self.var_username = username
        self.var_password = password
        self.var_default_folder = default_folder
        self.var_anonymous = anonymous

        self.loggerObj.debug("finished object init")
        self.print_log()














    # function to setup ui
    def setupUi(self, Form):

        # calling the parent setupUi
        super().setupUi(Form)

        # form close button
        self.close_button = Form.close

        Form.setWindowTitle("Jarvis Ftp Server")

        self.loggerObj.debug("finished parent ui setup")
        self.print_log()

        # remove anon button
        self.anonymous_label.hide()
        self.anonymous_enable_button.hide()
        clearLayout(self.horizontalLayout_8)

        # set current window index to 0
        self.stackedWidget.setCurrentIndex(0)


        # default button
        self.default_button.clicked.connect(lambda : self.default_button_clicked(self.default_button))
        













    # function to define when default button is pressed
    def default_button_clicked(self , buttonObj):

        if(self.var_default_folder == ""):
            self.showDefaultFolderNotSetDialog()
            return

        self.animate_button_press(buttonObj)

        self.stackedWidget.setCurrentIndex(1)

        self.start_ftp_server()
        
            



    def start_ftp_server(self , folder = None):

        # set value in labels
        self.ip_value_label.setText(NMethods.get_ip_address())
        self.port_value_label.setText(str(NMethods.getPort(int(self.var_port))))
        self.ip_port_value_label.setText("ftp://" + self.ip_value_label.text() + ":" + self.port_value_label.text())
        self.username_value_label.setText(self.var_username)
        self.password_value_label.setText(self.var_password)

        if(folder == None):
            self.folder_shared_value_text_browser.setText(str(self.var_default_folder))
            folder = self.var_default_folder

        else:
            self.folder_shared_value_text_browser.setText(str(folder))

        
        



    # function to animate the button press
    def animate_button_press(self , buttonObj , new_text = None , timeAnimation = 0.05):

        self.loggerObj.debug("animate button clicked")
        self.print_log()

        original_style_sheet = buttonObj.styleSheet()

        original_style_sheetList = original_style_sheet.split("\n")

        new_style_sheetList = []

        for i in original_style_sheetList:
            i = str(i)
            if(i.find("background-color") != -1):
                new_style_sheetList.append("background-color: rgb(3, 218, 198);\n")
            else:
                new_style_sheetList.append(i)

        
        buttonObj.setStyleSheet("".join(new_style_sheetList))

        if(new_text != None):
            originalText = buttonObj.text()
            buttonObj.setText(new_text)


        QtCore.QCoreApplication.processEvents()

        time.sleep(timeAnimation)

        buttonObj.setStyleSheet(original_style_sheet)

        if(new_text != None):
            buttonObj.setText(originalText)




    
    # function to show a message pop warning that the passwords does not match
    def showDefaultFolderNotSetDialog(self):
        self.loggerObj.debug("showDefaultFolderNotSetDialog invoked")
        self.print_log()

        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle("Jarvis Info")

        msg.setText("Default folder not set. You can set a default folder in settings.")


        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)



        runMsg = msg.exec_()

        self.loggerObj.debug("showDefaultFolderNotSetDialog quitted")
        self.print_log()
    













if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = FTPServerMainWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
