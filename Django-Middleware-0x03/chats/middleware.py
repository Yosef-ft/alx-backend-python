from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # Ensure the log file exists
        log_file_path = settings.BASE_DIR / 'requests.log'
        if not log_file_path.exists():
            with open(log_file_path, 'w'):
                pass


    def __call__(self, request):

        user = request.user
        log_file_path = settings.BASE_DIR / 'requests.log'

        with open(log_file_path, 'a') as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        response = self.get_response(request)


        return response
    


class RestrictAccessByTimeMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if not (6 <= current_hour < 21):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Access denied outside of 6:00PM to 9:00PM.")
        
        response = self.get_response(request)
        return response
