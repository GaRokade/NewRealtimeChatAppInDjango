from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that should bypass the login requirement
        exempt_paths = [
            reverse('login'),  # Login page
            reverse('register'),  # Register page
            '/admin/',  # Admin panel
        ]

        # Allow access to exempt paths
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)

        # Redirect to login page if user is not authenticated
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")

        return self.get_response(request)
