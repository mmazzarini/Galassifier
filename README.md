# GALASSIFIER

Galassifier is a RESTful application and Machine Learning Engineering (MLE) project.
The core of the project is connecting together the process of training of a Convolutional Neural Network (CNN) on galactic images, a
backend inference server, and a simple client interface. 
Serve and client interact by means of REST APIs.

## SERVER
The server is a python django application. 
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
The model was trained with TensorFlow and Keras framework, using a dataset of galaxies selected from
[Galaxy Zoo](https://data.galaxyzoo.org/?_ga=2.107268992.360088703.1763919279-669604038.1763591364)

### Current features:

The model consists of:
- A CNN
- Conv2D and MaxPooling layers
- early stopping regularization

### MLE features
- python modules returning a variety of methods: load/save files, build, train and evaluation of model
- config json file to properly tweak a number of parameters to configure the dataset reduction phase, the training and the model properties, as well as the evaluation phase
- main.py module containing the main orchestrator of the whole MLE pipeline.

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
- Add a reproducible ML training and evaluation pipeline
- Add tests for REST API endpoints
