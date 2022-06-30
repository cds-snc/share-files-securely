from masonite.middleware import Middleware


class SessionAuthenticationMiddleware(Middleware):
    """Middleware to check if the user is logged in."""

    def before(self, request, response):
        if request.session.has("user") is False:
            return response.redirect(name="auth.login")
        return request

    def after(self, request, response):
        return request
