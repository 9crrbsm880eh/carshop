from django.shortcuts import redirect
from django.urls import reverse


class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 400:
            return redirect(reverse('not_found'))
        return response
