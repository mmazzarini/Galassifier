import json

config_data = []

CONFIG_FILE_PATH = 'GalassifierServer/GalassifierServer/ML/training/Config/'
CONFIG_FILE_NAME = 'galassifier_training_config'
CONFIG_FILE_EXTENSION = '.json'

COMPLETE_CONFIG_FILE = CONFIG_FILE_PATH + CONFIG_FILE_NAME + CONFIG_FILE_EXTENSION

with open (COMPLETE_CONFIG_FILE, 'r') as config_file:
    try : 
        config_data = json.load(config_file)
    except json.decoder.JSONDecodeError as e:
        print(f"Error reading JSON configuration file: {e}")

#method to load the project configuration from a JSON file
def load_project_config():
    global config_data
    if config_data is not None:
        return config_data
    else:
        with open(COMPLETE_CONFIG_FILE, 'r') as config_file:
            try:
                config_data = json.load(config_file)
            except json.decoder.JSONDecodeError as e:
                print(f"Error reading JSON configuration file: {e}")
                return None
    return config_data

