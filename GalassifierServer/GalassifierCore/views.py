import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from GalassifierServer.settings import MODEL_FULL_PATH
import GalassifierServer.ML.galaxyClassifier as gClassifier
from GalassifierServer.COREUSER.loginFunctions import *
from .models import UserProfile

# Create your views here.

@csrf_exempt
def index(request):

    #let's create the user manager
    userManager = UserProfileLoginAndCreationManager.GetInstance()

    return JsonResponse({"message": "Hello, amazing Client!! You're at the Galassifier index."})
    #todo : return a page with the name of the server and the version of the API, and a link to the documentation.
    # return also the name of the client user (to be done in the future)

@csrf_exempt
def ProcessGalaxyImage(request):
    #todo : process the image sent by the client, and return the result as a JSON object.
    if(request.method != "POST"):
        #todo : process the image and return the result as a JSON object.
        #the request should contain the image in base64 format, and (optional for now, I'll decide later) the name of the galaxy to be processed.
        return JsonResponse({"message": "Invalid request method: expected POST."}, status=550)
    if("image" not in request.FILES):
        return JsonResponse({"message": "Invalid request body: missing 'image' field."}, status=575)

    print("Logging: can proceed to image")

    my_image = request.FILES["image"]

    #now we pass the image to the galassifier-ml, and we return the result as a JSON object.
    galaxy_type, confidence = gClassifier.predict_galaxy_type(my_image, MODEL_FULL_PATH)

    return JsonResponse(
        {
            "success": True,
            "galaxyType": f"{galaxy_type}",
            "confidence": confidence,
            "modelVersion": "PH_SOME_VERSION", # todo add version string         
        }
    )
        
# views Method to try to log User in the app.
@csrf_exempt
def LoginGalassifierUser(request):
    if(request.method != "POST"):
        return JsonResponse({"message": "Invalid request method: expected POST."}, status=400)
    #todo : process the login request and return the result as a JSON object.
    if("username" not in request.POST or "password" not in request.POST):
        return JsonResponse({"message": "Invalid request body: missing 'username' or 'password' field."}, status=400)
    
    username = request.POST["username"]
    password = request.POST["password"]

    userManager = UserProfileLoginAndCreationManager.GetInstance()
    if(userManager is None):
        return JsonResponse({"message":"Internal Error"}, status=404)

    user_information, error = userManager.TryLoginUserProfile(username, password)

    if error is not None:
        return JsonResponse({"message": error}, status=401)

    return JsonResponse({"message": "Login successful", "user_information": user_information})

# views Method to try to create new user.
@csrf_exempt
def CreateGalassifierUser(request):
    if(request.method != "POST"):
        return JsonResponse({"message": "Invalid request method: expected POST."}, status=400)
    
    #todo : process the login request and return the result as a JSON object.
    if("username" not in request.POST or "password" not in request.POST):
        return JsonResponse({"message": "Invalid request body: missing 'username' or 'password' field."}, status=400)
    if("confirm_password" not in request.POST):
        return JsonResponse({"message": "Invalid request body: must submit your password twice for confirmation."}, status=400)
    if("email" not in request.POST):
        return JsonResponse({"message": "Please insert a valid email."}, status=400)
    if("country" not in request.POST):
        return JsonResponse({"message": "Please insert a valid country."}, status=400)
    if("first_name" not in request.POST):
        return JsonResponse({"message": "Please insert a valid country."}, status=400)
    if("last_name" not in request.POST):
        return JsonResponse({"message": "Please insert a valid country."}, status=400)
    

    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    confirm_password = request.POST["confirm_password"]
    country = request.POST["country"]   
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    
    userManager = UserProfileLoginAndCreationManager.GetInstance()
    if(userManager is None):
        return JsonResponse({"message":"Internal Error"}, status=404)

    user_information, error = userManager.TryCreateUserProfile(username, password, confirm_password, email,  first_name, last_name, country, None)

    if error is not None:
        return JsonResponse({"message": error}, status=401)

    return JsonResponse({"message": "Login successful", "user_information": user_information})

