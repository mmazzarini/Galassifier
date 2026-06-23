#this module contains methods to load and use a pre-trained ML model and return the classification of a galaxy image

import sys
import numpy as np
from PIL import Image
import tensorflow as tf
import GalassifierServer.GalassifierServer.ML.modelContract as mContract

model = None

def lazy_model_load(in_model_path):
    global model
    if model is None:
        print("Loading galaxy classifier model...", file=sys.stderr) 
        model = tf.keras.models.load_model(in_model_path)
    return model

def predict_galaxy_type(image_path, model_path):
    try:
        #read image and set it to proper format and size
        image = Image.open(image_path).convert(mContract.INPUT_COLOR_MODE).resize((mContract.INPUT_IMAGE_SIZE, mContract.INPUT_IMAGE_SIZE))
        image = np.array(image).astype('float32')/mContract.IMG_COLOR_NORMALIZATION_FACTOR
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        #load pretrained ML model
        my_model = lazy_model_load(model_path)
        #prediction
        predictions = my_model.predict(image)
        predicted_galaxy_type_index = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_galaxy_type_index])
        print(f"Predicted galaxy type index: {predicted_galaxy_type_index}", file=sys.stderr)
        return (mContract.CLASS_NAMES[predicted_galaxy_type_index], confidence, mContract.MODEL_VERSION)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        raise
# We will execute this when calling it from command line, e.g. via an external exe.
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("error: usage: python classify.py <image_path> <model_path>", file=sys.stderr)
        #sys.exit(1) to do rewrite this
    image_path = sys.argv[1]
    model_path = sys.argv[2]
    predicted_galaxy_type = predict_galaxy_type(image_path, model_path)
    print(predicted_galaxy_type)
 