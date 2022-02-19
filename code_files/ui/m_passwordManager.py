from .rawUiFiles.passwordManager_fol import passwordLogin
from .rawUiFiles.passwordManager_fol import password_main
from .rawUiFiles.passwordManager_fol import password_show
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalDicts
from .packages.password_manager.main import PassManager
import pathlib
import pyperclip

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
    def __init__(self , loggerObj , parent=None , firstTime = True , verify_password_func = None , verify_password_func_args = None , login_button_text = None):
        
        # calling the parent init
        super(PasswordLoginWidget, self).__init__(parent)

        # if first time , then we need to create a new password
        self.var_firstTime = firstTime
        self.var_login_button_text = login_button_text

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

        Form.setWindowTitle("Jarvis Password Input")



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
        self.pushButton.clicked.connect(lambda: self.press_view_button(self.pushButton))
        self.pushButton_2.clicked.connect(lambda: self.press_view_button(self.pushButton_2))
        
        # connect login button
        self.login_btn.clicked.connect(lambda: self.press_login_button(self.login_btn))
        self.input1.returnPressed.connect(lambda: self.press_login_button(self.login_btn))

        
        if(self.var_firstTime and (self.var_login_button_text == None)):
            self.login_btn.setText("Create")
        elif(self.var_firstTime):
            self.login_btn.setText(self.var_login_button_text)
            

        # connect quit button
        self.exit_btn.clicked.connect(lambda: self.exit_button_pressed(self.exit_btn))

        self.loggerObj.debug("finished custom ui setup")
        self.print_log()




    # function to define when the view button is clicked
    def press_view_button(self , buttonObj):

        self.loggerObj.debug("view button clicked")
        self.print_log()

        self.animate_button_press(buttonObj)

        button_name = buttonObj.objectName()

        # if the button is not in dict add it
        if(GlobalData.buttonValues.get(buttonObj , None) is None):
            GlobalData.buttonValues[buttonObj] = False

            self.loggerObj.debug("add view button to dict")
            self.print_log()

        # if the button is clicked when it is in off state
        if(GlobalData.buttonValues.get(buttonObj , None) is False):

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

        # if the button is clicked when it is in on state
        elif(GlobalData.buttonValues.get(buttonObj , None) is True):

            if(button_name == "pushButton"):
                self.input1.setEchoMode(QtWidgets.QLineEdit.Password)
            else:
                self.input2.setEchoMode(QtWidgets.QLineEdit.Password)
            
            GlobalData.buttonValues[buttonObj] = False

            buttonObj.setText("View")
            
            buttonObj.setStyleSheet(GlobalData.original_button_styleSheet.get(buttonObj))
            
            self.loggerObj.debug("view button turned off")
            self.print_log()




    # function to handle exit button press
    def exit_button_pressed(self , buttonObj):

        self.loggerObj.debug("exiting password login window")
        self.print_log()

        self.animate_button_press(buttonObj)

        self.close_button()



    # function to define when login button is clicked
    def press_login_button(self , buttonObj):

        self.loggerObj.debug("login button clicked")
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



































