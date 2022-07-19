#!/bin/env python
from Window import Ui_MainWindow
from options import Options
from userServers import UserServers
from serverIndex import get_index, setup_index_list
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import vrmlUpdater

from wrls import WrlList

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

options = Options(ui)
user_servers = UserServers()

def add_server():
    global user_servers
    user_servers.add_server(ui.serverInput.text(), ui.wlsToggle.isChecked())
    ui.serverInput.clear()
    user_servers.update_ui(ui)

def remove_server():
    global user_servers
    getSelected = ui.userList.selectedItems()
    if getSelected:
        user_servers.remove_server(ui.userList.indexOfTopLevelItem(getSelected[0]))
        user_servers.update_ui(ui)

wrl_list = WrlList(options)
wrl_list.update_ui(ui)
def update_wrl_list():
    wrl_list.__init__(options)
    wrl_list.update_ui(ui)
options.onSaveCallbacks.append(update_wrl_list)

def select_all_wrls():
    for i in range(ui.wrlList.count()):
        ui.wrlList.item(i).setSelected(True)

def deselect_all_wrls():
    for i in range(ui.wrlList.count()):
        ui.wrlList.item(i).setSelected(False)

ui.selectAll.clicked.connect(select_all_wrls)
ui.deselectAll.clicked.connect(deselect_all_wrls)

setup_index_list(ui, options)
options.onSaveCallbacks.append(lambda: setup_index_list(ui, options))
user_servers.update_ui(ui)

# Only allow one entry to be selected between the two lists (userList and indexList)
ui.userList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
ui.indexList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

# If the user selects an entry in one of the two lists, deselect the other list
ui.userList.itemSelectionChanged.connect(lambda: ui.indexList.clearSelection())
ui.indexList.itemSelectionChanged.connect(lambda: ui.userList.clearSelection())

# Make selecting wrls in the wrlList be a toggle
ui.wrlList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

ui.saveButton.clicked.connect(options.save)
ui.serverAdd.clicked.connect(add_server)
ui.serverRemove.clicked.connect(remove_server)

def get_wrl_full_path(wrl_name: str):
    if wrl_name.startswith("/") or wrl_name.startswith("\\"):
        wrl_name = wrl_name[1:]
    return os.path.join(options.get_wrl_folder(), wrl_name)

def get_selected_server():
    # Check if the selected server is in the userList or indexList
    if ui.userList.selectedItems():
        return {
            'url': ui.userList.selectedItems()[0].text(0),
            'wls': ui.userList.selectedItems()[0].text(1) == "Yes"
        }
    elif ui.indexList.selectedItems():
        return {
            'url': ui.indexList.selectedItems()[0].text(0),
            'wls': ui.indexList.selectedItems()[0].text(1) == "Yes"
        }

def apply():
   # Make sure the user has selected a server and at least one wrl
    if not get_selected_server() or not ui.wrlList.selectedItems():
        QtWidgets.QMessageBox.warning(MainWindow, "Error", "You must select a server and at least one wrl.")
        return
    wrls_to_apply = ui.wrlList.selectedItems()
    for wrl in wrls_to_apply:
        vrmlUpdater.set_server(get_wrl_full_path(wrl.text()), get_selected_server()["url"], get_selected_server()["wls"])

    # Display a message box to tell the user that the wrls have been applied
    QtWidgets.QMessageBox.information(MainWindow, "VRML Updater", "Server changed to " + get_selected_server()["url"] + " for " + str(len(wrls_to_apply)) + " wrls")
    # Clear the selection of the user for everything
    ui.userList.clearSelection()
    ui.indexList.clearSelection()
    ui.wrlList.clearSelection()

def browse_for_wrl_directory():
    # Open a dialog to select a directory
    options.set_wrl_folder(QtWidgets.QFileDialog.getExistingDirectory(MainWindow, "Select wrl directory"))

ui.browseWrlFolder.clicked.connect(browse_for_wrl_directory)

MainWindow.show()

ui.applyButton.clicked.connect(apply)

sys.exit(app.exec_())