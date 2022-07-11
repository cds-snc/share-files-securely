from tests import TestCase
from app.controllers.HomeController import HomeController

from unittest.mock import Mock, patch


class HomeControllerTest(TestCase):
    def test_show(self):
        with patch("app.controllers.HomeController.File") as mock_file:
            controller = HomeController()
            request = Mock()
            request.session.get = Mock(return_value={"email": "test@email.com"})
            view = Mock()
            file = Mock()
            mock_file.where().get.return_value = [file]
            controller.show(request, view)
            view.render.assert_called_once()
            view.render.assert_called_with(
                "home",
                {
                    "s3_url": "https://share-files-securely.s3.amazonaws.com/",
                    "files": [file],
                },
            )
            file.load_av_tags.assert_called_once()
