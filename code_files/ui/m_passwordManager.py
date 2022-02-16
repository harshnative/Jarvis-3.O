from .rawUiFiles.passwordManager_fol import passwordLogin
from .rawUiFiles.passwordManager_fol import password_main
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalDicts
from .packages.password_manager.main import PassManager
import pathlib
from PyQt5 import sip


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
    














#  ____                                                      _   _                       _          __        __  _       _                  _    
# |  _ \    __ _   ___   ___  __      __   ___    _ __    __| | | |       ___     __ _  (_)  _ __   \ \      / / (_)   __| |   __ _    ___  | |_  
# | |_) |  / _` | / __| / __| \ \ /\ / /  / _ \  | '__|  / _` | | |      / _ \   / _` | | | | '_ \   \ \ /\ / /  | |  / _` |  / _` |  / _ \ | __| 
# |  __/  | (_| | \__ \ \__ \  \ V  V /  | (_) | | |    | (_| | | |___  | (_) | | (_| | | | | | | |   \ V  V /   | | | (_| | | (_| | |  __/ | |_  
# |_|      \__,_| |___/ |___/   \_/\_/    \___/  |_|     \__,_| |_____|  \___/   \__, | |_| |_| |_|    \_/\_/    |_|  \__,_|  \__, |  \___|  \__| 
#                                                                                |___/                                        |___/               


