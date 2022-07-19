import os
import json
from PyQt5 import QtWidgets

class UserServers:
    def __init__(self):
        # Check if the config file exists and is a valid json file with a top level array named servers
        try:
            empty = not os.path.exists('config.json') or not json.load(open('servers.json'))['servers']
        except:
            empty = True
        if empty:
            self.servers = []
        else:
            with open('servers.json', 'r') as f:
                config = json.load(f)
                self.servers = config['servers']
    def save(self):
        # Write the options to a json file in the user's config folder
        with open('servers.json', 'w') as f:
            f.write(json.dumps({
                'servers': self.servers
            }))
    def add_server(self, url, wls):
        self.servers.append({
            'url': url,
            'wls': wls
        })
        self.save()
    
    def remove_server(self, index):
        self.servers.pop(index)
        self.save()
        return self.servers

    def get_servers(self):
        return self.servers
    
    def get_server(self, index):
        return self.servers[index]
    
    def update_ui(self, ui):
        ui.userList.clear()
        for server in self.servers:
            ui.userList.addTopLevelItem(QtWidgets.QTreeWidgetItem([server['url'], "Yes" if server['wls'] else "No"]))