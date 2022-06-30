from tests import TestCase
from app.middlewares.SessionAuthenticationMiddleware import SessionAuthenticationMiddleware

from unittest.mock import Mock


class SessionAuthenticationTests(TestCase):
    def test_session_authentication_middleware_with_no_session(self):
        middleware = SessionAuthenticationMiddleware()
        request = Mock()
        request.session.has = Mock(return_value=False)
        response = Mock()
        response.redirect = Mock()
        middleware.before(request, response)
        response.redirect.assert_called_once()
        response.redirect.assert_called_with(name="auth.login")
        request.session.has.assert_called_once()

    def test_session_authentication_middleware_with_session(self):
        middleware = SessionAuthenticationMiddleware()
        request = Mock()
        request.session.has = Mock(return_value=True)
        response = Mock()
        result = middleware.before(request, response)
        request.session.has.assert_called_once()
        self.assertEqual(result, request)

    def test_session_authentication_middleware_after(self):
        middleware = SessionAuthenticationMiddleware()
        request = Mock()
        response = Mock()
        result = middleware.after(request, response)
        self.assertEqual(result, request)
