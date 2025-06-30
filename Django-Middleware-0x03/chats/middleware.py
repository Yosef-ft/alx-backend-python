from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
import time

User = get_user_model()

class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        
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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_log = {}

    def __call__(self, request):
        if request.method == 'POST':
            ip_address = request.META.get('REMOTE_ADDR')
            current_time = time.time()

            if ip_address in self.requests_log:
                last_request_time, request_count = self.requests_log[ip_address]
                
                if current_time - last_request_time > 60:
                    self.requests_log[ip_address] = (current_time, 1)
                else:
                    if request_count >= 5:
                        return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
                    self.requests_log[ip_address] = (last_request_time, request_count + 1)
            else:
                self.requests_log[ip_address] = (current_time, 1)

        response = self.get_response(request)
        return response



class RolepermissionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        
        if request.user.is_authenticated:
            if not (request.user.groups.filter(name='admin').exists() or request.user.groups.filter(name='moderator').exists()):
                return HttpResponseForbidden("You do not have permission to perform this action.")

        response = self.get_response(request)
        return response
