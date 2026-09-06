import json

config_data = []

with open ('GalassifierServer/GalassifierServer/ML/training/config/galassifier_training_config.json', 'r') as config_file:
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
        with open('GalassifierServer/GalassifierServer/ML/training/config/galassifier_training_config.json', 'r') as config_file:
            try:
                config_data = json.load(config_file)
            except json.decoder.JSONDecodeError as e:
                print(f"Error reading JSON configuration file: {e}")
                return None
    return config_data

