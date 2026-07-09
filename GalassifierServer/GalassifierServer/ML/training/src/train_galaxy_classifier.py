#generic imports
import numpy as np
from tensorflow import keras
import pandas as pd
import zipfile
import os
import shutil
import math
import tensorflow as tf
from google.colab import drive
import matplotlib.pyplot as plt
import json

drive.mount('/content/drive')

config_data = []

with open ('GalassifierServer/GalassifierServer/ML/training/Config/galassifier_training_config.json', 'r') as config_file:
    try : 
        config_data = json.load(config_file)
    except json.decoder.JSONDecodeError as e:
        print(f"Error reading JSON configuration file: {e}")

LOAD_REMOTE_DATASET = config_data["training_stages"]["load_and_mount_remote_dataset"]
MOUNT_REMOTE_IMAGES = config_data["training_stages"]["mount_remote_images"]
EVALUATE_MODEL = config_data["training_stages"]["evaluate_model"]
SAVE_ARTIFACTS = config_data["training_stages"]["save_artifacts"]

#method to load the project configuration from a JSON file
def load_project_config():
    global config_data
    if config_data is not None:
        return config_data
    else:
        with open('GalassifierServer/GalassifierServer/ML/training/Config/galassifier_training_config.json', 'r') as config_file:
            try:
                config_data = json.load(config_file)
            except json.decoder.JSONDecodeError as e:
                print(f"Error reading JSON configuration file: {e}")
                return None
    return config_data

#The model will be trained on a number of galaxy pics to learn how to classify them
def build_model():

    model_data = config_data["model"]
    classification_data = config_data["classification"]
    num_channels = 3 if model_data["use_rgb_input"] else 1
    model = keras.Sequential() 
    is_first_layer_added = False
    for index in range(len(model_data["num_filters_levels"])):
            if not is_first_layer_added:
                model.add(keras.layers.Conv2D(filters=model_data["num_filters_levels"][index], 
                            kernel_size=model_data["kernel_size_levels"][index], 
                            activation=model_data["convo2d_activation"],
                            input_shape=(model_data["input_image_size"][0], model_data["input_image_size"][1], num_channels)) 
                        )
                is_first_layer_added = True
            else:
                model.add(keras.layers.Conv2D(filters=model_data["num_filters_levels"][index], 
                            kernel_size=model_data["kernel_size_levels"][index], 
                            activation=model_data["convo2d_activation"]))
            model.add(keras.layers.MaxPooling2D(pool_size=model_data["maxpool_size_levels"][index]))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(len(classification_data["classes"]), activation=model_data["dense_activation"]))
    model.compile(optimizer=model_data["optimizer"], loss="sparse_categorical_crossentropy", metrics=model_data["metrics"])
    return model

#method to define galaxy table, from a csv file converting it into an array
def create_galaxy_table(in_galaxy_file):
    galaxies_np_file = in_galaxy_file.to_numpy()
    galaxies_table = []
    classes = config_data["classification"]["classes"]
    classification_keywords = config_data["classification"]["keyword_search_for_classes_in_data"]
    for line in galaxies_np_file:
        galaxy_type = 0 # means uncertain type
        galaxy_id = line[0]
        galaxy_type_str = str(line[6])
        for class_key in classification_keywords:
            if(class_key in galaxy_type_str):
                galaxy_type = classification_keywords.index(class_key)
                break
        galaxies_table.append([galaxy_id, galaxy_type])
    return galaxies_table

def load_dataset_from_drive(in_loadsave_path):

    data = np.load(in_loadsave_path)
    return (
        data['train_images'],
        data['train_labels'],
        data['val_images'],
        data['val_labels']
    )

def get_model_save_path():
    model_save_path = config_data["extensions"]["model_save_path"]
    model_save_path += config_data["extensions"]["model_save_name"]
    model_save_path += "_"
    model_save_path += config_data["extensions"]["model_version_number"]
    model_save_path += "."
    model_save_path += config_data["extensions"]["model_save_extension"]
    return model_save_path

