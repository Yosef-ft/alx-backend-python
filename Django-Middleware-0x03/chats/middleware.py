from datetime import datetime

from django.contrib.auth import get_user_model

User = get_user_model()

class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        user = request.user

        with open('requests.log', 'a') as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        response = self.get_response(request)


        return response
