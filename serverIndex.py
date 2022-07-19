import requests
from options import Options
from PyQt5 import QtCore, QtGui, QtWidgets

def get_index(url):
    try:
        response = requests.get(url)
    except:
        print("Could not connect to index server!")
        return []
    # Parse the response as JSON
    json = response.json()
    # Check if the response is a valid iterable
    try:
        _ = iter(json)
    except:
        print("Got invalid response from server")
        return []
    # Check if each entry in the array has at least the key "url" and "wls"
    for entry in json:
        if not entry.get('url') or not type(entry.get('wls')) == bool:
            print("Not all entries are correct")
            return []
    return json

def setup_index_list(ui, options: Options):
    # Get the index from the server
    index = get_index(options.get_index_url())

    ui.indexList.clear()
    # Add each entry to the list
    for entry in index:
        ui.indexList.addTopLevelItem(QtWidgets.QTreeWidgetItem([entry['url'], "Yes" if entry['wls'] else "No"]))