def save_dataset_to_drive(in_loadsave_path, in_loaded_train_images, in_loaded_train_labels, 
                          in_loaded_val_images, in_loaded_val_labels):
    np.savez(in_loadsave_path,
             train_images=in_loaded_train_images,
             train_labels=in_loaded_train_labels,
             val_images=in_loaded_val_images,
             val_labels=in_loaded_val_labels)

def train_model(model, loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels, model_save_path):
        #if(LOAD_REMOTE_DATASET == True):

        config_data = load_project_config()

        train_size = loaded_train_labels.shape[0] 
        validation_size = 0
        if (config_data["data"]["use_validation_set"] == True):
            train_size *= (config_data["training_stages"]["dataset_split_ratio"])
            validation_size  = loaded_val_labels.shape[0]*(1. - config_data["training_stages"]["dataset_split_ratio"])
        batch_size = config_data["training"]["batch_size"]
        num_epochs = config_data["training"]["num_epochs"]
 
        #train-val steps
        train_step = math.floor(loaded_train_images.shape[0]/train_size)
        val_step = math.floor(loaded_val_images.shape[0]/validation_size)

        #sample only some galaxies
        sized_train_images = loaded_train_images[0:len(loaded_train_images):train_step]
        sized_train_labels = loaded_train_labels[0:len(loaded_train_labels):train_step]
        sized_val_images = loaded_val_images[0:len(loaded_val_images):val_step]
        sized_val_labels = loaded_val_labels[0:len(loaded_val_labels):val_step]

        print(len(sized_train_images))
        print(len(sized_train_labels))
        print(len(sized_val_images))
        print(len(sized_val_labels))

        train_dataset = tf.data.Dataset.from_tensor_slices((sized_train_images, sized_train_labels))
        train_dataset = train_dataset.repeat(25)
        train_dataset = train_dataset.shuffle(10000)
        train_dataset = train_dataset.batch(batch_size)

        print(train_dataset.cardinality())

        val_dataset = tf.data.Dataset.from_tensor_slices((sized_val_images, sized_val_labels))
        val_dataset = val_dataset.repeat(25)
        val_dataset = val_dataset.shuffle(10000)
        val_dataset = val_dataset.batch(batch_size)
    
        print(val_dataset.cardinality())

        model_save_callback = keras.callbacks.ModelCheckpoint("my_checkpoint.h5", save_best_only=True, save_freq=1000, monitor="epoch")
        employed_callbacks = [model_save_callback]
        if(config_data["training"]["use_early_stopping"] == True):
            early_stop_callback = keras.callbacks.EarlyStopping(monitor="val_loss",patience=5)
            employed_callbacks.append(early_stop_callback)

        model.fit(x=train_dataset,
                epochs=num_epochs,
                validation_data= val_dataset if (config_data["data"]["use_validation_set"] == True) else None,
                steps_per_epoch=math.ceil(train_size/batch_size),
                callbacks=(employed_callbacks)
        )

        # Create the directory if it doesn't exist
        output_dir = os.path.dirname(model_save_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        model.save(model_save_path)
        print(f"Model saved successfully to: {model_save_path}")

def train_or_load_model(loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels):
    model_save_path = get_model_save_path()
    trained_model = []
    if(config_data["training_stages"]["save_model"]  == True):
        model = build_model()
        trained_model = train_model(model, loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels, model_save_path)
    else:
        trained_model = keras.models.load_model(model_save_path)

#simple model evaluation test
def evaluate_model(model, loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels):
    BASE_SHIFT = 5
    TEST_SIZE = 20
    TEST_STEP = math.floor(loaded_train_images.shape[0]/TEST_SIZE)

    correct_predictions = 0

    print(TEST_SIZE, TEST_STEP, BASE_SHIFT + TEST_SIZE*TEST_STEP)

    for idx in range (BASE_SHIFT, BASE_SHIFT + TEST_SIZE*TEST_STEP, TEST_STEP):

        galaxy_image_to_test = loaded_train_images[idx]
        galaxy_label_to_test = loaded_train_labels[idx]
        print(galaxy_image_to_test.shape, galaxy_image_to_test.size, galaxy_image_to_test.dims)
        prediction_labels = model.predict(galaxy_image_to_test.reshape(1,28,28))
        prediction_idx = np.argmax(prediction_labels, axis=1)
        prediction = prediction_labels[0][prediction_idx]
        print(f"prediction is: {prediction}; prediction index is: {prediction_idx}")

        prediction_color =""
        if(galaxy_label_to_test != prediction_idx):
            print(f"Wrong prediction!")
            prediction_color = "r"
        else:
            print(f"Correct prediction!")
            prediction_color = "g"
            correct_predictions += 1

        print(f'\n\ncorrect predictions: {correct_predictions}\n\n')
        plt.imshow(galaxy_image_to_test, cmap='gray')
        plt.title(f'galaxy image (Index {idx}), Label: {galaxy_label_to_test}', color=prediction_color)
        plt.axis('off')
        plt.show()

    print(f"Done testing: Correct predictions: {correct_predictions} out of {TEST_SIZE}")
    

def load_remote_dataset():

    #catalog: lets get galaxies
    #using https://data.galaxyzoo.org/?_ga=2.107268992.360088703.1763919279-669604038.1763591364
    #see also https://zenodo.org/records/3565489#.Y3vFKS-l0eY for the images
    galaxies_CSV_filename = 'gz2_hart16.csv.gz'
    galaxies_CSV_file_path = 'https://gz2hart.s3.amazonaws.com/gz2_hart16.csv.gz'
    galaxies_CSV_zip_file = keras.utils.get_file(galaxies_CSV_filename, galaxies_CSV_file_path)
    print(galaxies_CSV_zip_file)
    # Read the CSV file from the zip archive directly
    galaxies_file = pd.read_csv(galaxies_CSV_zip_file)
    galaxies_datatable = create_galaxy_table(galaxies_file)

    galaxies_images_file = []
    galaxies_image_filename = 'images_gz2_v2.zip'
    #here we load and read the images
    if(MOUNT_REMOTE_IMAGES == True):
        galaxies_images_file_path = 'https://zenodo.org/records/3565489/files/images_gz2.zip'
        galaxies_images_file = keras.utils.get_file(galaxies_image_filename, galaxies_images_file_path)
        print(galaxies_images_file)
        #copy images to drive
        
        shutil.copy(galaxies_images_file, '/content/drive/MyDrive/Galaxies_Zoo')
        galaxies_images_file = keras.utils.get_file(galaxies_image_filename, galaxies_images_file_path)
        print(galaxies_images_file)
    else:
        galaxies_images_file = os.path.join('/content/drive/MyDrive/Galaxies_Zoo', galaxies_image_filename)
        print(galaxies_images_file)
        if not os.path.exists(galaxies_images_file):
            print("Warning! The file does not exist in drive directory!")

    if(LOAD_REMOTE_DATASET == True):

        extract_dir = './galaxy_images_truncated'
        os.makedirs(extract_dir, exist_ok=True)

        galaxies_datatable_np = np.array(galaxies_datatable)

        try:
            with zipfile.ZipFile(galaxies_images_file, 'r') as zip_ref:
                all_files_in_zip = zip_ref.namelist()
                print(len(all_files_in_zip))
                extract_count = 0

                for file_name in all_files_in_zip:
                    if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        zip_ref.extract(file_name, extract_dir)
                        extract_count += 1

        except FileNotFoundError:
            print(f"Error: Zip file not found at '{galaxies_images_file}'. Please ensure it was downloaded correctly.")
        except zipfile.BadZipFile:
            print(f"Error: '{galaxies_images_file}' is not a valid zip file or is corrupted. It might have been an incomplete download.")
        except Exception as e:
            print(f"An unexpected error occurred during extraction: {e}")

        #print(extract_dir)
