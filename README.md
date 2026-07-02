# GALASSIFIER

Galassifier is a RESTful application that predicts the type of a galaxy from an input image.
The user uploads a galaxy image through a Vue.js client.
The backend receives the image through a REST API, runs a local machine learning classification process, 
and returns the predicted galaxy class as a JSON response.

## SERVER
The server is a python django application. It exposes REST APIs used by the client to classify galaxy images.

Main responsibilities:

- receive image classification requests from the client
- pass the image to a local Python/TensorFlow classification process
- wait for the prediction result
- return the classification in an HTTP/JSON-compatible format

> Current development server: Django, launched with `python manage.py runserver`.

## MACHINE LEARNING

The core feature of Galassifier is a deep learning model trained to classify galaxy images.
The model was trained with TensorFlow using a dataset of galaxies selected from Galaxy Zoo
(see https://data.galaxyzoo.org/?_ga=2.107268992.360088703.1763919279-669604038.1763591364)

Current model properties:

- convolutional neural network
- Conv2D and MaxPooling layers
- early stopping regularization
- local Python prediction script


## CLIENT

The client is a Vue.js application.

The client:

- navigates between pages using Vue Router
- lets the user upload a galaxy image
- sends POST/GET requests to the backend
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
