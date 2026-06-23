#module defining contract constants for our ML model.

#model contract constants
MODEL_VERSION = "galassifier-cnn-v1"
INPUT_IMAGE_SIZE = 28
CLASS_NAMES = ['Uncertain', 'Spiral', 'Elliptical']
IMG_COLOR_NORMALIZATION_FACTOR = 255.
INPUT_COLOR_MODE = 'L' #Means grayscale