
"""
Photo Manager
A simple program for choosing whether or not to keep an image in a set of images.
Version 1.2

(c) 2019 Matthew Gallant
Licensed under the MIT license, check LICENSE.md for more info
"""

import sys
import os
import glob
import base64
import io
import platform
import ctypes

from shutil import copyfile

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PhotoCollectorMain(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):  

        # Init Variables
        self.currentPosition = 0     
        self.allImages = []  
        self.imageWidth = 400
        self.saveLocation = ""

        # Check If Windows Because The Menubar Takes Up Extra Space
        if (platform.system() == 'Windows'):
            self.modifier = 40
        else:
            self.modifier = 0

        # Create Windows App ID & Color Scheme
        if (platform.system() == "Windows"):
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('me.matthewgallant.photomanager')
            palette = self.palette()
            palette.setColor(self.backgroundRole(), Qt.white)
            self.setPalette(palette)
        
        # Init Menubar
        menubar = self.menuBar()

        # Init File Menu
        fileMenu = menubar.addMenu('File')

        # Load Images Action
        loadAction = QAction('Load Images', self)
        loadAction.setShortcut("Ctrl+O")
        loadAction.triggered.connect(self.loadImages)
        fileMenu.addAction(loadAction)

        # Open Information Action
        prefAction = QAction('About Photo Manager', self)
        prefAction.triggered.connect(self.openAbout)
        fileMenu.addAction(prefAction)
        

        # Init Action Menu
        actionMenu = menubar.addMenu('Action')

        # Keep Image Action
        self.keepAction = QAction('Keep Image', self)
        self.keepAction.setShortcut("Ctrl+K")
        self.keepAction.triggered.connect(self.keepImage)
        actionMenu.addAction(self.keepAction)

        # Discard Image Action
        self.discardAction = QAction('Discard Image', self)
        self.discardAction.setShortcut("Ctrl+D")
        self.discardAction.triggered.connect(self.discardImage)
        actionMenu.addAction(self.discardAction)

        # Init Action Menu
        imageMenu = menubar.addMenu('Image')

        # 400px Image Width Action
        self.fourHundredAction = QAction('400px Wide', self)
        self.fourHundredAction.setShortcut("Ctrl+1")
        self.fourHundredAction.triggered.connect(self.adjustFrameFourHundred)
        imageMenu.addAction(self.fourHundredAction)

        # 600px Image Width Action
        self.sixHundredAction = QAction('600px Wide', self)
        self.sixHundredAction.setShortcut("Ctrl+2")
        self.sixHundredAction.triggered.connect(self.adjustFrameSixHundred)
        imageMenu.addAction(self.sixHundredAction)

        # 800px Image Width Action
        self.eightHundredAction = QAction('800px Wide', self)
        self.eightHundredAction.setShortcut("Ctrl+3")
        self.eightHundredAction.triggered.connect(self.adjustFrameEightHundred)
        imageMenu.addAction(self.eightHundredAction)

        # 1000px Image Width Action
        self.oneThousandAction = QAction('1000px Wide', self)
        self.oneThousandAction.setShortcut("Ctrl+4")
        self.oneThousandAction.triggered.connect(self.adjustFrameOneThousand)
        imageMenu.addAction(self.oneThousandAction)

        # 1200px Image Width Action
        self.twelveHundredAction = QAction('1200px Wide', self)
        self.twelveHundredAction.setShortcut("Ctrl+5")
        self.twelveHundredAction.triggered.connect(self.adjustFrameTwelveHundred)
        imageMenu.addAction(self.twelveHundredAction)

        # Disable Button Until Image Load
        self.disableMenuItems()

        # Build Window
        if (platform.system() == "Windows"):
            self.resize(800, 200)
        elif (platform.system() == "Darwin"):
            self.resize(400, 100)
        else:
            self.resize(600, 300)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Image Window
        self.imageLabel = QLabel(centralWidget)

        # Open Folder Text Label
        self.loadLabel = QLabel(centralWidget)
        self.loadLabel.setText('Please Open An Image Folder')
        self.loadLabel.adjustSize()

        # Get Frame Information
        x1 = self.frameGeometry().width()
        y1 = self.frameGeometry().height()
        x2 = self.loadLabel.frameGeometry().width()
        y2 = self.loadLabel.frameGeometry().height()

        if (platform.system() == 'Darwin'):
            self.loadLabel.move((x1 / 2) - (x2 / 2), (y1 / 2) - (y2 / 2) - 12)
        elif (platform.system() == 'Windows'):
            self.loadLabel.move(250, self.modifier + 70)
        else:
            self.loadLabel.move(215, 125)

        # Init Window Settings
        self.centerWindow()
        self.setWindowTitle('Photo Manager')    
        self.show()

    def loadImages(self):

        # Show Info
        QMessageBox.information(self, 'Choose Photos', "In The Next Window, Please Choose The Folder With The Photos You Wish To Sort.", QMessageBox.Ok)
        
        # Open File Dialog
        folderName = QFileDialog.getExistingDirectory(self, 'Open Images Folder')

        # Check If Folder Was Selected
        if (folderName != ""):

            # Collect Image Names
            self.allImages = []

            # Collect JPEGs
            jpegs = glob.glob(folderName + "/*.jpeg")
            for image in jpegs:
                self.allImages.append(image)

            # Collect JPEGs
            jpegs = glob.glob(folderName + "/*.JPEG")
            for image in jpegs:
                self.allImages.append(image)

            # Collect JPGs
            jpgs = glob.glob(folderName + "/*.jpg")
            for image in jpgs:
                self.allImages.append(image)

            # Collect JPGs
            jpgs = glob.glob(folderName + "/*.JPG")
            for image in jpgs:
                self.allImages.append(image)

            # Collect PNGs
            pngs = glob.glob(folderName + "/*.png")
            for image in pngs:
                self.allImages.append(image)

            # Collect PNGs
            pngs = glob.glob(folderName + "/*.PNG")
            for image in pngs:
                self.allImages.append(image)

            if (len(self.allImages) > 0):

                # Show Info
                QMessageBox.information(self, 'Choose Destination', "In The Next Window, Please Choose Where To Save The Sorted Photos.", QMessageBox.Ok)
                
                # Open File Dialog
                destinationName = QFileDialog.getExistingDirectory(self, 'Open Destination Folder')

                # Check If Folder Was Selected
                if (destinationName != ""):

                    # Create Folders
                    if(os.path.exists(destinationName + "/Keep") or os.path.exists(destinationName + "/Discard")):
                        QMessageBox.information(self, 'Save Location Already Exists', "Please Delete The 'Keep' and 'Discard' Directories To Continue.", QMessageBox.Ok)
                    else:

                        # Set Save Location
                        self.saveLocation = destinationName

                        # Create Save Directories
                        os.makedirs(destinationName + "/Keep")
                        os.makedirs(destinationName + "/Discard")

                        # Load Image Into Window
                        self.currentPosition = 0
                        self.updateImage(self.allImages[self.currentPosition])

                        # Adjust Window Settings
                        self.loadLabel.setVisible(False)

                        # Adjust Menu Settings
                        self.enableMenuItems()

            else:
                QMessageBox.information(self, 'No Images Found', "No Images Found in Folder", QMessageBox.Ok)

    def updateImage(self, imageLocation):
        self.loadedImage = QPixmap(imageLocation).scaledToWidth(self.imageWidth, mode=Qt.SmoothTransformation)
        self.imageLabel.setPixmap(self.loadedImage)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.adjustSize()
        self.resize(self.imageWidth, self.loadedImage.size().height() + self.modifier)
        self.imageLabel.move(0, self.modifier)
        self.centerWindow()
        
    def centerWindow(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def keepImage(self):
        
        # Keep Image
        copyfile(self.allImages[self.currentPosition], self.saveLocation + "/Keep/" + os.path.basename(self.allImages[self.currentPosition]))

        # Update Image Window
        if (self.currentPosition + 1 <= len(self.allImages) - 1):
            self.currentPosition += 1
            self.updateImage(self.allImages[self.currentPosition])
        else:
            QMessageBox.information(self, 'End of Images', "End of Images", QMessageBox.Ok)
            self.resetMainWindow()

    def discardImage(self):

        # Discard Image
        copyfile(self.allImages[self.currentPosition], self.saveLocation + "/Discard/" + os.path.basename(self.allImages[self.currentPosition]))

        # Update Image Window
        if (self.currentPosition + 1 <= len(self.allImages) - 1):
            self.currentPosition += 1
            self.updateImage(self.allImages[self.currentPosition])
        else:
            QMessageBox.information(self, 'End of Images', "End of Images", QMessageBox.Ok)
            self.resetMainWindow()
    
    def openAbout(self):
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()

    def adjustFrameFourHundred(self):
        self.imageWidth = 400
        self.updateImage(self.allImages[self.currentPosition])

    def adjustFrameSixHundred(self):
        self.imageWidth = 600
        self.updateImage(self.allImages[self.currentPosition])

    def adjustFrameEightHundred(self):
        self.imageWidth = 800
        self.updateImage(self.allImages[self.currentPosition])

    def adjustFrameOneThousand(self):
        self.imageWidth = 1000
        self.updateImage(self.allImages[self.currentPosition])

    def adjustFrameTwelveHundred(self):
        self.imageWidth = 1200
        self.updateImage(self.allImages[self.currentPosition])
        
    def enableMenuItems(self):
        self.keepAction.setDisabled(False)
        self.discardAction.setDisabled(False)

        self.fourHundredAction.setDisabled(False)
        self.sixHundredAction.setDisabled(False)
        self.eightHundredAction.setDisabled(False)
        self.oneThousandAction.setDisabled(False)
        self.twelveHundredAction.setDisabled(False)

    def disableMenuItems(self):
        self.keepAction.setDisabled(True)
        self.discardAction.setDisabled(True)

        self.fourHundredAction.setDisabled(True)
        self.sixHundredAction.setDisabled(True)
        self.eightHundredAction.setDisabled(True)
        self.oneThousandAction.setDisabled(True)
        self.twelveHundredAction.setDisabled(True)

    def resetMainWindow(self):
        if (platform.system() == "Windows"):
            self.resize(800, 200)
        elif (platform.system() == "Darwin"):
            self.resize(400, 100)
        else:
            self.resize(600, 300)
        
        self.centerWindow()
            
        self.loadLabel.setVisible(True)
        self.imageLabel.clear()
        self.disableMenuItems()

class AboutWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):


        # Logo Image
        b64_data = "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"
        
        # Create Window Objects
        if (platform.system() == "Windows"):
            palette = self.palette()
            palette.setColor(self.backgroundRole(), Qt.white)
            self.setPalette(palette)
            self.setFixedSize(400, 550)
        else:
            self.setFixedSize(300, 300)

        self.setWindowTitle('About Photo Manager')

        # Create Universal Variables
        self.titleFont = QFont("Helvetica", 35, QFont.Bold) 
        self.subtitleFont = QFont("Helvetica", 20, QFont.Normal) 

        # Welcome Title Label
        self.titleLabel = QLabel("Photo Manager")
        self.titleLabel.setFont(self.subtitleFont)
        self.titleLabel.setAlignment(Qt.AlignCenter)

        # Create Logo Image
        self.imageLabel = QLabel(self)
        self.logoImage = QPixmap()
        self.logoImage.loadFromData(base64.b64decode(b64_data))
        self.logoImage = self.logoImage.scaled(150, 150, transformMode = Qt.SmoothTransformation)
        self.imageLabel.setPixmap(self.logoImage)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        # Get OS Text
        if (platform.system() == "Windows"):
            osInfo = "Windows"
        elif (platform.system() == "Darwin"):
            osInfo = "macOS"
        elif (platform.system() == "Linux"):
            osInfo = "Linux"
        else:
            osInfo = "Unknown OS"

        # Create Text Field Titles
        self.versionLabel = QLabel("Version 1.2 (" + osInfo + ")")
        self.copyrightLabel = QLabel("<a href='https://matthewgallant.me'>\u00A9 2020 Matthew Gallant</a>")

        self.versionLabel.setAlignment(Qt.AlignCenter)
        self.copyrightLabel.setAlignment(Qt.AlignCenter)

        self.copyrightLabel.setOpenExternalLinks(True)

        # Create Buttons
        self.closeButton = QPushButton('Close', self)

        # Create Button Actions
        self.closeButton.clicked.connect(self.quitProgram)

        # Create our Containers to Hold our Components
        self.vboxLayout = QVBoxLayout()

        # Add Items to VBox
        self.vboxLayout.addWidget(self.imageLabel)
        self.vboxLayout.addWidget(self.titleLabel)
        self.vboxLayout.addWidget(self.versionLabel)
        self.vboxLayout.addWidget(self.copyrightLabel)
        self.vboxLayout.addWidget(self.closeButton)

        self.setLayout(self.vboxLayout)        
        self.show()

    def quitProgram(self):
       self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhotoCollectorMain()
    
    # Set Window Icon On Windows
    if (platform.system() == "Windows"):
    
        # Get Current Folder
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        elif __file__:
            application_path = os.path.dirname(__file__)
        
        # Get Image File
        icon_image = os.path.join(application_path, 'icon.ico')

        # Set Image File
        app.setWindowIcon(QIcon(icon_image))
        ex.setWindowIcon(QIcon(icon_image))
    
    sys.exit(app.exec_())
