from .rawUiFiles.ftpServer_fol import ftpServer
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalDicts
import pathlib
import pyperclip
import socket

import logging
from io import StringIO


# importing FTP module
from pyftpdlib import log
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import errno
from contextlib import closing



from threading import Thread

class GlobalData:

    buttonValues = {}
    original_button_styleSheet = {}

    serverObj = None








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







def startFTPserver(address , handler):
    server = servers.FTPServer(address, handler)

    GlobalData.serverObj = server

    server.serve_forever()









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



        self.streamIO = StringIO()
        self.stream_handler = logging.StreamHandler(self.streamIO)

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

        # select button
        self.select_button.clicked.connect(lambda : self.select_button_clicked(self.select_button))

        # set value in labels
        self.ip_value_label.setText(NMethods.get_ip_address())
        self.port_value_label.setText(str(NMethods.getPort(int(self.var_port))))
        self.ip_port_value_label.setText("ftp://" + self.ip_value_label.text() + ":" + self.port_value_label.text())
        self.username_value_label.setText(self.var_username)
        self.password_value_label.setText(self.var_password)
        self.folder_shared_value_text_browser.setText(str(self.var_default_folder))



        # start button
        self.start_button.clicked.connect(lambda : self.start_ftp_server(self.start_button))


        # quit button
        self.quit_button.clicked.connect(lambda : self.quit_button_clicked(self.quit_button))


        # copy buttons
        self.ip_copy_button.clicked.connect(lambda : self.copy_button_clicked(self.ip_copy_button , self.ip_value_label.text()))
        self.port_copy_button.clicked.connect(lambda : self.copy_button_clicked(self.port_copy_button , self.port_value_label.text()))
        self.ip_port_copy_button.clicked.connect(lambda : self.copy_button_clicked(self.ip_port_copy_button , self.ip_port_value_label.text()))
        self.username_copy_button.clicked.connect(lambda : self.copy_button_clicked(self.username_copy_button , self.username_value_label.text()))
        self.password_copy_button.clicked.connect(lambda : self.copy_button_clicked(self.password_copy_button , self.password_value_label.text()))
        self.folder_shared_copy_button.clicked.connect(lambda : self.copy_button_clicked(self.folder_shared_copy_button , self.folder_shared_value_text_browser.toPlainText()))

        # clear log Text browser
        self.log_text_browser.setText("")

        self.loggerObj.debug("completed ui")
        self.print_log()





    # function to define copy button operation
    def copy_button_clicked(self , buttonObj , toCopy):
        self.loggerObj.debug(f"copy button clicked")
        self.print_log()

        pyperclip.copy(toCopy)

        self.loggerObj.debug(f"copied password to clipboard")
        self.print_log()

        self.animate_button_press(buttonObj , "Copied !" , 0.15)




    # function to define what happens when select button is pressed
    def select_button_clicked(self , buttonObj):
        self.loggerObj.debug("select button pressed")
        self.print_log()

        self.animate_button_press(buttonObj)

        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        dlg.setDirectory(QtCore.QDir.homePath())
            
        dlg.exec()

        filenames = dlg.selectedFiles()
        
        try:
            dirName = filenames[0]
        except IndexError:
            self.showErrorDialog(f"Select a dir first")
            return

        self.folder_shared_value_text_browser.setText(str(dirName))

        self.stackedWidget.setCurrentIndex(1)





    # function to define when default button is pressed
    def default_button_clicked(self , buttonObj):
        self.loggerObj.debug("default button pressed")
        self.print_log()

        if(self.var_default_folder == ""):
            self.showDefaultFolderNotSetDialog()
            return

        self.animate_button_press(buttonObj)

        self.stackedWidget.setCurrentIndex(1)

        
            



    def start_ftp_server(self , buttonObj):
        self.loggerObj.info("starting ftp server")
        self.print_log()

        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Define a new user having full r/w permissions and a read-only
        # anonymous user
        authorizer.add_user(self.username_value_label.text(), self.password_value_label.text() , self.folder_shared_value_text_browser.toPlainText() , perm='elradfmwMT')

        if(self.var_anonymous == "True"):
            self.loggerObj.info("anonymous access allowed")
            self.print_log()
            authorizer.add_anonymous(homedir=self.folder_shared_value_text_browser.toPlainText())

        # Instantiate FTP handler class
        handler = FTPHandler
        handler.authorizer = authorizer

        pyftpdlib_logger = logging.getLogger("pyftpdlib")
        pyftpdlib_logger.addHandler(self.stream_handler)

        log.config_logging(logging.INFO)
                
        self.showLogsTimer = QtCore.QTimer()
        self.showLogsTimer.timeout.connect(self.showLogs)
        self.showLogsTimer.start(500)

        # Define a customized banner (string returned when client connects)
        handler.banner = "pyftpdlib based ftpd ready."
        address = (self.ip_value_label.text() , int(self.port_value_label.text()))  
        
        self.serverThread = Thread(target=startFTPserver, args=(address,handler,) , daemon=True)
        self.serverThread.start()

        self.loggerObj.info("FTP server started")
        self.print_log()

        self.animate_button_press(buttonObj)

        buttonObj.setText("Started !")
        buttonObj.setDisabled(True)







    def quit_button_clicked(self , buttonObj):
        self.animate_button_press(buttonObj)

        if(GlobalData.serverObj != None):
            GlobalData.serverObj.close_all()

        self.loggerObj.info("FTP server Closed")
        self.print_log()

        self.close_button()






    def showLogs(self):
        self.streamIO.flush()
        value = self.streamIO.getvalue()

        if(len(value) == 0):
            return

        self.log_text_browser.append(value)

        # reset stream io
        self.streamIO.seek(0)
        self.streamIO.truncate(0)



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



        runMsg = msg.exec()

        self.loggerObj.debug("showDefaultFolderNotSetDialog quitted")
        self.print_log()




    # function to show a message pop warning that the passwords does not match
    def showErrorDialog(self , errorMsg):
        self.loggerObj.debug(f"showErrorDialog invoked with error = {errorMsg}")
        self.print_log()

        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle("Jarvis Error")

        msg.setText(errorMsg)


        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setStandardButtons(QtWidgets.QMessageBox.Retry)

        runMsg = msg.exec()

        self.loggerObj.debug(f"showErrorDialog quitted with error = {errorMsg}")
        self.print_log()
    













if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = FTPServerMainWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
