import json
import config

def release_model_contract(history):

    config_data = config.load_project_config()
    models_root = config_data["storage"]["storage_root"] + config_data["storage"]["model_root"]
    CONTRACT_FILE_PATH = models_root + config_data["run"]["run_foldername"]
    CONTRACT_FILE_VERSION = config_data["run"]["run_version_number"]
    CONTRACT_FILE_PATH += str(CONTRACT_FILE_VERSION)
    CONTRACT_FILE_NAME = config_data["run"]["run_model_contract_name"]
    CONTRACT_FILE_EXTENSION = config_data["run"]["run_artifact_extension"]

    if history is None:
        print("No training history available. Cannot release model contract.")
        return
    if not hasattr(history, 'history'):
        print("Training history does not have 'history' attribute. Cannot release model contract.")
        return
    model_history = history.history

    contract_dict = {
        "version": config_data["run"]["run_version_number"],
        #now some stuff about the model itself, architecture, params etc
        "model_input_size" : config_data["model"]["input_image_size"],
        "model_rgb_input" : config_data["model"]["use_rgb_input"],
        "classification" : config_data["classification"]
    }

    contract_file_path = f"{CONTRACT_FILE_PATH}/{CONTRACT_FILE_NAME}" + str(CONTRACT_FILE_VERSION) + f".{CONTRACT_FILE_EXTENSION}"

    with open(contract_file_path, "w") as f:
        json.dump(contract_dict, f)



def release_model_metrics(history):

    config_data = config.load_project_config()
    models_root = config_data["storage"]["storage_root"] + config_data["storage"]["model_root"]
    METRICS_FILE_PATH = models_root + config_data["run"]["run_foldername"]
    METRICS_FILE_VERSION = config_data["run"]["run_version_number"]
    METRICS_FILE_PATH += str(METRICS_FILE_VERSION)
    METRICS_FILE_NAME = config_data["run"]["run_model_metrics_name"]
    METRICS_FILE_EXTENSION = config_data["run"]["run_artifact_extension"]

    if history is None:
        print("No training history available. Cannot release model contract.")
        return
    if not hasattr(history, 'history'):
        print("Training history does not have 'history' attribute. Cannot release model contract.")
        return
    model_history = history.history

    metrics_dict = {

        "loss": model_history["loss"],
        "accuracy": model_history["accuracy"],
        "val_loss": model_history["val_loss"] if "val_loss" in model_history else None,
        "val_accuracy": model_history["val_accuracy"] if "val_accuracy" in model_history else None,

        #write down final values for quick reference
        "final_loss" : model_history["loss"][-1],
        "final_accuracy" : model_history["accuracy"][-1],
        "final_val_loss" : model_history["val_loss"][-1] if "val_loss" in model_history else None,
        "final_val_accuracy" : model_history["val_accuracy"][-1] if "val_accuracy" in model_history else None,
        "best_val_loss" : min(model_history["val_loss"]) if "val_loss" in model_history else None,
        "best_val_accuracy" : max(model_history["val_accuracy"]) if "val_accuracy" in model_history else None


    }

    metrics_file_path = f"{METRICS_FILE_PATH}/{METRICS_FILE_NAME}" + str(METRICS_FILE_VERSION) + f".{METRICS_FILE_EXTENSION}"

    with open(metrics_file_path, "w") as f:
        json.dump(metrics_dict, f)

