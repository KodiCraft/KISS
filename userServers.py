import os
import json
from PyQt5 import QtWidgets
from options import Options
from pinger import ping
import threading

class UserServers:
    def __init__(self):
        # Check if the config file exists and is a valid json file with a top level array named servers
        try:
            empty = not os.path.exists(UserServers.get_platform_server_path()) or not json.load(open(UserServers.get_platform_server_path()))['servers']
        except:
            empty = True
        if empty:
            self.servers = []
        else:
            with open(UserServers.get_platform_server_path(), 'r') as f:
                config = json.load(f)
                self.servers = config['servers']
    def save(self):
        # Write the options to a json file in the user's config folder
        with open(UserServers.get_platform_server_path(), 'w') as f:
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
            ui.userList.addTopLevelItem(QtWidgets.QTreeWidgetItem([server['url'], "Yes" if server['wls'] else "No", "Pinging..."]))
            # Start a thread to ping each server and update the list
            def ping_server(item):
                pingval = ping(item.text(0))
                if pingval == -1:
                    item.setText(2, "Offline")
                else:
                    item.setText(2, str(pingval) + "ms")
            threading.Thread(target=ping_server, args=(ui.indexList.topLevelItem(ui.indexList.topLevelItemCount() - 1),)).start()
    

    def get_platform_server_path():
        # Check if the folder already exists. If not, create it.
        if not os.path.exists(os.path.join(Options.get_platform_config_prefix(), 'KISS')):
            os.mkdir(os.path.join(Options.get_platform_config_prefix(), 'KISS'))
        return os.path.join(Options.get_platform_config_prefix(), 'KISS', 'servers.json')
