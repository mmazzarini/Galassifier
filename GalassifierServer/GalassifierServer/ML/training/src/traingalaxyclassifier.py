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

# todo Remove this!!   
#PYTHON_READ_IMAGE_VERSION = 1 # 0: read images from remote website and save them to drive; 1: read images from drive
#PYTHON_READWRITE_DATASET_VERSION = 1 # 0: write dataset to disk in drive; 1: read dataset from drive
#PYTHON_READWRITE_MODEL_VERSION = 1 # 0: write model to disk in drive; 1: read model from drive
#PYTHON_TEST_MODEL_AGAINST_DATA = 1 # 0: do not test the model; 1: test the model
#IMG_SIZE_X = 28
#IMG_SIZE_Y = 28

#how to import a json from a file in drive: https://stackoverflow.com/questions/60348192/how-to-import-a-json-file-from-google-drive-in-google-colab

#Let's build our model
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

#def load_remote_dataset():
if(LOAD_REMOTE_DATASET == True):
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
    #here we load and read the images
    if(MOUNT_REMOTE_IMAGES == True):
        galaxies_images_file_path = 'https://zenodo.org/records/3565489/files/images_gz2.zip'
        galaxies_images_filename = 'images_gz2_v2.zip'
        galaxies_images_file = keras.utils.get_file(galaxies_images_filename, galaxies_images_file_path)
        print(galaxies_images_file)
        #copy images to drive
        shutil.copy(galaxies_images_file, '/content/drive/MyDrive/Galaxies_Zoo')
        galaxies_images_file = keras.utils.get_file(galaxies_images_filename, galaxies_images_file_path)
        print(galaxies_images_file)
    else:
        galaxies_images_filename = 'images_gz2_v2.zip'
        galaxies_images_file = os.path.join('/content/drive/MyDrive/Galaxies_Zoo', galaxies_images_filename)
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

if(LOAD_REMOTE_DATASET == True):

    galaxies_CSV_map_filename = 'gz2_filename_mapping.csv'
    galaxies_CSV_map_file_path = 'https://zenodo.org/records/3565489/files/gz2_filename_mapping.csv'
    galaxies_CSV_map_file = keras.utils.get_file(galaxies_CSV_map_filename, galaxies_CSV_map_file_path)
    print(galaxies_CSV_map_file)
    # Read the CSV file from the zip archive directly
    galaxies_map = pd.read_csv(galaxies_CSV_map_file)
    print(galaxies_map.to_numpy().shape)
    galaxy_map_np = np.empty((0,2), dtype=np.int64)
    index = 0
    for galaxy_data in galaxies_map.to_numpy():
        index += 1
        galaxy_id = int(galaxy_data[0])
        galaxy_asset_id = int(galaxy_data[2]) # Renamed for clarity: this is asset_id, not galaxy_type
        galaxy_map_np = np.append(galaxy_map_np, np.array([[galaxy_id, galaxy_asset_id]],dtype=np.int64), axis=0)

    # Strategy
    # 1. Create a ref to the images:
    #    Map:  ID of galaxy - - - number of picture
    # 2. Build: collection of images: first 7000 = training. second 3000: validation
    # 3. Train

    print(galaxy_map_np.shape)
    print(np.array(galaxies_datatable).shape)
    galaxies_datatable_np = np.array(galaxies_datatable)
    print(galaxies_datatable_np.shape, type(galaxies_datatable_np))

    train_images = []
    train_labels = []
    val_images = []
    val_labels = []
    train_num = math.floor(galaxies_datatable_np.shape[0]*0.70)
    val_num = galaxies_datatable_np.shape[0] - train_num
    total_set_num = train_num + val_num

    dir_images_root = extract_dir + '/' + 'images' + '/'
    print('dir images root: ' + dir_images_root)
    counter = 0
    for galaxy_mapdata in galaxy_map_np:
        if(counter >= total_set_num):
            break
        galaxy_id = galaxy_mapdata[0]
        galaxy_img_num = galaxy_mapdata[1]
        # path
        galaxy_img_path = os.path.join(dir_images_root, str(galaxy_img_num) + '.jpg')

        if not os.path.exists(galaxy_img_path):
              print (f"Warning: path {galaxy_img_path} does not exist!")
        try:
            # 1) load img; 2) array-fy image; 3) normalize it
            img = keras.utils.load_img(galaxy_img_path, color_mode="grayscale", target_size=(IMG_SIZE_X, IMG_SIZE_Y))
            img_array = keras.utils.img_to_array(img)
            img_normalized = img_array / 255.0
            print(f"SUCCESS: image {galaxy_img_path} found!")
        except Exception as e:
            print(f"Error: could not properly load image at path {galaxy_img_path}: {e}")
            continue
        #galaxy type
        gal_type_line_num = (galaxies_datatable_np[:,0] == galaxy_id).nonzero()
        if(gal_type_line_num[0].size == 0):
            continue
        galaxy_type_idx = gal_type_line_num[0][0]
        galaxy_type = galaxies_datatable_np[galaxy_type_idx][1]
        #fill arrays
        if(counter < train_num):
            # train imgs
            train_images.append(img_normalized)
            train_labels.append(galaxy_type)
        else:
            #val imgs
            val_images.append(img_normalized)
            val_labels.append(galaxy_type)
        counter += 1

    #after doing all: let's make numpy-arrays out of our dataset
    train_images = np.array(train_images)
    train_labels = np.array(train_labels)
    val_images = np.array(val_images)
    val_labels = np.array(val_labels)
    print(f'Done processing. Train images len: {len(train_images)}; validation images len: {len(val_images)}.')
