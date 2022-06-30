from tests import TestCase
from app.middlewares.TranslateMiddleware import TranslateMiddleware

from unittest.mock import Mock


class TranslateTests(TestCase):
    def test_translate_middleware_with_no_language(self):
        middleware = TranslateMiddleware()
        request = Mock()
        request.session.has = Mock(return_value=False)
        response = Mock()
        response.redirect = Mock()
        middleware.before(request, response)
        request.app.make("view").share.assert_called_once()
        assert middleware._language == "en"

    def test_translate_middleware_with_language(self):
        middleware = TranslateMiddleware()
        request = Mock()
        request.session.has = Mock(return_value=True)
        request.session.get = Mock(return_value="fr")
        response = Mock()
        response.redirect = Mock()
        middleware.before(request, response)
        request.app.make("view").share.assert_called_once()
        assert middleware._language == "fr"

    def test_translate_middleware_with_invalid_language(self):
        middleware = TranslateMiddleware()
        request = Mock()
        request.session.has = Mock(return_value=True)
        request.session.get = Mock(return_value="xx")
        response = Mock()
        response.redirect = Mock()
        middleware.before(request, response)
        request.app.make("view").share.assert_called_once()
        assert middleware._language == "en"

    def test_translate_middleware_after(self):
        middleware = TranslateMiddleware()
        request = Mock()
        response = Mock()
        result = middleware.after(request, response)
        self.assertEqual(result, request)
