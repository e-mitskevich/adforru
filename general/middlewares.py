from django.http import HttpResponseRedirect
from django.urls import reverse


class GeneralMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        path = request.get_full_path()
        if path.startswith("/cabinet") and not request.user.is_authenticated:
            if path not in (reverse("cabinet_login"), reverse("cabinet_logout"), reverse("cabinet_registration")):
                return HttpResponseRedirect(reverse("cabinet_login"))

        response = self.get_response(request)

        return response