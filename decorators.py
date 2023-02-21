from Window import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
import functools
import traceback
import sys

def box_on_error(title):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("args: " + str(args))
            
            try:
                if isinstance(args[0], bool):
                    return func(*args[1:], **kwargs)
                return func(*args, **kwargs)
            except Exception as e:
                box = QtWidgets.QMessageBox()
                box.setWindowTitle(title)
                box.setIcon(QtWidgets.QMessageBox.Critical)
                box.setText(str(e) + " at " + func.__name__
                            + "\nPlease report this to me on GitHub or Discord with as much detail as possible\n")
                details = "Exception: " + str(e)
                details += "\nFunction: " + func.__name__
                details += "\nFile: " + func.__code__.co_filename
                details += "\nOS: " + sys.platform
                details += "\nPython version: " + sys.version
                details += "\nPyQt version: " + QtCore.PYQT_VERSION_STR
                details += "\nQt version: " + QtCore.QT_VERSION_STR
                details += "\nTraceback: " + traceback.format_exc()
                
                box.setDetailedText(details)
                
                def close():
                    box.close()
                button = box.addButton("Close", QtWidgets.QMessageBox.AcceptRole)
                button.clicked.connect(close)
                
                box.setDefaultButton(button)
                
                box.exec_()
                
        return wrapper
    return decorator
