# GALASSIFIER

Galassifier is a RESTful application and Machine Learning Engineering (MLE) project.
The core of the project is connecting together the process of training of a Convolutional Neural Network (CNN) on galactic images, a
backend inference server, and a simple client interface. 
Server and client interact by means of REST APIs.

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

### MLE features
- python modules returning a variety of methods: load/save files, model building, training, evaluation, and artifact generation
- config json file to properly tweak a number of parameters to configure the dataset reduction phase, the training and the model properties, as well as the evaluation phase
- main.py module containing the main orchestrator of the whole MLE pipeline.

### Evaluation and artifacts
In order tro estimate the impact of the choice of parameters and configuration, as well as the architectural decisions on the MLE pipeline, the MLE system
outputs some evaluation data.
The most relevant one is the Confusion Matrix. 
N.B. due to dataset limitations, I simulated the test dataset using some of the training and validation data that were not used for the training.
If in the configuration file the parameter "use_validation_confusion_matrix" is set to true, then the evaluation pipeline will create a
validation matrix dictionary in the evaluation data json file.

The classification of galaxies is set as an array of labels: ["Uncertain", "Spiral", "Elliptical"].

Therefore, the confusion matrix will be read from the json eval file with the following fashion:

    [U] [S] [E]
[U]  00  01  02
[S]  10  11  12
[E]  20  21  22

Where the rows represent the true labels of the images, and the colums represent the predictions for those images.

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
