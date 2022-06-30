from urllib import response
from tests import TestCase
from app.controllers.AuthController import AuthController

from unittest.mock import ANY, Mock, patch


class AuthControllerTest(TestCase):
    def test_auth(self):
        controller = AuthController()
        response = Mock()
        controller.auth(response)
        response.redirect.assert_called_with(location=ANY)

    def test_callback(self):
        with patch("app.controllers.AuthController.google") as google:
            controller = AuthController()
            request = Mock()
            request.input = Mock(return_value="code")
            session = Mock()
            view = Mock()
            controller.callback(request, session, view)
            google.fetch_token.assert_called_with(
                ANY,
                client_secret=ANY,
                code=ANY,
            )
            google.get.assert_called_with(ANY)
            session.set.assert_called_with("user", ANY)
            view.render.assert_called_with("complete_auth")
