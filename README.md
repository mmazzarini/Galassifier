Galassifier is a RESTful application that predicts the type of a galaxy to the user that inputs a galaxy image.

SERVER
The server is a python django application.
- it employs REST APIs to deal with client POST request to classify an image
- it calls a local python module to classify the galaxy and waits for its response
- returns the response in a JSON format

ML-DEEP LEARNING
The most noticeable feature is a ML model.
- The model was trained using python tensorflow libraries with a set of galaxies selected from GalaxyZoo.
- Properties: Convo2D-Maxpooling classic DeepLearning model (work in progress)
- The model is selected with early-stopping regularization and employed in a python script to predict galaxies types.
- The python script is called locally via process building/handling java libraries

CLIENT
- Client is an app in vue.js. The client:
- navigates through pages via router calls
- sends POST/GET requests to Server, to allow interactions with the core backend services.


EXAMPLE USAGE (In dev environment - vscode):
From 2 separate terminals:
- launch server with "python manage.py runserver"
- launch client with "npm run dev"
- enjoy :))

TODOS:
- dock and run server app on some platform (AWS for instance)
- wrap client, when done, in a proper framework to distribute the executable to platforms (e.g. it would be nice to have the app on the phone or on desktop)
- improvements to ML: ablation test, production and postprod pipeline on ML-side.
- additional service to include: user profile management, credits management...
