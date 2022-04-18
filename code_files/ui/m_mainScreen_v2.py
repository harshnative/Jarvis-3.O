from typing import _SpecialForm
from .rawUiFiles.mainScreen_fol import mainScreen
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalLists
from .packages.globalData.globalDataClasses import GlobalData_main
import logging
from .packages.log_module.logger import Logger
from .m_passwordManager import PasswordMainWidget
from .m_settings import SettingsMainWidget
from .m_ftpServer import FTPServerMainWidget
import pathlib
from pyqtgraph import PlotWidget, plot
import pyqtgraph
import random
from threading import Thread
from collections import deque
from scipy.interpolate import make_interp_spline
import numpy







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













class MainScreenWidget(QtWidgets.QWidget , mainScreen.Ui_Form):

    # call the 
    def __init__(self , loggerObj , parent=None):
        
        # calling the parent init
        super(MainScreenWidget, self).__init__(parent)

        self.loggerObj_store = loggerObj
        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        self.loggerObj.debug("finished object init")
        self.print_log()

        self.dialogBox_storage = {}

        if(GlobalData_main.isOnLinux):
            settingsPath = pathlib.Path(GlobalData_main.folderPathLinux , "settings.db").absolute()
        else:
            settingsPath = pathlib.Path(GlobalData_main.folderPathWindows , "settings.db").absolute()


        self.settingsPath = settingsPath

        tempUi = SettingsMainWidget(self.settingsPath , self.loggerObj_store)

        self.settingsDict = tempUi.settingsDict

        del tempUi














    def setupUi(self, Form):

        self.Form = Form

        # calling the parent setupUi
        super().setupUi(Form)

        Form.setWindowTitle("Jarvis 3.O")


        self.loggerObj.debug("finished parent ui setup")
        self.print_log()




        self.loggerObj.debug("finished adding screen saver video")



        # get buttons anmes from modules dict
        self.current_start_module_buttons = 1
        self.max_buttons = 4

        # get buttons list
        self.module_buttons_data = self.make_module_buttons()

        # generate buttons in modules_button_grid
        self.generate_module_buttons()


        # connect prev and next button
        self.pushButton_2.pressed.connect(self.press_arrow_button_next)
        self.pushButton.pressed.connect(self.press_arrow_button_prev)


        # connect those 4 module buttons
        self.pushButton_3.pressed.connect(lambda: self.press_module_button(self.pushButton_3))
        self.pushButton_4.pressed.connect(lambda: self.press_module_button(self.pushButton_4))
        self.pushButton_5.pressed.connect(lambda: self.press_module_button(self.pushButton_5))
        self.pushButton_6.pressed.connect(lambda: self.press_module_button(self.pushButton_6))



        # add graph canvas
        self.graphWidget = pyqtgraph.PlotWidget()
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.graphWidget.hideAxis('bottom')
        self.graphWidget.hideAxis('left')
        self.graphWidget.setBackground('#000000')    
        self.graphWidget_pen = pyqtgraph.mkPen(color=(82, 5, 255))
    

        # adding canvas to the layout
        self.gridLayout_2.addWidget(self.graphWidget)

        self.sleep_time = 1
        self.valueQueue = deque()
        self.valueQueue_size = 10

        for i in range(self.valueQueue_size):
            self.valueQueue.append(random.random())

        self.plotTimer = QtCore.QTimer()
        self.plotTimer.timeout.connect(self.showPlot)
        self.plotTimer.start(1000)

        X_Y_Spline_temp = make_interp_spline(range(len(self.valueQueue)) , self.valueQueue)
 
        # Returns evenly spaced numbers
        # over a specified interval.
        X_Temp = numpy.linspace(0, len(self.valueQueue)-1, 500)
        Y_Temp = X_Y_Spline_temp(X_Temp)

        self.graphWidget_line = self.graphWidget.plot(X_Temp , Y_Temp ,  pen=self.graphWidget_pen)

        self.loggerObj.debug("finished custom ui setup")
        self.print_log()






    def showPlot(self):
        self.graphWidget_line.clear()
        X_Y_Spline = make_interp_spline(range(len(self.valueQueue)) , self.valueQueue)
 
        # Returns evenly spaced numbers
        # over a specified interval.
        X = numpy.linspace(0, len(self.valueQueue)-1, 500)
        Y = X_Y_Spline(X)

        self.graphWidget_line = self.graphWidget.plot(X , Y ,  pen=self.graphWidget_pen)

        self.valueQueue.popleft()
        self.valueQueue.append(random.random())







    def closeEvent(self, event):
        self.loggerObj.info("existing jarvis")
        self.print_log()

        del self.dialogBox_storage 

        


    

    # make button list from modules list
    def make_module_buttons(self):
        self.loggerObj.debug("make module buttons")
        self.print_log()

        buttonsList = []

        # get button names from modules dict
        for i in GlobalLists.modules_list:
            buttonsList.append(i)


        # make the 4 modulus 0
        if((len(buttonsList) % self.max_buttons) != self.max_buttons):
            for i in range(self.max_buttons - (len(buttonsList) % self.max_buttons)):
                buttonsList.append("Comming\nSoon")

        return buttonsList
















    # method to generate buttons in buttonList
    def generate_module_buttons(self , start = 1):
        self.loggerObj.debug("generating module buttons")
        self.print_log()

        # method to set the button state based on name
        def setButtonName(name , buttonObj):
            if(name == "Comming\nSoon"):
                buttonObj.setText(name)
                buttonObj.setDisabled(True)
                buttonObj.setStyleSheet("background-color: rgb(55, 0, 179);\n"
                "color: rgba(238, 238, 236 , 50);\n"
                "font: 85 24pt \"FreeSans\";\n"
                "\n"
                "")
            else:
                buttonObj.setText(name)
                buttonObj.setEnabled(True)
                buttonObj.setStyleSheet("background-color: rgb(55, 0, 179);\n"
                "color: rgb(238, 238, 236);\n"
                "font: 85 24pt \"FreeSans\";\n"
                "\n"
                "")


        # set names for all four buttons
        module_name =  self.module_buttons_data[start - 1]
        setButtonName(module_name , self.pushButton_3)

        module_name =  self.module_buttons_data[start]
        setButtonName(module_name , self.pushButton_4)

        module_name =  self.module_buttons_data[start + 1]
        setButtonName(module_name , self.pushButton_5)

        module_name =  self.module_buttons_data[start + 2]
        setButtonName(module_name , self.pushButton_6)
            
        self.current_start_module_buttons = start

        self.loggerObj.debug("finished generating module buttons")
        self.print_log()
        












    # method to define what happens when the next button is pressed
    def press_arrow_button_next(self):
        self.loggerObj.debug("next button pressed")
        self.print_log()

        self.animate_button_press(self.pushButton_2)

        # 1. enable the prev_arrow_button
        self.pushButton.setEnabled(True)
        self.pushButton.setStyleSheet("background-color: rgb(55, 0, 179);\n"
        "color: rgb(238, 238, 236);\n"
        "font: 85 24pt \"FreeSans\";\n"
        "\n"
        "\n"
        "border-image: url(:/newPrefix/prev_button.svg);")

        # if the end at which the modules_button_grid is current in is greator than the length of buttons list
        # then disable the button
        if((self.current_start_module_buttons + 4) >= (len(self.module_buttons_data) - 1)):
            self.pushButton_2.setDisabled(True)
            self.pushButton_2.setStyleSheet("background-color: rgb(46, 52, 54);\n"
            "color: rgb(238, 238, 236);\n"
            "font: 85 24pt \"FreeSans\";\n"
            "\n"
            "\n"
            "border-image: url(:/newPrefix/next_button.svg);")

            self.loggerObj.info("No more modules can't go further")
            self.print_log()
            return None

        # else update the module buttons
        self.generate_module_buttons(start = self.current_start_module_buttons + 4)
    



















    # method to define what happends when the prev button is pressed
    def press_arrow_button_prev(self):

        self.loggerObj.debug("prev button pressed")
        self.print_log()

        self.animate_button_press(self.pushButton)

        # 1. enable the next_arrow_button
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setStyleSheet("background-color: rgb(55, 0, 179);\n"
        "color: rgb(238, 238, 236);\n"
        "font: 85 24pt \"FreeSans\";\n"
        "\n"
        "\n"
        "border-image: url(:/newPrefix/next_button.svg);")

        # if the end at which the modules_button_grid is current in is greator than the length of buttons list
        # then disable the button

        if(self.current_start_module_buttons <= 1):
            self.pushButton.setDisabled(True)
            self.pushButton.setStyleSheet("background-color: rgb(46, 52, 54);\n"
            "color: rgb(238, 238, 236);\n"
            "font: 85 24pt \"FreeSans\";\n"
            "\n"
            "\n"
            "border-image: url(:/newPrefix/prev_button.svg);")

            self.loggerObj.info("no more modules can't go back")
            self.print_log()
            return None

        # else update the module buttons
        self.generate_module_buttons(start = self.current_start_module_buttons - 4)
    




    




    # function to animate the button press
    def animate_button_press(self , buttonObj):
        self.loggerObj.debug("animating button pressed invoked")
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


    





    # method to define when one of the module button is pressed
    def press_module_button(self , buttonObj):

        self.loggerObj.debug("module button pressed")
        self.print_log()

        self.animate_button_press(buttonObj)

        Form = QtWidgets.QDialog()

        self.loggerObj.info(f"opening {buttonObj.text()} module")
        self.print_log()
        
        if(buttonObj.text() == "Password\nmanager"):

            dbPath = self.settingsDict.get("password_db_path" , "")

            if(dbPath == ""):
                if(GlobalData_main.isOnLinux):
                    dbPath = pathlib.Path(GlobalData_main.folderPathLinux , "password.db").absolute()
                else:
                    dbPath = pathlib.Path(GlobalData_main.folderPathWindows , "password.db").absolute()

            else:
                if(not(pathlib.Path(dbPath).absolute().is_file())):
                    self.showErrorDialog(f"no db found at {dbPath} , check path in settings or clear it to make new db")
                    return


            ui = PasswordMainWidget(dbPath , self.loggerObj_store)

            if(ui.continueSetup):
                ui.setupUi(Form)
                Form.show()
            else:
                self.loggerObj.info("existing password manager")
                self.print_log()

                del ui
                del Form
                return


        elif(buttonObj.text() == "Settings"):

            ui = SettingsMainWidget(self.settingsPath , self.loggerObj_store)
            ui.setupUi(Form)
            Form.show()
            Form.exec()

            self.settingsDict = ui.settingsDict





        elif(buttonObj.text() == "FTP\nserver"):

            ftp_port = self.settingsDict.get("ftp_port")
            ftp_username = self.settingsDict.get("ftp_username")
            ftp_password = self.settingsDict.get("ftp_password")
            ftp_default_folder = self.settingsDict.get("ftp_default_folder")
            ftp_anonymous = self.settingsDict.get("ftp_anonymous")

            ui = FTPServerMainWidget(self.loggerObj_store , ftp_port , ftp_username , ftp_password , ftp_default_folder , ftp_anonymous)
            ui.setupUi(Form)
            Form.show()
            Form.exec()
        

        self.dialogBox_storage[buttonObj.text()] = [ui , Form]


        









    
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
    ui = MainScreenWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
