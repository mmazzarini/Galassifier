
import numpy as np
import config

config_data = config.load_project_config()

def load_dataset_from_drive(in_loadsave_path):

    print("Reading dataset from drive...")
    data = np.load(in_loadsave_path)
    return data

def save_dataset_to_drive(in_loadsave_path, in_loaded_train_images, in_loaded_train_labels, 
                          in_loaded_val_images, in_loaded_val_labels):
    np.savez(in_loadsave_path,
             train_images=in_loaded_train_images,
             train_labels=in_loaded_train_labels,
             val_images=in_loaded_val_images,
             val_labels=in_loaded_val_labels)
    

def get_model_save_path():
    model_save_path = config_data["extensions"]["model_save_path"]
    model_save_path += config_data["extensions"]["model_save_name"]
    model_save_path += "_"
    model_save_path += config_data["extensions"]["model_version_number"]
    model_save_path += "."
    model_save_path += config_data["extensions"]["model_save_extension"]
    return model_save_path