# class implementing additonal ui elements in password login widget
class PasswordShowWidget(QtWidgets.QWidget , password_show.Ui_Form):

    # call the 
    def __init__(self , loggerObj , parent=None , add = True , data = None):
        
        # calling the parent init
        super(PasswordShowWidget, self).__init__(parent)

        # setup logger obj
        self.loggerObj_store = loggerObj
        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        # variable containg password after verifying
        self.returnedPassword = None

        self.var_add = add
        self.var_data = data

        # 0 - add button
        # 1 - update button
        # 2 - delete button
        # 3 - back button
        self.windowQuitFlag = None

        if(not(self.var_add) and (self.var_data == None)):
            raise RuntimeError("data Excepted")

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

        Form.setWindowTitle("Jarvis Password Edit")



        # if not first time
        if(self.var_add):
            self.history_label.hide()
            self.history_textBrowser.hide()
            self.history_view_button.hide()

            self.delete_button.hide()
            self.ok_button.setText("Add")

        else:
            self.username_lineEdit.setText(self.var_data.get("username" , "")) , 
            self.password_lineEdit.setText(self.var_data.get("password" , "")) ,
            self.url_lineEdit.setText(self.var_data.get("url" , "")) , 
            self.caption_lineEdit.setText(self.var_data.get("caption" , "")) ,

            tags_string = ""

            for i in self.var_data.get("tags" , []):
                tags_string = tags_string + i + " "
 
            tags_string = tags_string.strip()

            self.tags_lineEdit.setText(tags_string) ,

            historyText = ""

            for i in self.var_data.get("history" , "").splitlines():
                historyText = historyText + "*"*len(i) + "\n"

            self.history_textBrowser.setText(historyText) ,


            self.history_view_button.clicked.connect(lambda: self.press_view_textBrowser_button(self.history_view_button , self.history_textBrowser , self.var_data.get("history" , "")))
            self.delete_button.clicked.connect(lambda: self.delete_button_pressed(self.delete_button))

            self.ok_button.setText("Update")


        self.tags_lineEdit.setPlaceholderText("space seperated tags")




        # set password input echo mode to default
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        # connect copy button buttons
        self.username_copy_button.clicked.connect(lambda: self.copy_button_pressed(self.username_copy_button , self.username_lineEdit))
        self.password_copy_button.clicked.connect(lambda: self.copy_button_pressed(self.password_copy_button , self.password_lineEdit))
        self.url_copy_button.clicked.connect(lambda: self.copy_button_pressed(self.url_copy_button , self.url_lineEdit))
        
        # connect ok button
        self.ok_button.clicked.connect(lambda: self.ok_button_pressed(self.ok_button))
        self.back_button.clicked.connect(lambda: self.back_button_pressed(self.back_button))

        # connect view button
        self.password_view_button.clicked.connect(lambda: self.press_view_button(self.password_view_button , self.password_lineEdit))
        
        
        self.loggerObj.debug("finished custom ui setup")
        self.print_log()






    # method to copy line edit corresponding to button press
    def copy_button_pressed(self , buttonObj , lineEditObj):

        toCopy = lineEditObj.text()

        pyperclip.copy(toCopy)

        self.animate_button_press(buttonObj , "Copied !" , 0.15)






    def press_view_button(self , buttonObj , lineEditToToggle):

        self.loggerObj.debug("view button clicked")
        self.print_log()

        self.animate_button_press(buttonObj)

        # if the button is not in dict add it
        if(GlobalData.buttonValues.get(buttonObj , None) is None):
            GlobalData.buttonValues[buttonObj] = False

            self.loggerObj.debug("add view button to dict")
            self.print_log()

        # if the button is clicked when it is in off state
        if(GlobalData.buttonValues.get(buttonObj) is False):

            lineEditToToggle.setEchoMode(QtWidgets.QLineEdit.Normal)
            
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

        # if the button is clicked when it is in on state
        elif(GlobalData.buttonValues.get(buttonObj) is True):

            lineEditToToggle.setEchoMode(QtWidgets.QLineEdit.Password)
            
            GlobalData.buttonValues[buttonObj] = False

            buttonObj.setText("View")
            
            buttonObj.setStyleSheet(GlobalData.original_button_styleSheet.get(buttonObj))
            
            self.loggerObj.debug("view button turned off")
            self.print_log()






    # method to toggle btw password and normal view in text browser
    def press_view_textBrowser_button(self , buttonObj , textBrowserObj , textBrowserOriginalData):

        self.loggerObj.debug("view button clicked")
        self.print_log()

        self.animate_button_press(buttonObj)

        # if the button is not in dict add it
        if(GlobalData.buttonValues.get(buttonObj , None) is None):
            GlobalData.buttonValues[buttonObj] = False

            self.loggerObj.debug("add view button to dict")
            self.print_log()


        # if the button is clicked when it is in off state
        if(GlobalData.buttonValues.get(buttonObj) is False):

            textBrowserObj.setText(textBrowserOriginalData)

            
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

        # if the button is clicked when it is in on state
        elif(GlobalData.buttonValues.get(buttonObj) is True):

            newData = ""

            for i in textBrowserOriginalData.splitlines():
                newData = newData + "*"*len(i) + "\n"

            textBrowserObj.setText(newData)
            
            GlobalData.buttonValues[buttonObj] = False

            buttonObj.setText("View")
            
            buttonObj.setStyleSheet(GlobalData.original_button_styleSheet.get(buttonObj))
            
            self.loggerObj.debug("view button turned off")
            self.print_log()

        




    # method to execute when ok button is clicked
    def ok_button_pressed(self , buttonObj):

        self.loggerObj.debug("ok button clicked")
        self.print_log()

        if(self.var_add):
            resultDict = {
                "username" : self.username_lineEdit.text() , 
                "password" : self.password_lineEdit.text() ,
                "url" : self.url_lineEdit.text() , 
                "caption" : self.caption_lineEdit.text() , 
                "tags" : self.tags_lineEdit.text() ,
            }

            self.windowQuitFlag = 0


        else:
            resultDict = {
                "username" : self.username_lineEdit.text() , 
                "password" : self.password_lineEdit.text() ,
                "url" : self.url_lineEdit.text() , 
                "caption" : self.caption_lineEdit.text() , 
                "tags" : self.tags_lineEdit.text() ,
            }
        

            self.windowQuitFlag = 1


        self.var_data = resultDict

        self.animate_button_press(buttonObj)

        self.close_button()





    # method to execute when delete button is clicked
    def delete_button_pressed(self , buttonObj):

        self.loggerObj.debug("delete button clicked")
        self.print_log()

        self.windowQuitFlag = 2

        self.animate_button_press(buttonObj)

        self.close_button()






    # method to execute when delete button is clicked
    def back_button_pressed(self , buttonObj):

        self.loggerObj.debug("back button clicked")
        self.print_log()

        self.windowQuitFlag = 3

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


    







































