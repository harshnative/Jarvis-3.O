import pathlib
import logging


class GlobalDicts:
    pass


class GlobalLists:
    modules_list = [
        "Password\nmanager" ,
        "Settings" ,
    ]






# declaring some global variables
class GlobalData_main:

    # current version of software
    currentVersion = 0.1

    # variables to determine the operating system of the user 
    isOnWindows = False
    isOnLinux = False

    # variables to manage the loading animation 
    runLoadingAnimation = True
    loadingAnimationCount = 5
    lAnimationObj = None



    folderPathLinux = None
    folderPathWindows = pathlib.Path("C:/programData/JarvisData").absolute()

    globalLogger = None
    loggerLevel = logging.INFO



