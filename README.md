# GALASSIFIER

Galassifier is a RESTful application and Machine Learning (ML) engineering project.
The project connects a Convolutional Neural Network (CNN) training pipeline, a Django inference backend, and a Vue.js client.
The server and client communicate through REST APIs. 

## SERVER

The server is a Python/Django application. 
It loads the current CNN and employs it for local inference on images of galaxies.
It exposes a REST API to communicate with the client.

Main responsibilities:

- receive image classification requests from the client
- pass the image to a local Python/TensorFlow classification process
- wait for the prediction result
- return the classification in an HTTP/JSON-compatible format

> Current development server: Django, launched with `python manage.py runserver`.

## MACHINE LEARNING

The core feature of Galassifier is a CNN trained to classify galaxy images.
The model was trained with TensorFlow/Keras, using a dataset of galaxies selected from GalaxyZoo project (see References and Disclaimer below).

### Current features:

The model consists of:
- A CNN
- Conv2D and MaxPooling layers
- early stopping regularization

### ML Engineering features

- Python modules for file loading/saving, model building, training, evaluation, and artifact generation
- JSON configuration file to properly tweak a number of parameters to configure the dataset reduction phase, the training and the model properties, as well as the evaluation phase
- main.py module containing the main orchestrator of the whole ML engineering pipeline.

### Evaluation and artifacts

The training pipeline produces simple JSON artifacts to make each model run easier to inspect and compare.

Current artifacts include:
- model contract JSON
- training metrics JSON
- validation confusion matrix JSON
- debug plot routine

#### Validation confusion matrix

The main evaluation artifact is the validation confusion matrix. 
At the current stage, the project reports validation-set evaluation. A fully independent test set is planned as future work.
If the `use_validation_confusion_matrix` parameter is set to true in the configuration file, the evaluation pipeline creates a
validation confusion matrix artifact in the JSON file.

The classification of galaxies is set as an array of labels: ["Uncertain", "Spiral", "Elliptical"].

Therefore, the validation confusion matrix will be read from the JSON file as follows:

```txt
            Predicted
            U    S    E
True U     00   01   02
     S     10   11   12
     E     20   21   22
```

Rows represent true labels, while columns represent predicted labels. The entries 00, 01, ..., 22 represent positions in the matrix.

#### Debug plots

The pipeline also includes a debug plot routine (currently included by default in the pipeline). This routine takes some of the galaxies in the training dataset and produces plots comparing predictions and true labels, for a qualitative inspection of predictions and failure cases.

## CLIENT

The client is represented by a minimal Vue.js application.

The client:

- navigates between pages (using Vue Router)
- lets the user upload a galaxy image
- sends the galaxy image to the server via REST architecture
- displays the classification result returned by the server

## Development Usage

In a development environment, open two separate terminals.

Start the server:
> python manage.py runserver

Start the client:
> npm run dev

Then open the client in the browser and follow the app UI flow to upload galaxy image.

## TODO

- Deploy the backend to a cloud platform, such as AWS
- Package the client for desktop or mobile distribution
- Improve the ML model with ablation tests
- Complete the reproducible ML training and evaluation pipeline
- Add tests for REST API endpoints

## REFERENCES AND DISCLAIMER

I am neither the author nor the owner of the Galaxy Zoo galaxies dataset used for this project. 
I used the data from Galaxy Zoo Project as follows:

### Galaxy Zoo Project Reference
* Lintott et al. 2008, MNRAS, 389, 1179 ([ADS Link](https://adsabs.harvard.edu/abs/2008MNRAS.389.1179L))

### Galaxy Zoo Data Reference
* Lintott et al. 2011, MNRAS, 410, 166 ([ADS Link](https://adsabs.harvard.edu/abs/2011MNRAS.410..166L))

Data courtesy of Galaxy Zoo and the Sloan Digital Sky Survey (SDSS). Click [here](https://data.galaxyzoo.org) to visit the Galaxy Zoo website.