# class containing main password screen ui
class PasswordMainWidget(QtWidgets.QWidget , password_main.Ui_Form):

    # call the init
    def __init__(self , filePath , loggerObj , parent=None):
        
        # calling the parent init
        super(PasswordMainWidget, self).__init__(parent)

        # setup logger obj
        self.loggerObj_store = loggerObj
        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        self.loggerObj.debug("finished object init")
        self.print_log()

        self.continueSetup = True


        # if the db file already exist
        self.filePath = pathlib.Path(filePath).absolute()
        self.filePath_str = str(self.filePath)

        # if the db already exist then it is not first time
        firstTime = not(self.filePath.is_file())


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
            ui = PasswordLoginWidget(loggerObj , firstTime=firstTime , verify_password_func=verifyPassFunc , verify_password_func_args=[self.filePath])
            ui.setupUi(Form)
            Form.show()
            Form.exec()

            returnedPassword = ui.returnedPassword

            if(firstTime and ((returnedPassword == None) or (returnedPassword == ""))):
                try:
                    os.remove(filePath)
                except FileNotFoundError:
                    pass
                return None 
            if((returnedPassword == None) or (returnedPassword == "")):
                return None


            del ui
            del Form

            return returnedPassword


        self.verifyPassFunc_func = verifyPassFunc
        self.openPassInputWindow_func = openPassInputWindow


        # generate db object
        self._password = openPassInputWindow()

        if(self._password == None):
            self.continueSetup = False
            return None

        self.dbObj = PassManager(self._password , self.filePath_str)
        self.dbObj_all = self.dbObj.db.all()














    # function to setup ui
    def setupUi(self, Form):

        # calling the parent setupUi
        super().setupUi(Form)

        # form close button
        self.close_button = Form.close

        Form.setWindowTitle("Jarvis Password Manager")

        self.loggerObj.debug("finished parent ui setup")
        self.print_log()

        # generate password in scroll area
        self.addPassToScrollArea()

        self.filter_lineEdit.textChanged[str].connect(self.filter_password_in_scollView)

        self.add_new_button.clicked.connect(lambda : self.add_button_pressed(self.add_new_button))

        self.loggerObj.debug("finished custom ui setup")
        self.print_log()

        self.back_button.setText("Change Pass")

        self.quit_button.clicked.connect(lambda : self.quit_button_pressed(self.quit_button))
        self.back_button.clicked.connect(lambda : self.change_pass_button_pressed(self.back_button))




    

    # function to add all passwords to scroll area
    def addPassToScrollArea(self , defaultList = None):

        if(defaultList == None):
            defaultList = self.dbObj_all

        self.loggerObj.debug("adding passwords to scroll area")
        self.print_log()

        # clear all previous widgets in vertical layout _2
        clearLayout2(self.verticalLayout_2)

        self.loggerObj.debug("cleared old widgets in scroll area")
        self.print_log()

        count = 1

        # using button group to seperate out which button was clicked
        self.caption_button_group = QtWidgets.QButtonGroup()
        self.caption_button_group.setExclusive(True)

        self.cuser_button_group = QtWidgets.QButtonGroup()
        self.cuser_button_group.setExclusive(True)

        self.cpass_button_group = QtWidgets.QButtonGroup()
        self.cpass_button_group.setExclusive(True)


        for item in defaultList:
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

        self.loggerObj.debug(f"successfully added all passwords")
        self.print_log()






    # function to filter password in scroll view
    def filter_password_in_scollView(self):
        
        # get text from filter line edit
        toSearch = self.filter_lineEdit.text()

        # if empty display all
        if(toSearch == ""):
            self.addPassToScrollArea(None)

        newList = []

        # search for each db instance
        for i in self.dbObj_all:

            found = False

            caption = i.get("caption" , "")
            tags = i.get("tags" , [])

            # if caption matches
            if(caption.find(toSearch) != -1):
                found = True
            else:
                for j in tags:

                    # if any tag matches
                    if(j.find(toSearch) != -1):
                        found = True
                        break
            
            if(found):
                newList.append(i)

        self.addPassToScrollArea(newList)
        






    # function to handle events when change pass button is clicked
    def change_pass_button_pressed(self , buttonObj):
        self.loggerObj.debug(f"chage pass button clicked")
        self.print_log()

        self.animate_button_press(buttonObj)


        def openPassInputWindow(self):
            Form = QtWidgets.QDialog()
            ui = PasswordLoginWidget(self.loggerObj_store , firstTime=True , verify_password_func=self.verifyPassFunc_func , verify_password_func_args=[self.filePath] , login_button_text="Change Pass")
            ui.setupUi(Form)
            Form.show()
            Form.exec()

            returnedPassword = ui.returnedPassword

            if((returnedPassword == None) or (returnedPassword == "")):
                return None


            del ui
            del Form

            return returnedPassword


        # generate db object
        returnedPassword = openPassInputWindow(self)

        if(returnedPassword == None):
            return None
        else:
            self._password = returnedPassword

            self.dbObj.db.storage.change_encryption_key(self._password)

            self.dbObj_all = self.dbObj.db.all()

            self.showPasswordChangedDialog()

        




    # function to handle evenets when quit button is clicked
    def quit_button_pressed(self , buttonObj):
        self.loggerObj.info(f"quiting password manager")
        self.print_log()

        self.animate_button_press(buttonObj)

        del self.dbObj
        del self.dbObj_all
        del self._password

        self.close_button()






    # function to handle events when caption button is clicked
    def caption_button_pressed(self , buttonObj):

        self.loggerObj.debug(f"caption button clicked")
        self.print_log()

        self.animate_button_press(buttonObj)
        
        id = buttonObj.objectName().split(":")[0]
        id_instance = self.dbObj.db.search(self.dbObj.query.id == id)[0]

        Form = QtWidgets.QDialog()
        ui = PasswordShowWidget(self.loggerObj_store , add = False , data=id_instance)
        ui.setupUi(Form)
        Form.show()
        Form.exec()

        if(ui.windowQuitFlag == 1):
            newDict = ui.var_data

            self.dbObj.update_pass(id , newDict.get("username" , "") , newDict.get("password" , "") , newDict.get("caption" , "") , newDict.get("url" , "") , newDict.get("tags" , ""))

            self.dbObj_all = self.dbObj.db.all()
            self.addPassToScrollArea()

            self.loggerObj.info(f"password updated")
            self.print_log()

        if(ui.windowQuitFlag == 2):
            
            self.dbObj.delete_pass(id)

            self.dbObj_all = self.dbObj.db.all()
            self.addPassToScrollArea()

            self.loggerObj.info(f"password deleted")
            self.print_log()

        del ui
        del Form

        



    # function to handle events when caption button is clicked
    def add_button_pressed(self , buttonObj):

        self.loggerObj.debug(f"add button clicked")
        self.print_log()

        self.animate_button_press(buttonObj)
        
        Form = QtWidgets.QDialog()
        ui = PasswordShowWidget(self.loggerObj_store)
        ui.setupUi(Form)
        Form.show()
        Form.exec()

        if(ui.windowQuitFlag == 0):
            newDict = ui.var_data

            self.dbObj.insert_new_pass(newDict.get("username" , "") , newDict.get("password" , "") , newDict.get("caption" , "") , newDict.get("url" , "")  , newDict.get("tags" , "") , history="")

            self.dbObj_all = self.dbObj.db.all()
            self.addPassToScrollArea()

            self.loggerObj.info(f"password added")
            self.print_log()

        del ui
        del Form




    # function to handle events when cuser button is clicked
    def cuser_button_pressed(self , buttonObj):

        self.loggerObj.debug(f"cuser button clicked")
        self.print_log()
        
        id = buttonObj.objectName().split(":")[0]

        id_instance = self.dbObj.db.search(self.dbObj.query.id == id)[0]
        
        username = id_instance.get("username" , "")

        pyperclip.copy(username)

        self.loggerObj.debug(f"copied username to clipboard")
        self.print_log()

        self.animate_button_press(buttonObj , "Copied !" , 0.15)





    # function to handle events when caption cpass is clicked
    def cpass_button_pressed(self , buttonObj):
        
        self.loggerObj.debug(f"cpass button clicked")
        self.print_log()
        
        id = buttonObj.objectName().split(":")[0]

        id_instance = self.dbObj.db.search(self.dbObj.query.id == id)[0]
        
        password = id_instance.get("password" , "")

        pyperclip.copy(password)

        self.loggerObj.debug(f"copied password to clipboard")
        self.print_log()

        self.animate_button_press(buttonObj , "Copied !" , 0.15)







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
    def showPasswordChangedDialog(self):
        self.loggerObj.debug("showPasswordChangedDialog invoked")
        self.print_log()

        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle("Jarvis Info")

        msg.setText("Password changed successfully")


        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)



        runMsg = msg.exec_()

        self.loggerObj.debug("showPasswordChangedDialog quitted")
        self.print_log()
    













if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = PasswordLoginWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
