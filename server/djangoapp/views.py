from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `login_user` view to handle sign-in requests
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            # Parse username and password from the JSON request body
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            # Try to authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Log in the user
                login(request, user)
                response = {"userName": username, "status": "Authenticated"}
            else:
                response = {"status": "Failed", "message": "Invalid credentials"}
        except Exception as e:
            logger.error(f"Error during login: {e}")
            response = {"status": "Failed", "message": "An error occurred"}
    else:
        response = {"status": "Failed", "message": "Only POST requests are allowed"}

    return JsonResponse(response)


# Create a `logout_user` view to handle sign-out requests
@csrf_exempt
def logout_user(request):
    if request.method == "GET":
        try:
            # Log out the user
            logout(request)
            response = {"userName": "", "status": "Logged out"}
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            response = {"status": "Failed", "message": "An error occurred"}
    else:
        response = {"status": "Failed", "message": "Only GET requests are allowed"}

    return JsonResponse(response)