from typing import _SpecialForm
from .rawUiFiles.passwordManager_fol import passwordLogin
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalDicts
from .packages.globalData.globalDataClasses import M_passwordManager_GlobalData





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

















def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
                child.widget().deleteLater()

















class mainScreenWidget(QtWidgets.QWidget , passwordLogin.Ui_Form):

    # call the 
    def __init__(self, parent=None , firstTime = True , verify_password_func = None , return_password = None):
        
        # calling the parent init
        super(mainScreenWidget, self).__init__(parent)

        self.var_firstTime = firstTime
        self.var_verify_password_func = verify_password_func














    def setupUi(self, Form):

        self.close_button = Form.close

        # calling the parent setupUi
        super().setupUi(Form)

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




    # function to define when the view button is pressed
    def press_view_button(self , buttonObj):

        self.animate_button_press(buttonObj)

        button_name = buttonObj.objectName()

        # if the button is not in dict add it
        if(GlobalData.buttonValues.get(buttonObj , None) is None):
            GlobalData.buttonValues[buttonObj] = False

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
        

        # if the button is pressed when it is in on state
        elif(GlobalData.buttonValues.get(buttonObj) is True):

            if(button_name == "pushButton"):
                self.input1.setEchoMode(QtWidgets.QLineEdit.Password)
            else:
                self.input2.setEchoMode(QtWidgets.QLineEdit.Password)
            
            GlobalData.buttonValues[buttonObj] = False

            buttonObj.setText("View")
            
            buttonObj.setStyleSheet(GlobalData.original_button_styleSheet.get(buttonObj))
            






    def press_login_button(self , buttonObj):
        self.animate_button_press(buttonObj)

        
        # if first time
        if(self.var_firstTime):
            pass1 = self.input1.text()
            pass2 = self.input2.text()

            if(pass1 != pass2):
                self.showPasswordDoesNotMatch()
            else:
                M_passwordManager_GlobalData.newPassword = pass1
                self.close_button()

        else:
            pass1 = self.input1.text()

            if(self.var_verify_password_func(pass1)):
                self.close_button()
            else:
                self.showPasswordIncorrect()


                




    # function to animate the button press
    def animate_button_press(self , buttonObj):
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





    # function to show a message pop warning that the passwords does not match
    def showPasswordIncorrect(self):
        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle("Jarvis Error")

        msg.setText("Incorrect password , recheck and try again")

        msg.setIcon(QtWidgets.QMessageBox.Critical)

        msg.setStandardButtons(QtWidgets.QMessageBox.Retry)

        runMsg = msg.exec_()









if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = mainScreenWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
