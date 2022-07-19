from PyQt5 import QtWidgets
import os
import platform
import json

class Options:
    def __init__(self, windowRef) -> None:
        # Check if the config file exists and is a valid json file with the correct keys
        if not os.path.exists(Options.get_platform_config_path()) or not json.load(open(Options.get_platform_config_path()))['wrl_folder'] or not json.load(open(Options.get_platform_config_path()))['index_url']:
            self.windowRef = windowRef
        else:
            with open(Options.get_platform_config_path(), 'r') as f:
                config = json.load(f)
                self.windowRef = windowRef
                self.windowRef.wrlFolder.setText(config['wrl_folder'])
                self.windowRef.indexUrl.setText(config['index_url'])

    def get_wrl_folder(self) -> str:
        print(self.windowRef.wrlFolder.text())
        return self.windowRef.wrlFolder.text()
    
    def set_wrl_folder(self, folder: str) -> None:
        self.windowRef.wrlFolder.setText(folder)

    def get_index_url(self) -> str:
        return self.windowRef.indexUrl.text()

    def save(self) -> None:
        # Write the options to a json file in the user's config folder
        with open(Options.get_platform_config_path(), 'w') as f:
            f.write(json.dumps({
                'wrl_folder': self.get_wrl_folder(),
                'index_url': self.get_index_url()
            }))
    
    def get_platform_config_prefix() -> str:
        if platform.system() == 'Windows':
            return os.environ['APPDATA']
        elif platform.system() == 'Linux':
            return os.path.join(os.environ['HOME'], '.config')
        elif platform.system() == 'Darwin':
            return os.path.join(os.environ['HOME'], 'Library', 'Application Support')
    
    def get_platform_config_path() -> str:
        # Check if the folder already exists. If not, create it.
        if not os.path.exists(os.path.join(Options.get_platform_config_prefix(), 'KISS')):
            os.mkdir(os.path.join(Options.get_platform_config_prefix(), 'KISS'))
        return os.path.join(Options.get_platform_config_prefix(), 'KISS', 'config.json')