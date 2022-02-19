from .rawUiFiles.settings_fol import settings

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalDicts
from .packages.password_manager.main import PassManager
import pathlib
import pyperclip
import getpass
from tinydb import TinyDB , Query

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
    










































# class containing main password screen ui
class SettingsMainWidget(QtWidgets.QWidget , settings.Ui_Form):

    # call the init
    def __init__(self , filePath , loggerObj , parent=None):
        
        # calling the parent init
        super(SettingsMainWidget, self).__init__(parent)

        # setup logger obj
        self.loggerObj_store = loggerObj
        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        self.dbObj = TinyDB(path = filePath)
        self.query = Query()

        try:
            self.username = self.dbObj.search(self.query.id == "username")[0].get("value" , getpass.getuser())
        except IndexError:
            self.username = getpass.getuser()
            self.dbObj.insert({"id" : "username" , "value" : self.username})

        try:
            self.password_db_path = self.dbObj.search(self.query.id == "password_db_path")[0].get("value" , "")
        except IndexError:
            self.password_db_path = ""
            self.dbObj.insert({"id" : "password_db_path" , "value" : self.password_db_path})



        self.settingsDict = {
            "username" : self.username , 
            "password_db_path" : self.password_db_path , 
        }

        self.loggerObj.debug("finished object init")
        self.print_log()













    # function to setup ui
    def setupUi(self, Form):

        # calling the parent setupUi
        super().setupUi(Form)

        # form close button
        self.close_button = Form.close

        Form.setWindowTitle("Jarvis Settings")

        self.loggerObj.debug("finished parent ui setup")
        self.print_log()




        # add username field
        self.username_verticalLayout = QtWidgets.QVBoxLayout()
        self.username_verticalLayout.setObjectName("username_verticalLayout")
        
        self.username_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.username_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: 63 24pt \"FreeSans\";\n"
"color: rgb(255, 255, 255);\n"
"padding: 8px;\n"
"margin: 8px;")
        self.username_label.setObjectName("username_label")
        self.username_label.setText("Username : ")
        
        self.username_verticalLayout.addWidget(self.username_label, 0, QtCore.Qt.AlignVCenter)
        
        self.username_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.username_lineEdit.setStyleSheet("background-color: rgb(85, 87, 83);\n"
"font: 63 24pt \"FreeSans\";\n"
"color: rgb(255, 255, 255);\n"
"padding: 8px;\n"
"margin: 8px;")
        self.username_lineEdit.setObjectName("username_lineEdit")
        self.username_lineEdit.setText(self.username)
        
        self.username_verticalLayout.addWidget(self.username_lineEdit)
        
        self.verticalLayout_2.addLayout(self.username_verticalLayout)




        # add passwords db file path
        self.password_db_path_verticalLayout = QtWidgets.QVBoxLayout()
        self.password_db_path_verticalLayout.setObjectName("password_db_path_verticalLayout")
        
        self.password_db_path_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.password_db_path_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: 63 24pt \"FreeSans\";\n"
"color: rgb(255, 255, 255);\n"
"padding: 8px;\n"
"margin: 8px;")
        self.password_db_path_label.setObjectName("password_db_path_label")
        self.password_db_path_label.setText("Password db path : ")
        
        self.password_db_path_verticalLayout.addWidget(self.password_db_path_label, 0, QtCore.Qt.AlignVCenter)
        
        self.password_db_path_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.password_db_path_lineEdit.setStyleSheet("background-color: rgb(85, 87, 83);\n"
"font: 63 24pt \"FreeSans\";\n"
"color: rgb(255, 255, 255);\n"
"padding: 8px;\n"
"margin: 8px;")
        self.password_db_path_lineEdit.setObjectName("password_db_path_lineEdit")
        self.password_db_path_lineEdit.setText(self.password_db_path)
        
        self.password_db_path_verticalLayout.addWidget(self.password_db_path_lineEdit)
        
        self.verticalLayout_2.addLayout(self.password_db_path_verticalLayout)



        self.pushButton_2.clicked.connect(lambda : self.save_button_clicked(self.pushButton_2))
        self.pushButton.clicked.connect(self.close_button)






    # function to define save button event
    def save_button_clicked(self , buttonObj):

        self.loggerObj.debug("save button clicked")
        self.print_log()

        self.dbObj.update({
            "value" : self.username_lineEdit.text() , 
        } , 
        self.query.id == "username")

        password_db_path = self.password_db_path_lineEdit.text()

        if(not(pathlib.Path(password_db_path).absolute().is_file()) and not(password_db_path == "")):
            self.showErrorDialog(f"no file found at {password_db_path}")
            return 
            
        self.dbObj.update({
            "value" :  password_db_path, 
        } , 
        self.query.id == "password_db_path")


        self.settingsDict = {
            "username" : self.username_lineEdit.text() , 
            "password_db_path" : password_db_path , 
        }

        self.animate_button_press(buttonObj)

        self.close_button()





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
    def showErrorDialog(self , errorMsg):
        self.loggerObj.debug(f"showErrorDialog invoked with error = {errorMsg}")
        self.print_log()

        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle("Jarvis Error")

        msg.setText(errorMsg)


        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setStandardButtons(QtWidgets.QMessageBox.Retry)

        runMsg = msg.exec_()

        self.loggerObj.debug(f"showErrorDialog quitted with error = {errorMsg}")
        self.print_log()
    













if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = SettingsMainWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
