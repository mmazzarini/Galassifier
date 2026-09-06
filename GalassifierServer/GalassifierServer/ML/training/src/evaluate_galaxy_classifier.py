import math
import matplotlib.pyplot as plt
import numpy as np
import config

#simple model evaluation test
def evaluate_model(model, loaded_train_images, loaded_train_labels, loaded_val_images, loaded_val_labels):

    config_data = config.load_project_config()
    IMG_SIZE_X = config_data["model"]["input_image_size"][0]
    IMG_SIZE_Y = config_data["model"]["input_image_size"][1]

    BASE_SHIFT = 5
    TEST_SIZE = 20
    TEST_STEP = math.floor(loaded_train_images.shape[0]/TEST_SIZE)

    correct_predictions = 0

    print(TEST_SIZE, TEST_STEP, BASE_SHIFT + TEST_SIZE*TEST_STEP)

    for idx in range (BASE_SHIFT, BASE_SHIFT + TEST_SIZE*TEST_STEP, TEST_STEP):

        num_channels = 3 if config_data["model"]["use_rgb_input"] else 1
        galaxy_image_to_test = loaded_train_images[idx]
        galaxy_label_to_test = loaded_train_labels[idx]
        #print(galaxy_image_to_test.shape, galaxy_image_to_test.size, galaxy_image_to_test.shape)
        prediction_labels = model.predict(galaxy_image_to_test.reshape(1, IMG_SIZE_X, IMG_SIZE_Y, num_channels))
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
    

