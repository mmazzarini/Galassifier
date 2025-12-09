Galassifier is a RESTful application that predicts the type of a galaxy to the user that inputs a galaxy image.

SERVER
The server is a Java springboot application.
- it employs RESTful APIs to deal with client POST request to classify an image
- it calls a local python process to classify the galaxy and waits for its response
- returns the response in a HTTP/JSON-compatible format

ML-DEEP LEARNING
The most noticeable feature is a ML model.
- The model was trained using python tensorflow libraries with a set of galaxies selected from GalaxyZoo.
- Properties: Convo2D-Maxpooling classic DeepLearning model (work in progress)
- The model is selected with early-stopping regularization and employed in a python script to predict galaxies types.
- The python script is called locally via process building/handling java libraries

CLIENT
- #TBD Should be some app in node.js / react
