# GALASSIFIER

Galassifier is a RESTful application and Machine Learning (ML) engineering project.
The project connects a Convolutional Neural Network (CNN) training pipeline, a Django inference backend/Server, and a vue.js Client,.
Server and Client communicate through REST APIs. 

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
The model was trained with TensorFlow/Keras, using a dataset of galaxies selected from
[Galaxy Zoo](https://data.galaxyzoo.org/?_ga=2.107268992.360088703.1763919279-669604038.1763591364)

### Current features:

The model consists of:
- A CNN
- Conv2D and MaxPooling layers
- early stopping regularization

### ML Engineering features

- python modules returning a variety of methods: load/save files, model building, training, evaluation, and artifact generation
- config json file to properly tweak a number of parameters to configure the dataset reduction phase, the training and the model properties, as well as the evaluation phase
- main.py module containing the main orchestrator of the whole ML engineering pipeline.

### Evaluation and artifacts

The training pipeline produces simple JSON artifacts to make each model run easier to inspect and compare.

Current artifacts include:
- a validation confusion matrix
- a debug plot routine to show images and visually compare predictions and true labels

#### Validation confusion matrix

The most relevant one is the Confusion Matrix. 
N.B. At the current stage, the project reports validation-set evaluation. A fully independent test set is planned as future work.
If in the configuration file the parameter "use_validation_confusion_matrix" is set to true, then the evaluation pipeline will create a
validation matrix dictionary in the evaluation data json file.

The classification of galaxies is set as an array of labels: ["Uncertain", "Spiral", "Elliptical"].

Therefore, the confusion matrix will be read from the json eval file with the following fashion:

```txt
            Predicted
            U    S    E
True U     00   01   02
     S     10   11   12
     E     20   21   22
```

Where the rows represent the true labels of the images, and the columns represent the predictions for those images. The numbers 00, 01, ..., 22 represent indexed positions in the matrix.

#### Debug plots

There is an additional set of plots produced with a debug feature (currently included by default in the pipeline) that plots some of the galaxies in the training dataset and produces plots comparing prediction and true label, for a qualitative inspection of predictions and failure cases.

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
