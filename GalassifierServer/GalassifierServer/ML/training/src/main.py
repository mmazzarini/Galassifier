
import config
from google.colab import drive
import loadsave_utilities as lsutils
import evaluate_galaxy_classifier as eval_galaxy
import train_galaxy_classifier as train_galaxy
import galaxy_dataset as galaxy_data

drive.mount('/content/drive')

def Galaxy_Classifier():
    ####
    a = 1 #placeholder
    a += 1 #placeholder

    config_data = config.load_project_config()
    LOAD_REMOTE_DATASET = config_data["training_stages"]["load_and_mount_remote_dataset"]
    MOUNT_REMOTE_IMAGES = config_data["training_stages"]["mount_remote_images"]
    TRAIN_MODEL = config_data["training_stages"]["train_model"]
    EVALUATE_MODEL = config_data["training_stages"]["evaluate_model"]

    dataset = []

    if(LOAD_REMOTE_DATASET == True):
        galaxies_datatable_np, galaxy_map_np = galaxy_data.load_remote_dataset()
        dataset = galaxy_data.load_dataset_from_tables(galaxies_datatable_np, galaxy_map_np)
        lsutils.save_dataset_to_drive('/content/drive/MyDrive/Galaxies_Zoo/galaxy_dataset.npz', 
                                          dataset["train_images"],
                                          dataset["train_labels"],
                                          dataset["val_images"],
                                          dataset["val_labels"]
                                      )
    else:
        dataset = lsutils.load_dataset_from_drive('/content/drive/MyDrive/Galaxies_Zoo/galaxy_dataset.npz')

    model = train_galaxy.build_model()

    if(TRAIN_MODEL == True):
        trained_model, history = train_galaxy.train_model(model, dataset["train_images"], dataset["train_labels"], 
                                 dataset["val_images"], dataset["val_labels"])

    if(EVALUATE_MODEL == True):
        eval_galaxy.evaluate_model(trained_model, dataset["train_images"], dataset["train_labels"],
                               dataset["val_images"], dataset["val_labels"])


# MAIN EXECUTION BLOCK!!

if __name__ == "__main__":

    config_data = config.load_project_config()
    USE_LEGACY_CODE = config_data["code"]["use_legacy_code"]
    if(USE_LEGACY_CODE == True):
        print("Using legacy code for dataset loading, model training, and evaluation. !WARNING: This is strongly discouraged and is here only for legacy purposes.")
        #lazy import inside branch to avoid unwanted side effects with new code. We restrict the usage scope of legacy code to this branch only.
        import traingalaxyclassifier as legacy_module
        legacy_module.train_galaxy_classifier()
    else:
        print("Using Galaxy_Classifier() call")
        print("WARNING! This version is currently under development and may not work as expected. So be careful with its usage!")
        Galaxy_Classifier()