# class implementing additonal ui elements in password login widget
class PasswordLoginWidget(QtWidgets.QWidget , passwordLogin.Ui_Form):

    # call the 
    def __init__(self , loggerObj , parent=None , firstTime = True , verify_password_func = None , verify_password_func_args = None):
        
        # calling the parent init
        super(PasswordLoginWidget, self).__init__(parent)

        # if first time , then we need to create a new password
        self.var_firstTime = firstTime

        # verify_password_func_args + password will to passed to verify password func
        self.var_verify_password_func = verify_password_func
        
        # make verify_password_func_args = empty list if None
        if(verify_password_func_args == None):
            self.verify_password_func_args = []
        else:
            self.verify_password_func_args = verify_password_func_args

        # setup logger obj
        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        # variable containg password after verifying
        self.returnedPassword = None

        self.loggerObj.debug("finished object init")
        self.print_log()












    # function to setup ui
    def setupUi(self, Form):

        # calling the parent setupUi
        super().setupUi(Form)

        self.loggerObj.debug("finished parent ui setup")
        self.print_log()

        # close button for closing the dialog
        self.close_button = Form.close



        # if not first time
        if(not(self.var_firstTime)):
            # the rename password label to Enter password
            self.password.setText("Enter Password : ")

            # hide second password label and input
            self.input2.setHidden(True)
            self.password2.setHidden(True)
            self.pushButton_2.setHidden(True)


        # set password input echo mode to default
        self.input1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input2.setEchoMode(QtWidgets.QLineEdit.Password)

        # connect view buttons
        self.pushButton.pressed.connect(lambda: self.press_view_button(self.pushButton))
        self.pushButton_2.pressed.connect(lambda: self.press_view_button(self.pushButton_2))
        
        # connect login button
        self.login_btn.pressed.connect(lambda: self.press_login_button(self.login_btn))
        self.input1.returnPressed.connect(lambda: self.press_login_button(self.login_btn))

        self.loggerObj.debug("finished custom ui setup")
        self.print_log()




    # function to define when the view button is pressed
    def press_view_button(self , buttonObj):

        self.loggerObj.debug("view button pressed")
        self.print_log()

        self.animate_button_press(buttonObj)

        button_name = buttonObj.objectName()

        # if the button is not in dict add it
        if(GlobalData.buttonValues.get(buttonObj , None) is None):
            GlobalData.buttonValues[buttonObj] = False

            self.loggerObj.debug("add view button to dict")
            self.print_log()

        # if the button is pressed when it is in off state
        if(GlobalData.buttonValues.get(buttonObj) is False):

            if(button_name == "pushButton"):
                self.input1.setEchoMode(QtWidgets.QLineEdit.Normal)
            else:
                self.input2.setEchoMode(QtWidgets.QLineEdit.Normal)
            
            GlobalData.buttonValues[buttonObj] = True

            buttonObj.setText("Hide")

            # change the button background color to red
            original_style_sheet = buttonObj.styleSheet()

            original_style_sheetList = original_style_sheet.split("\n")

            new_style_sheetList = []

            for i in original_style_sheetList:
                i = str(i)
                if(i.find("background-color") != -1):
                    new_style_sheetList.append("background-color: rgb(176, 0, 32);\n")
                else:
                    new_style_sheetList.append(i)

            
            buttonObj.setStyleSheet("".join(new_style_sheetList))
            
            GlobalData.original_button_styleSheet[buttonObj] = original_style_sheet
        
            self.loggerObj.debug("view button turned on")
            self.print_log()

        # if the button is pressed when it is in on state
        elif(GlobalData.buttonValues.get(buttonObj) is True):

            if(button_name == "pushButton"):
                self.input1.setEchoMode(QtWidgets.QLineEdit.Password)
            else:
                self.input2.setEchoMode(QtWidgets.QLineEdit.Password)
            
            GlobalData.buttonValues[buttonObj] = False

            buttonObj.setText("View")
            
            buttonObj.setStyleSheet(GlobalData.original_button_styleSheet.get(buttonObj))
            
            self.loggerObj.debug("view button turned off")
            self.print_log()





    # function to define when login button is pressed
    def press_login_button(self , buttonObj):

        self.loggerObj.debug("login button pressed")
        self.print_log()

        self.animate_button_press(buttonObj)

        
        # if first time
        if(self.var_firstTime):
            self.loggerObj.debug("first time login")
            self.print_log()

            pass1 = self.input1.text()
            pass2 = self.input2.text()

            if(pass1 != pass2):
                self.loggerObj.info("passwords does not match")
                self.print_log()
                self.showPasswordDoesNotMatch()

            else:
                self.loggerObj.debug("passwords matched")
                self.print_log()

                # password to create db will be added to returnedPassword object
                self.returnedPassword = pass1

                self.close_button()

        else:
            self.loggerObj.debug("regular login")
            self.print_log()

            pass1 = self.input1.text()

            if(self.var_verify_password_func(*self.verify_password_func_args , pass1)):
                self.loggerObj.debug("password verified")
                self.print_log()

                # password to open db will be added to returnedPassword object
                self.returnedPassword = pass1

                self.close_button()
            else:
                self.loggerObj.info("incorrect password")
                self.print_log()
                self.showPasswordIncorrect()


                




    # function to animate the button press
    def animate_button_press(self , buttonObj):

        self.loggerObj.debug("animate button pressed")
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

        QtCore.QCoreApplication.processEvents()

        time.sleep(0.05)

        buttonObj.setStyleSheet(original_style_sheet)


    



    # function to show a message pop warning that the passwords does not match
    def showPasswordDoesNotMatch(self):
        self.loggerObj.debug("showPasswordDoesNotMatch invoked")
        self.print_log()

        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle("Jarvis Error")

        msg.setText("Password and confirm password does not match , recheck and try again")

        msg.setIcon(QtWidgets.QMessageBox.Critical)
        # msg.setIcon(QtWidgets.QMessageBox.Warning)
        # msg.setIcon(QtWidgets.QMessageBox.Information)
        # msg.setIcon(QtWidgets.QMessageBox.Question)


        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # msg.setStandardButtons(QtWidgets.QMessageBox.Open)
        # msg.setStandardButtons(QtWidgets.QMessageBox.Save)
        # msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        # msg.setStandardButtons(QtWidgets.QMessageBox.Close)
        # msg.setStandardButtons(QtWidgets.QMessageBox.Yes)
        # msg.setStandardButtons(QtWidgets.QMessageBox.No)
        # msg.setStandardButtons(QtWidgets.QMessageBox.Abort)
        msg.setStandardButtons(QtWidgets.QMessageBox.Retry)
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ignore)


        runMsg = msg.exec_()

        self.loggerObj.debug("showPasswordDoesNotMatch quitted")
        self.print_log()





    # function to show a message pop warning that the passwords does not match
    def showPasswordIncorrect(self):
        self.loggerObj.debug("showPasswordIncorrect invoked")
        self.print_log()

        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle("Jarvis Error")

        msg.setText("Incorrect password , recheck and try again")

        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setStandardButtons(QtWidgets.QMessageBox.Retry)

        runMsg = msg.exec_()

        self.loggerObj.debug("showPasswordIncorrect quitted")
        self.print_log()



























