#generic imports
import numpy as np
from tensorflow import keras
import os
import math
import tensorflow as tf
from google.colab import drive
import matplotlib.pyplot as plt
import json
import loadsave_utilities as lsutils
import config

config_data = config.load_project_config()

LOAD_REMOTE_DATASET = config_data["training_stages"]["load_and_mount_remote_dataset"]
MOUNT_REMOTE_IMAGES = config_data["training_stages"]["mount_remote_images"]
EVALUATE_MODEL = config_data["training_stages"]["evaluate_model"]
USE_VALIDATION_SET = config_data["data"]["use_validation_set"]

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


def train_model(model, loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels):
        #if(LOAD_REMOTE_DATASET == True):

        config_data = config.load_project_config()

        train_size = loaded_train_labels.shape[0] 
        validation_size = 0
        if (USE_VALIDATION_SET == True):
            train_size *= (config_data["data"]["dataset_split_ratio"])
            validation_size  = loaded_val_labels.shape[0]*(1. - config_data["data"]["dataset_split_ratio"])
        batch_size = config_data["training"]["batch_size"]
        num_epochs = config_data["training"]["num_epochs"]
 
        #train-val steps
        train_step = math.floor(loaded_train_images.shape[0]/train_size)
        val_step = math.floor(loaded_val_images.shape[0]/validation_size) if (USE_VALIDATION_SET == True) else 0

        #sample only some galaxies
        sized_train_images = loaded_train_images[0:len(loaded_train_images):train_step]
        sized_train_labels = loaded_train_labels[0:len(loaded_train_labels):train_step]
        sized_val_images = loaded_val_images[0:len(loaded_val_images):val_step] if (USE_VALIDATION_SET == True) else []
        sized_val_labels = loaded_val_labels[0:len(loaded_val_labels):val_step] if (USE_VALIDATION_SET == True) else []

        print(len(sized_train_images))
        print(len(sized_train_labels))
        print(len(sized_val_images))
        print(len(sized_val_labels))

        train_dataset = tf.data.Dataset.from_tensor_slices((sized_train_images, sized_train_labels))
        train_dataset = train_dataset.repeat(25)
        train_dataset = train_dataset.shuffle(10000)
        train_dataset = train_dataset.batch(batch_size)

        print(train_dataset.cardinality())

        val_dataset = tf.data.Dataset.from_tensor_slices((sized_val_images, sized_val_labels)) if (USE_VALIDATION_SET == True) else None
        if (USE_VALIDATION_SET == True):
            val_dataset = val_dataset.repeat(25)
            val_dataset = val_dataset.shuffle(10000)
            val_dataset = val_dataset.batch(batch_size)
            print(val_dataset.cardinality())

        modelfile_dir = config_data["extensions"]["model_save_path"]
        modelfile_prefix = os.path.join(modelfile_dir, "model_checkpoint")
        modelfile_version = config_data["extensions"]["model_version_number"]
        modelfile_extension = config_data["extensions"]["model_save_extension"]
        modelfile_filename = modelfile_prefix + "_" + modelfile_version + "." + modelfile_extension

        model_save_callback = keras.callbacks.ModelCheckpoint(modelfile_filename, save_best_only=True, save_freq=1000, monitor="val_loss")
        employed_callbacks = [model_save_callback]
        if(config_data["training"]["use_early_stopping"] == True):
            early_stop_callback = keras.callbacks.EarlyStopping(monitor="val_loss",patience=config_data["training"]["early_stopping_patience"])
            employed_callbacks.append(early_stop_callback)

        train_history = model.fit(x=train_dataset,
                epochs=num_epochs,
                validation_data= val_dataset if (config_data["data"]["use_validation_set"] == True) else None,
                steps_per_epoch=math.ceil(train_size/batch_size),
                callbacks=(employed_callbacks)
        )

        return model, train_history

        # Save the model to the specified path
        # Create the directory if it doesn't exist
        #output_dir = os.path.dirname(model_save_path)
        #if not os.path.exists(output_dir):
        #    os.makedirs(output_dir)

        #model.save(model_save_path)
        #print(f"Model saved successfully to: {model_save_path}")