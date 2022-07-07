from tests import TestCase
from app.controllers.FileController import FileController

from unittest.mock import ANY, MagicMock, patch


class FileControllerTest(TestCase):
    def test_delete(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.param.return_value = 1
            response = MagicMock()
            with patch("app.controllers.FileController.boto3") as mock_boto3:
                client = MagicMock()
                mock_boto3.client.return_value = client
                file = MagicMock()
                file.name.return_value = "test.txt"
                mock_file.where().where().first.return_value = file
                controller.delete(request, response)
                client.delete_object.assert_called_with(Bucket="share-files-securely", Key=ANY)
                file.delete.assert_called_once()
                response.redirect.assert_called_with("/")
                response.redirect("/").with_success.assert_called_with("File deleted!")

    def test_delete_file_not_found(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.param.return_value = 1
            response = MagicMock()
            mock_file.where().where().first.return_value = False
            controller.delete(request, response)
            response.redirect.assert_called_with("/")
            response.redirect("/").with_error.assert_called_with("File not found!")

    def test_generate_file_not_found(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.return_value = 1
            response = MagicMock()
            view = MagicMock()
            mock_file.where().where().first.return_value = False
            controller.generate(request, response, view)
            response.json.assert_called_with({"error": "File not found!"})

    def test_generate_with_exception(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.return_value = 1
            response = MagicMock()
            view = MagicMock()
            mock_file.where().where().first.side_effect = Exception("test")
            controller.generate(request, response, view)
            response.json.assert_called_with({"error": "File not found!"})

    def test_generate_with_success(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.side_effect = ["1", "60"]
            response = MagicMock()
            view = MagicMock()
            file = MagicMock()
            file.name.return_value = "test.txt"
            mock_file.where().where().first.return_value = file
            with patch("app.controllers.FileController.boto3") as mock_boto3:
                client = MagicMock()
                client.generate_presigned_url.return_value = "https://presigned.url"
                mock_boto3.client.return_value = client
                controller.generate(request, response, view)
                client.generate_presigned_url.assert_called_with(
                    "get_object",
                    Params={"Bucket": "share-files-securely", "Key": ANY},
                    ExpiresIn=60 * 60 * 60,
                )
                view.render.assert_called_with(
                    "generate",
                    {"file": file, "link": "https://presigned.url", "link_duration": "60"},
                )

    def test_save_new_file(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.side_effect = ["test.txt", "100", "mime/type"]
            mock_file.where().where().first.return_value = False
            response = MagicMock()
            controller.save(request, response)
            mock_file.create.assert_called_once()
            mock_file.create.assert_called_with(
                id=ANY,
                name="test.txt",
                size="100",
                type="mime/type",
                user_email="test@email.com",
            )
            response.json.assert_called_with({"status": "created", "id": ANY})

    def test_save_existing_file(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.side_effect = ["1", "100", "mime/type"]
            file = MagicMock()
            mock_file.where().where().first.return_value = file
            response = MagicMock()
            controller.save(request, response)
            mock_file.where().where().first.assert_called_once()
            file.save.assert_called_once()
            response.json.assert_called_with({"status": "updated", "id": ANY})

    def test_share_file_not_found(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.return_value = 1
            view = MagicMock()
            mock_file.where().where().first.return_value = False
            controller.share(request, view)
            view.render.assert_called_with("errors/404")

    def test_share_with_exception(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.return_value = 1
            view = MagicMock()
            mock_file.where().where().first.side_effect = Exception("test")
            controller.share(request, view)
            view.render.assert_called_with("errors/404")

    def test_share_where_file_exists(self):
        with patch("app.controllers.FileController.File") as mock_file:
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.return_value = 1
            view = MagicMock()
            file = MagicMock()
            mock_file.where().where().first.return_value = file
            controller.share(request, view)
            view.render.assert_called_with("share", {"file": file})

    def test_sign(self):
        with patch("app.controllers.FileController.boto3") as mock_boto3:
            client = MagicMock()
            client.generate_presigned_post.return_value = {"fields": {"key": "value"}}
            mock_boto3.client.return_value = client
            controller = FileController()
            request = MagicMock()
            request.session.get.return_value = {"email": "test@email.com"}
            request.input.return_value = "1"
            response = MagicMock()
            controller.sign(request, response)
            client.generate_presigned_post.assert_called_with(
                "share-files-securely", "test@email.com/1", ExpiresIn=300
            )
            response.json.assert_called_with({"key": "value"})