# class containing main password screen ui
class PasswordMainWidget(QtWidgets.QWidget , password_main.Ui_Form):

    # call the init
    def __init__(self , filePath , loggerObj , parent=None):
        
        # calling the parent init
        super(PasswordMainWidget, self).__init__(parent)

        # setup logger obj
        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        self.loggerObj.debug("finished object init")
        self.print_log()


        # if the db file already exist
        filePath = pathlib.Path(filePath).absolute()

        # if the db already exist then it is not first time
        firstTime = not(filePath.is_file())


        # function to verify password for db
        def verifyPassFunc(filePath , password):
            try:
                PassManager(password , filePath)
                return True
            except RuntimeError:
                return False


        # function to open the password input widget and get the password
        def openPassInputWindow():
            Form = QtWidgets.QDialog()
            ui = PasswordLoginWidget(loggerObj , firstTime=firstTime , verify_password_func=verifyPassFunc , verify_password_func_args=[filePath])
            ui.setupUi(Form)
            Form.show()
            Form.exec()

            returnedPassword = ui.returnedPassword

            del ui
            del Form

            return returnedPassword


        # generate db object
        self._password = openPassInputWindow()
        self.dbObj = PassManager(self._password , filePath)














    # function to setup ui
    def setupUi(self, Form):

        # calling the parent setupUi
        super().setupUi(Form)

        # form close button
        self.close_button = Form.close

        self.loggerObj.debug("finished parent ui setup")
        self.print_log()


        self.addPassToScrollArea()

        self.loggerObj.debug("finished custom ui setup")
        self.print_log()





    

    # function to add all passwords to scroll area
    def addPassToScrollArea(self):

        self.loggerObj.debug("adding passwords to scroll area")
        self.print_log()

        # clear all previous widgets in vertical layout _2
        clearLayout2(self.verticalLayout_2)

        self.loggerObj.debug("cleared old widgets in scroll area")
        self.print_log()

        count = 1

        # using button group to seperate out which button was pressed
        self.caption_button_group = QtWidgets.QButtonGroup()
        self.caption_button_group.setExclusive(True)

        self.cuser_button_group = QtWidgets.QButtonGroup()
        self.cuser_button_group.setExclusive(True)

        self.cpass_button_group = QtWidgets.QButtonGroup()
        self.cpass_button_group.setExclusive(True)


        for item in self.dbObj.db.all():
            # horizontal layout
            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setContentsMargins(-1, 0, -1, 16)

            # caption button
            pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            pushButton.setStyleSheet("font: 81 20pt \"FreeSans\";\n"
    "background-color: rgb(55, 0, 179);\n"
    "color: rgb(255, 255, 255);\n"
    "padding: 16px;\n"
    "text-align: left;")

            pushButton.setObjectName(item.get("id") + ":caption")
            pushButton.setText(f"""{count}. {item.get("caption")}""")
            self.caption_button_group.addButton(pushButton)

            horizontalLayout.addWidget(pushButton)


            # username copy button
            pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            pushButton_2.setStyleSheet("font: 100 20pt \"FreeSans\";\n"
    "background-color: rgb(78, 154, 6);\n"
    "color: rgb(255, 255, 255);\n"
    "padding: 16px;")

            pushButton_2.setObjectName(item.get("id") + ":C_user")
            pushButton_2.setText("C_user")
            self.cuser_button_group.addButton(pushButton_2)

            horizontalLayout.addWidget(pushButton_2)


            # password copy button
            pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            pushButton_3.setStyleSheet("font: 100 20pt \"FreeSans\";\n"
    "background-color: rgb(78, 154, 6);\n"
    "color: rgb(255, 255, 255);\n"
    "padding: 16px;")

            pushButton_3.setObjectName(item.get("id") + ":C_pass")
            pushButton_3.setText("C_pass")
            self.cpass_button_group.addButton(pushButton_3)

            horizontalLayout.addWidget(pushButton_3)
            horizontalLayout.setStretch(0, 5)
            horizontalLayout.setStretch(1, 1)
            horizontalLayout.setStretch(2, 1)

            # add horizontal layout to scroll area
            self.verticalLayout_2.addLayout(horizontalLayout)

            self.loggerObj.debug(f"successfully added password at count = {count}")
            self.print_log()

            count = count + 1


        self.caption_button_group.buttonPressed.connect(self.caption_button_pressed)
        self.cuser_button_group.buttonPressed.connect(self.cuser_button_pressed)
        self.cpass_button_group.buttonPressed.connect(self.cpass_button_pressed)





    # function to handle events when caption button is pressed
    def caption_button_pressed(self , buttonObj):

        self.animate_button_press(buttonObj)
        
        print(buttonObj.objectName())
        print(buttonObj.text())





    # function to handle events when cuser button is pressed
    def cuser_button_pressed(self , buttonObj):

        self.animate_button_press(buttonObj)
        
        print(buttonObj.objectName())
        print(buttonObj.text())



    # function to handle events when caption cpass is pressed
    def cpass_button_pressed(self , buttonObj):

        self.animate_button_press(buttonObj)
        
        print(buttonObj.objectName())
        print(buttonObj.text())





    # function to animate the button press
    def animate_button_press(self , buttonObj):

        self.loggerObj.debug("animate button pressed")
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

        QtCore.QCoreApplication.processEvents()

        time.sleep(0.05)

        buttonObj.setStyleSheet(original_style_sheet)


    













if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = PasswordLoginWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
