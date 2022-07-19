from options import Options
from PyQt5 import QtWidgets, QtGui, QtCore
import os

class WrlList:
    def __init__(self, options: Options):
        # Check if the wrl folder is a valid folder
        if not os.path.exists(options.get_wrl_folder()):
            print("Invalid wrl folder, wrls will not be populated until a proper folder is selected")
            self.wrls = []
            return
        # Recursively get all .wrl files in the wrl folder with the substring "cpBureau" inside them
        self.wrls = []
        for root, dirs, files in os.walk(options.get_wrl_folder()):
            for file in files:
                if file.endswith(".wrl"):
                    try:
                        if "cpBureau" in open(os.path.join(root, file)).read():
                         self.wrls.append(os.path.join(root, file))
                    except:
                        pass
        # Sort the wrls by name
        self.wrls.sort()
        
        self.wrlFolder = options.get_wrl_folder()

    def get_wrls(self):
        return self.wrls
    
    def update_ui(self, ui):
        ui.wrlList.clear()
        for wrl in map(lambda x: x.replace(self.wrlFolder, ""), self.wrls):
            ui.wrlList.addItem(QtWidgets.QListWidgetItem(wrl))