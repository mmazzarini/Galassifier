
#looking at my project struct, how do I import models herew? and can I do it?
# yes, you can import the models from the GalassifierCore app in your views.py file. You can do it like this:
from GalassifierCore.models import UserProfile
from GalassifierServer.CORELIBS import keysLibrary as keysLib
from django.contrib.auth.models import User

#class handling login and creatioon of user profiles
class UserProfileLoginAndCreationManager():

    _creating = False

    # static method to instantiate the class only once (singleton pattern)
    @staticmethod
    def GetInstance():
        UserProfileLoginAndCreationManager._creating = True
        if not hasattr(UserProfileLoginAndCreationManager, "_instance"):
            UserProfileLoginAndCreationManager._instance = UserProfileLoginAndCreationManager()
        UserProfileLoginAndCreationManager._creating = False
        return UserProfileLoginAndCreationManager._instance

    #this is to prevent the class from being instantiated more than once,as it is a singleton
    def __init__(self):
        if (self._creating is False):
            raise Exception("UserProfileLoginAndCreationManager is a singleton! Use GetInstance() method to get the instance.")
    
    def __TryLoginUserProfile(username, password):
        
        if(username is None):
            raise ValueError("Empty username")    
        if(password is None):
            raise ValueError("Empty password")
            
        found_credentials = next(({"username": user.username, "password": user.password} for user in UserProfile.objects.all() if UserProfile.user.username == username and UserProfile.user.password == password), None)
        if(found_credentials is None):
            raise ValueError("Invalid username or password")
        
        found_user = UserProfile.objects.get(user__username=username)

        user_information = {
            "username": found_credentials["username"],
            "NUM_GALAXIES_CLASSIFIED": found_user.number_galaxies_classified,
            "NUM_ELLIPTICALS": found_user.number_ellipticals,
            "NUM_SPIRALS": found_user.number_spirals,
            "NUM_UNCERTAIN": found_user.number_uncertain,
            "USER_CREDITS": found_user.user_credits
        }

        return user_information

    def TryLoginUserProfile(self, username, password):
        try:
            user_information = self.__TryLoginUserProfile(username, password)

        except ValueError as e:
            return None, str(e)
        #returning user info and None error msg, meaning it worked    
        return user_information, None 

    #Create user profile methods

    def __TryCreateUserProfile(self, in_username, in_password, in_confirm_password, in_email, in_first_name, in_last_name, in_country, in_userpic=None):

        try: self.__CoreProfileValidityCheck(in_username, in_password, in_confirm_password, in_email, in_first_name, in_last_name, in_country)
        except ValueError as e:
            raise e
        
        #create new userprofile and add it to DB
        new_user = User.objects.create_user(
            username=in_username,
            password=in_password,
            email=in_email,
            first_name=in_first_name,
            last_name=in_last_name
        )

        new_user_profile = UserProfile.objects.create(
            user=new_user,
            user_country = in_country
        )

        return new_user_profile #no error,successful
    

    def TryCreateUserProfile(self, in_username, in_password, in_confirm_password, in_email, in_first_name, in_last_name, in_country, in_userpic=None):

        try:
            new_user_profile = self.__TryCreateUserProfile(in_username, in_password, in_confirm_password, in_email, in_first_name, in_last_name, in_country, in_userpic)
        except ValueError as e:
            return None, str(e)
        #returning user info and None error msg, meaning it worked    
        return new_user_profile, None 

    def __CoreProfileValidityCheck(username, password, confirm_password, email, first_name, last_name, country):

        __required_fields_and_errors = {
            "username": (username, keysLib.GALASSIFIER_USERNAME_FIELD_NAME_INVALID),
            "password": (password, keysLib.GALASSIFIER_PASSWORD_FIELD_NAME_INVALID),
            "confirm_password": (confirm_password, keysLib.GALASSIFIER_CONFIRM_PASSWORD_FIELD_NAME_INVALID),
            "email": (email, keysLib.GALASSIFIER_EMAIL_FIELD_NAME_INVALID),
            "first_name": (first_name, keysLib.GALASSIFIER_FIRST_NAME_FIELD_NAME_INVALID),
            "last_name": (last_name, keysLib.GALASSIFIER_LAST_NAME_FIELD_NAME_INVALID),
            "country": (country, keysLib.GALASSIFIER_COUNTRY_FIELD_NAME_INVALID)
        }

        for field_name, (field_value, error_key) in __required_fields_and_errors.items():
            if field_value is None:
                raise ValueError(f"{error_key}")
        
        if(password != confirm_password):
            raise ValueError(f"{keysLib.GALASSIFIER_PASSWORDS_MISMATCH_FIELD_NAME_INVALID}")

        if UserProfile.objects.filter(user__username=username).exists():
            raise ValueError(f"{keysLib.GALASSIFIER_DUPLICATED_USER_FIELD_NAME_INVALID}")
        