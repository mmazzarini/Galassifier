#python routine to be called by user or by external program
#it reads an image file path as argument (argv[1])
#then it processes trhe image with a pre-trained ML model to classify the galaxy type
#the routine requires Pillow library to handle images

import sys
import numpy as np
from PIL import Image
import tensorflow as tf

galaxy_types = ['Uncertain', 'Spiral', 'Elliptical']

model = None

def lazy_model_load(in_model_path):
    global model
    if model is None:
        print("Loading galaxy classifier model...") 
        model = tf.keras.models.load_model(in_model_path)
    return model

def predict_galaxy_type(image_path, model_path):
    try:
        #read image and set it to proper format and size
        image = Image.open(image_path).convert('L').resize((28,28))
        image = np.array(image).astype('float32')/255.0
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        #load pretrained ML model
        my_model = lazy_model_load(model_path)
        #prediction
        predictions = my_model.predict(image)
        predicted_galaxy_type_index = np.argmax(predictions)
        confidence = float(predictions[0][predicted_galaxy_type_index])
        print(f"Predicted galaxy type index: {predicted_galaxy_type_index}", file=sys.stderr)
        return (galaxy_types[predicted_galaxy_type_index], confidence)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        #sys.exit(1) todo refactor this

# We will execute this when calling it from command line, e.g. via an external exe.
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("error: usage: python classify.py <image_path> <model_path>", file=sys.stderr)
        #sys.exit(1) to do rewrite this
    image_path = sys.argv[1]
    model_path = sys.argv[2]
    predicted_galaxy_type = predict_galaxy_type(image_path, model_path)
    print(predicted_galaxy_type)
 