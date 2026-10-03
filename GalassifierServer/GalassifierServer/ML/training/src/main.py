
import config
from google.colab import drive
import loadsave_utilities as lsutils
import evaluate_galaxy_classifier as eval_galaxy
import train_galaxy_classifier as train_galaxy
import galaxy_dataset as galaxy_data
import contract

drive.mount('/content/drive')

def Galaxy_Classifier():

    config_data = config.load_project_config()
    LOAD_REMOTE_DATASET = config_data["training_stages"]["load_and_mount_remote_dataset"]
    TRAIN_MODEL = config_data["training_stages"]["train_model"]
    EVALUATE_MODEL = config_data["training_stages"]["evaluate_model"]
    RELEASE_CONTRACT = config_data["contract"]["release_contract"]
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

    history = None

    if(TRAIN_MODEL == True):
        trained_model, history = train_galaxy.train_model(model, dataset["train_images"], dataset["train_labels"], 
                                 dataset["val_images"], dataset["val_labels"])

        if(EVALUATE_MODEL == True):

            eval_result = eval_galaxy.evaluate_model(trained_model, dataset["train_images"], dataset["train_labels"],
                                dataset["val_images"], dataset["val_labels"])

            if("evaluation_validation" in eval_result and eval_result["evaluation_validation"] is not None):
                VAL_EVALUATION_FILE_PATH = config_data["run"]["run_filepath"]
                VAL_EVALUATION_FILE_NAME = config_data["run"]["run_validation_evaluation_name"]
                VAL_NUMBER = config_data["run"]["run_version_number"]
                VAL_EXTENSION = config_data["run"]["run_file_extension"]
                save_file_name = VAL_EVALUATION_FILE_PATH + "/" + VAL_EVALUATION_FILE_NAME + str(VAL_NUMBER) + "." + VAL_EXTENSION
                lsutils.save_validation_evaluation(save_file_name, eval_result)

        if(RELEASE_CONTRACT == True):
            contract.release_model_contract(history)
            contract.release_model_metrics(history)


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