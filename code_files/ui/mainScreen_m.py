from rawUiFiles import mainScreen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia, QtMultimediaWidgets
import sys 
import os







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















class newUIForm(QtWidgets.QWidget , mainScreen.Ui_Form):

    def __init__(self, parent=None):
        
        # calling the parent init
        super(newUIForm, self).__init__(parent)







    def setupUi(self, Form):

        self.Form = Form
        # calling the parent setupUi
        super().setupUi(Form)

        self.mediaPlayer = QtMultimedia.QMediaPlayer()

        self.videoWidget = QtMultimediaWidgets.QVideoWidget()
    
        self.gridLayout_2.addWidget(self.videoWidget)

        self.mediaPlayer.stateChanged.connect(self.repeatVideo)

        self.start_video()


    



    def start_video(self):
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        # self.mediaPlayer.setMedia(QtMultimedia.QMediaContent())
        self.mediaPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(resource_path("combined_assests/jarvis_screen_saver.mp4"))))
        self.mediaPlayer.play()





    def repeatVideo(self):
        if(self.mediaPlayer.state() == 0):
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()










if __name__ == "__main__":


    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = newUIForm()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
