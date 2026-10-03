
import numpy as np
import config
import json

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

#simple valdation evaluation filesave (JSON format for portability)
def save_validation_evaluation(file_path, evaluation_data):

    data = {
        "classes" : config_data["classification"]["classes"],
        
        "val_confusion_matrix" : evaluation_data["evaluation_validation"]["matrix"].tolist(),
        "val_correct_predictions" : evaluation_data["evaluation_validation"]["val_correct_predictions"],
        "val_predictions_accuracy" : evaluation_data["evaluation_validation"]["val_predictions_accuracy"],
        "val_correct_predictions_per_class" : evaluation_data["evaluation_validation"]["val_correct_predictions_per_class"].tolist(),
        "val_accuracy_per_class" : evaluation_data["evaluation_validation"]["val_accuracy_per_class"].tolist(),
        "val_num_samples" : evaluation_data["evaluation_validation"]["num_samples"],
        "rows" : "true",
        "cols" : "preds"
    }

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)