# essential modules
import os
import platform
import time
import sys
from threading import Thread
import multiprocessing
import sys
import pathlib
import logging
from ui.packages.globalData.globalDataClasses import GlobalData_main









# Checking the users operating system and adding data to global class
osUsing = platform.system()

if(osUsing == "Linux"):
    GlobalData_main.isOnLinux = True
    
    if(sys.argv[0].find(".py") != -1):
        GlobalData_main.folderPathLinux = os.getcwd() + "/JarvisData"
        GlobalData_main.loggerLevel = logging.DEBUG
    else:
        GlobalData_main.folderPathLinux = pathlib.Path("/opt/JarvisData").absolute()

    # making the program data folder
    try:
        os.mkdir(GlobalData_main.folderPathLinux)
    except FileExistsError:
        pass
    except PermissionError:
        print("\nPlease run jarvis using sudo")
        sys.exit()


elif(osUsing == "Windows"):
    GlobalData_main.isOnWindows = True

    # making the program data folder
    try:
        os.mkdir(GlobalData_main.folderPathWindows)
    except FileExistsError:
        pass

else:
    print("Jarvis currently does not support this operating system :(")
    time.sleep(3)
    sys.exit()

del osUsing





# loading animation thread
class LoadingAnimation(Thread):

    def run(self):

        string = ""

        # will run only till max 5 times or early if the global var runLoadingAnimation is made false
        while(GlobalData_main.runLoadingAnimation and GlobalData_main.loadingAnimationCount):
            string = string + "."
            time.sleep(0.5)
            print("\rloading , please wait " , string , end = "")
            GlobalData_main.loadingAnimationCount -= 1

        print()




from ui.packages.log_module.logger import Logger


# starting in the main to avoide awakeness by sub processes
if __name__ == "__main__":
    multiprocessing.freeze_support()

    if(GlobalData_main.loggerLevel != logging.DEBUG):
        # loading animation thread started 
        GlobalData_main.lAnimationObj = LoadingAnimation()
        GlobalData_main.lAnimationObj.start()


if(GlobalData_main.isOnLinux):
    loggerPath = pathlib.Path(GlobalData_main.folderPathLinux , "logs.log").absolute()
else:
    loggerPath = pathlib.Path(GlobalData_main.folderPathWindows , "logs.log").absolute()

GlobalData_main.globalLogger = Logger(loggerPath , level=GlobalData_main.loggerLevel)






from PyQt5 import QtCore, QtGui, QtWidgets
from ui.m_mainScreen import MainScreenWidget as test


def handler(msg_type, msg_log_context, msg_string):

    if(msg_string == "QWidget::paintEngine: Should no longer be called"):
        pass
    else:
        GlobalData_main.globalLogger.logger_obj.warning(f"msg_type = {msg_type} , msg_log_context = {msg_log_context} , msg_string = {msg_string}")
        GlobalData_main.globalLogger.print_log()
        



if __name__ == "__main__":
    QtCore.qInstallMessageHandler(handler)
    QtWidgets.QApplication.setStyle("fusion")
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = test(GlobalData_main.globalLogger)


    if(GlobalData_main.loggerLevel != logging.DEBUG):
        # closing the loading animation
        GlobalData_main.runLoadingAnimation = False
        GlobalData_main.lAnimationObj.join()


    ui.setupUi(Form)
    Form.show()
    rc = app.exec_()

    del app
    del ui
    del Form

    sys.exit(rc)

    




