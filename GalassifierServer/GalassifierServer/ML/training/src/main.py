
from GalassifierServer.GalassifierServer.ML.training.src.config import load_project_config
from google.colab import drive

drive.mount('/content/drive')

config_data = load_project_config()

LOAD_REMOTE_DATASET = config_data["training_stages"]["load_and_mount_remote_dataset"]
MOUNT_REMOTE_IMAGES = config_data["training_stages"]["mount_remote_images"]
EVALUATE_MODEL = config_data["training_stages"]["evaluate_model"]
SAVE_ARTIFACTS = config_data["training_stages"]["save_artifacts"]
