from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bypass login check for login and admin pages
        if request.path.startswith(reverse('login')) or request.path.startswith('/admin/'):
            return self.get_response(request)

        # Redirect to login page if user is not authenticated
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")

        return self.get_response(request)
