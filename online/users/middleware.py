from django.shortcuts import redirect, reverse


class RedirectIfLoggedInMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and (
            request.path == "/users/login/" or request.path == "/users/register/"
        ):
            return redirect(reverse("website:index"))
        response = self.get_response(request)
        return response
