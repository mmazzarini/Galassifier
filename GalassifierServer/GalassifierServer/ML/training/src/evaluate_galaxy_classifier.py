import math
import matplotlib.pyplot as plt
import numpy as np
import config

#simple model evaluation test
def evaluate_model(model, loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels):

    config_data = config.load_project_config()

    eval_result = {}

    if(config_data["evaluation"]["use_debug_plots"] == True):
        BASE_SHIFT = config_data["evaluation"]["base_shift"]
        TEST_SIZE = config_data["evaluation"]["test_size"]
        TEST_STEP = math.floor(loaded_train_images.shape[0]/TEST_SIZE)
        if(TEST_STEP == 0):
            TEST_STEP = 1
        IMG_SIZE_X = config_data["model"]["input_image_size"][0]
        IMG_SIZE_Y = config_data["model"]["input_image_size"][1]
        NUM_CHANNELS = 3 if config_data["model"]["use_rgb_input"] == True else 1
        debug_predictions = debug_plots(model, loaded_train_images, loaded_train_labels, BASE_SHIFT, TEST_SIZE, TEST_STEP, IMG_SIZE_X, IMG_SIZE_Y, NUM_CHANNELS)

        test_on_train_set = eval_result["test_on_train_set"] = {}
        test_on_train_set["correct_predictions"] = debug_predictions
        test_on_train_set["base_shift"] = BASE_SHIFT
        test_on_train_set["test_size"] = TEST_SIZE
        test_on_train_set["test_step"] = TEST_STEP
        test_on_train_set["img_size_x"] = IMG_SIZE_X
        test_on_train_set["img_size_y"] = IMG_SIZE_Y
        test_on_train_set["num_channels"] = NUM_CHANNELS
        print(f"Done testing: Correct predictions: {debug_predictions} out of {TEST_SIZE}")

    USE_VALIDATION_CONFUSION_MATRIX = config_data["evaluation"]["use_validation_confusion_matrix"]
        
    if(USE_VALIDATION_CONFUSION_MATRIX == True):
        val_confusion_mat, val_correct_predictions, val_accuracy, val_correct_per_class, accuracy_per_class = val_confusion_matrix(model, loaded_val_images, loaded_val_labels)
        eval_result["evaluation_validation"] = {}
        eval_result["evaluation_validation"]["matrix"] = val_confusion_mat
        eval_result["evaluation_validation"]["val_correct_predictions"] = val_correct_predictions
        eval_result["evaluation_validation"]["val_predictions_accuracy"] = val_accuracy
        eval_result["evaluation_validation"]["val_correct_predictions_per_class"] = val_correct_per_class
        eval_result["evaluation_validation"]["val_accuracy_per_class"] = accuracy_per_class
        eval_result["evaluation_validation"]["num_samples"] = loaded_val_labels.shape[0]
    else:
        eval_result["evaluation_validation"] = None

    return eval_result

def debug_plots(model, in_images, in_labels, in_base_shift, in_test_size, in_test_step, in_img_size_x, in_img_size_y, in_num_channels):

    correct_predictions = 0

    print(in_test_size, in_test_step, in_base_shift + in_test_size*in_test_step)

    for idx in range (in_base_shift, in_base_shift + in_test_size*in_test_step, in_test_step):

        galaxy_image_to_test = in_images[idx]
        galaxy_label_to_test = in_labels[idx]
        #print(galaxy_image_to_test.shape, galaxy_image_to_test.size, galaxy_image_to_test.shape)
        prediction_labels = model.predict(galaxy_image_to_test.reshape(1, in_img_size_x, in_img_size_y, in_num_channels))
        prediction_idx = int(np.argmax(prediction_labels, axis=1))
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

    return correct_predictions
    
def val_confusion_matrix(model, loaded_val_images, loaded_val_labels):

    config_data = config.load_project_config()

    predictions = model.predict(loaded_val_images) #arrays of probabilities for each class. N arrays for N images
    predicted_classes = np.argmax(predictions, axis=1)
    val_confusion_mat = np.zeros((config_data["classification"]["classes"].__len__(), config_data["classification"]["classes"].__len__()), dtype=int)
    val_correct_predictions = 0
    for i in range(loaded_val_labels.shape[0]):
        #true ones in rows, vs predicted in columns for each fixed row
        val_confusion_mat[loaded_val_labels[i]][predicted_classes[i]] += 1
        if(loaded_val_labels[i] == predicted_classes[i]):
            val_correct_predictions += 1

    print(f"Validation Confusion Matrix:\n{val_confusion_mat}")
    print(f"Validation correct predictions: {val_correct_predictions} out of {loaded_val_labels.shape[0]}")

    val_correct_per_class = np.zeros((config_data["classification"]["classes"].__len__(),), dtype=int)

    for i in range(config_data["classification"]["classes"].__len__()):
        val_correct_per_class[i] = val_confusion_mat[i][i]

    print(f"Validation correct predictions per class: {val_correct_per_class}")
    samples_per_class = np.sum(val_confusion_mat, axis=1)
    accuracy_per_class = np.divide(
        val_correct_per_class,
        samples_per_class,
        out=np.zeros_like(val_correct_per_class, dtype=float),
        where=samples_per_class != 0
    )

    return val_confusion_mat, val_correct_predictions, 1.0*val_correct_predictions/loaded_val_labels.shape[0], val_correct_per_class, accuracy_per_class
 