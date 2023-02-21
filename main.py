#!/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import asyncio
import threading

from PyQt5 import QtWidgets

from Window import Ui_MainWindow
from options import Options
from userServers import UserServers
from serverIndex import setup_index_list
import vrmlUpdater
import pinger

from wrls import WrlList
from decorators import box_on_error

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

options = Options(ui)
user_servers = UserServers()

@box_on_error("Error adding server")
def add_server():
    user_servers.add_server(ui.serverInput.text(), ui.wlsToggle.isChecked())
    ui.serverInput.clear()
    user_servers.update_ui(ui)

@box_on_error("Error removing server")
def remove_server():
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

@box_on_error("Error updating wrl list")
def select_all_wrls():
    for i in range(ui.wrlList.count()):
        ui.wrlList.item(i).setSelected(True)

@box_on_error("Error updating wrl list")
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
ui.userList.itemSelectionChanged.connect(ui.indexList.clearSelection)
ui.indexList.itemSelectionChanged.connect(ui.userList.clearSelection)

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
@box_on_error("Error applying server")
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

@box_on_error("Error browsing for wrl directory")
def browse_for_wrl_directory():
    # Open a dialog to select a directory
    folder = QtWidgets.QFileDialog.getExistingDirectory(MainWindow, "Select wrl directory")
    if folder == "":
        return
    # Set the wrl folder to the selected directory
    options.set_wrl_folder(folder)

ui.browseWrlFolder.clicked.connect(browse_for_wrl_directory)


MainWindow.show()
print(pinger.ping("not.a.real.url"))

ui.applyButton.clicked.connect(apply)

# Create a thread to update the indexList and userList every few seconds
nextUpdate = time.time()
updating = True
def update_lists():
    global nextUpdate
    while updating:
        if time.time() > nextUpdate:
            nextUpdate = time.time() + 30
            user_servers.update_ui(ui)
            setup_index_list(ui, options)

            # Force the userList and the indexList to have each column be as wide as the widest item in that column
            ui.userList.resizeColumnToContents(0)
            ui.userList.resizeColumnToContents(1)
            ui.indexList.resizeColumnToContents(0)
            ui.indexList.resizeColumnToContents(1)

update_thread = threading.Thread(target=update_lists)
update_thread.start()

# When the user closes the window, stop the thread
def stop_updating(_):
    global updating
    updating = False
MainWindow.closeEvent = stop_updating

sys.exit(app.exec_())