else:
    print("Reading dataset from drive...")

loadsave_path = '/content/drive/MyDrive/GalaxyClassificationData/galaxy_classification.npz'

loaded_train_images = []
loaded_train_labels = []
loaded_val_images = []
loaded_val_labels = []

def load_dataset_from_drive():
    global loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels
    data = np.load(loadsave_path)
    loaded_train_images = data['train_images']
    loaded_train_labels = data['train_labels']
    loaded_val_images = data['val_images']
    loaded_val_labels = data['val_labels']

if(LOAD_REMOTE_DATASET == True):

    np.savez (loadsave_path,
            train_images=train_images,
            train_labels=train_labels,
            val_images=val_images,
            val_labels=val_labels)
    loaded_train_images = train_images
    loaded_train_labels = train_labels
    loaded_val_images = val_images
    loaded_val_labels = val_labels
else:
    load_dataset_from_drive()

#build model
model = build_model()

if(LOAD_REMOTE_DATASET == True):
    #train model
    TRAIN_SIZE = 7000
    VALIDATION_SIZE = 3000
    BATCH_SIZE = 32
    NUM_EPOCHS = 50
    #train step
    train_step = math.floor(loaded_train_images.shape[0]/TRAIN_SIZE)
    val_step = math.floor(loaded_val_images.shape[0]/VALIDATION_SIZE)

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
    train_dataset = train_dataset.batch(BATCH_SIZE)

    print(train_dataset.cardinality())

    val_dataset = tf.data.Dataset.from_tensor_slices((sized_val_images, sized_val_labels))
    val_dataset = val_dataset.repeat(25)
    val_dataset = val_dataset.shuffle(10000)
    val_dataset = val_dataset.batch(BATCH_SIZE)
 
    print(val_dataset.cardinality())

    early_stop_callback = keras.callbacks.EarlyStopping(monitor="val_loss",patience=5)
    model_save_callback = keras.callbacks.ModelCheckpoint("my_checkpoint.h5", save_best_only=True, save_freq=1000, monitor="epoch")

    model.fit(x=train_dataset,
              epochs=NUM_EPOCHS,
              validation_data=val_dataset,
              steps_per_epoch=math.ceil(TRAIN_SIZE/BATCH_SIZE),
              callbacks=[early_stop_callback, model_save_callback])

backup_model = []
model_save_path = '/content/drive/MyDrive/GalaxyClassificationModels/my_galaxy_classifier_model.h5'

if(SAVE_ARTIFACTS == True):
    #save
    # Create the directory if it doesn't exist
    output_dir = os.path.dirname(model_save_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model.save(model_save_path)
    print(f"Model saved successfully to: {model_save_path}")
    backup_model = model
else:
    backup_model = keras.models.load_model(model_save_path)

if(EVALUATE_MODEL == True):

    BASE_SHIFT = 5
    TEST_SIZE = 20
    TEST_STEP = math.floor(loaded_train_images.shape[0]/TEST_SIZE)

    correct_predictions = 0

    print(TEST_SIZE, TEST_STEP, BASE_SHIFT + TEST_SIZE*TEST_STEP)

    for idx in range (BASE_SHIFT, BASE_SHIFT + TEST_SIZE*TEST_STEP, TEST_STEP):

        galaxy_image_to_test = loaded_train_images[idx]
        galaxy_label_to_test = loaded_train_labels[idx]
        print(galaxy_image_to_test.shape, galaxy_image_to_test.size, galaxy_image_to_test.dims)
        prediction_labels = backup_model.predict(galaxy_image_to_test.reshape(1,28,28))
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