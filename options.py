from PyQt5 import QtWidgets
import os
import json

class Options:
    def __init__(self, windowRef) -> None:
        # Check if the config file exists and is a valid json file with the correct keys
        if not os.path.exists('config.json') or not json.load(open('config.json'))['wrl_folder'] or not json.load(open('config.json'))['index_url']:
            self.windowRef = windowRef
        else:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.windowRef = windowRef
                self.windowRef.wrlFolder.setText(config['wrl_folder'])
                self.windowRef.indexUrl.setText(config['index_url'])

    def get_wrl_folder(self) -> str:
        print(self.windowRef.wrlFolder.text())
        return self.windowRef.wrlFolder.text()

    def get_index_url(self) -> str:
        return self.windowRef.indexUrl.text()

    def save(self) -> None:
        # Write the options to a json file in the user's config folder
        with open('config.json', 'w') as f:
            f.write(json.dumps({
                'wrl_folder': self.get_wrl_folder(),
                'index_url': self.get_index_url()
            }))