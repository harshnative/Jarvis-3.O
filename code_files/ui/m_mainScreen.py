from typing import _SpecialForm
from .rawUiFiles.mainScreen_fol import mainScreen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys 
import os
import time
from .packages.globalData.globalDataClasses import GlobalDicts
import logging
from .packages.log_module.logger import Logger












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

        self.loggerObj = loggerObj.logger_obj
        self.print_log = loggerObj.print_log

        self.loggerObj.debug("finished object init")
        self.print_log()















    def setupUi(self, Form):

        self.Form = Form

        # calling the parent setupUi
        super().setupUi(Form)

        self.loggerObj.debug("finished parent ui setup")
        self.print_log()


        # setup video player
        self.mediaPlayer = QtMultimedia.QMediaPlayer()

        self.videoWidget = QtMultimediaWidgets.QVideoWidget()
    
        # add video player to grid layout
        self.gridLayout_2.addWidget(self.videoWidget)

        # see when the video ends
        self.mediaPlayer.stateChanged.connect(self.repeatVideo)

        # start video
        self.start_video()

        self.loggerObj.info("finished adding screen saver video")



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


        self.loggerObj.debug("finished custom ui setup")
        self.print_log()






    

    # make button list from modules list
    def make_module_buttons(self):
        self.loggerObj.debug("make module buttons")
        self.print_log()

        buttonsList = []

        # get button names from modules dict
        for i in GlobalDicts.modules_dict.keys():
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

        self.animate_button_press(buttonObj)

        self.loggerObj.info(f"opening {buttonObj.text()} module")
        self.print_log()












    # method to start video playback for the first time
    def start_video(self):
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        # self.mediaPlayer.setMedia(QtMultimedia.QMediaContent())
        self.mediaPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(resource_path("combined_assests/jarvis_screen_saver.mp4"))))
        self.mediaPlayer.play()

        self.loggerObj.debug("video started")
        self.print_log()








    # method to re play the video when the video ends
    def repeatVideo(self):
        if(self.mediaPlayer.state() == 0):
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()
                    
            self.loggerObj.debug("video restarted")
            self.print_log()











if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MainScreenWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
