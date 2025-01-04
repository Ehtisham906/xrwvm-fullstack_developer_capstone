from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from .restapis import get_request, analyze_review_sentiments, post_review

from .models import CarMake, CarModel
from .populate import initiate

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

# Create a `registration` view to handle user registration
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            # Parse user details from the JSON request body
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                response = {"userName": username, "error": "Already Registered"}
            else:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                # Log in the new user
                login(request, user)
                response = {"userName": username, "status": "Authenticated"}
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            response = {"status": "Failed", "message": "An error occurred"}
    else:
        response = {"status": "Failed", "message": "Only POST requests are allowed"}

    return JsonResponse(response)

# View to get car data
def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()  # Populate the database if empty
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
    return JsonResponse({"CarModels": cars})

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})


# Get dealer details by dealer_id
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Get dealer reviews by dealer_id and analyze sentiments
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response.get('sentiment', 'neutral')
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})