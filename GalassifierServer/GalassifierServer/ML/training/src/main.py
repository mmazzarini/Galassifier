
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
    EVALUATE_MODEL = config_data["training_stages"]["evaluate_model"]
    SAVE_ARTIFACTS = config_data["training_stages"]["save_artifacts"] 
    
    dataset = []

    if(LOAD_REMOTE_DATASET == True):
        galaxies_datatable_np, galaxy_map_np =galaxy_data.load_remote_dataset()
        dataset = galaxy_data.load_dataset_from_tables(galaxies_datatable_np, galaxy_map_np)
        lsutils.save_dataset_to_drive('/content/drive/MyDrive/Galaxies_Zoo/galaxy_dataset.npz', 
                                      {
                                          dataset["train_images"],
                                          dataset["train_labels"],
                                          dataset["val_images"],
                                          dataset["val_labels"]
                                      })
    else:
        datafile = lsutils.load_dataset_from_drive('/content/drive/MyDrive/Galaxies_Zoo/galaxy_dataset.npz')
        dataset = galaxy_data.create_galaxy_table(datafile)

    galaxy_table = galaxy_data.create_galaxy_table()

    model = train_galaxy.build_model()
    model = train_galaxy.train_model(model, dataset["train_images"], dataset["train_labels"], 
                                 dataset["val_images"], dataset["val_labels"], 
                                 lsutils.get_model_save_path())
    #model = keras.models.load_model(lsutils.get_model_save_path())

    eval_galaxy.evaluate_model(model, dataset["train_images"], dataset["train_labels"],
                               dataset["val_images"], dataset["val_labels"])

if __name__ == "__main__":
    Galaxy_Classifier()