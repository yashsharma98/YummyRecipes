from django.middleware.common import MiddlewareMixin
from django.http import HttpResponsePermanentRedirect

class TrailingSlashMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.endswith('/'):
            return HttpResponsePermanentRedirect(request.path + '/')


from django.shortcuts import redirect
from django.urls import reverse

class CheckPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.has_usable_password():
            if request.path != reverse('updatepassword'):
                return redirect('updatepassword')
        response = self.get_response(request)
        return response

class ClearExistingUserFirstnameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path == reverse('login'):
            request.session.pop('existing_user_first_name', None)
            request.session.pop('existing_user_email', None)

        return response