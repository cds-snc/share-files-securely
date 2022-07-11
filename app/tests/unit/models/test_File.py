from masonite.tests import TestCase, DatabaseTransactions
from app.models.File import File

from unittest.mock import Mock, patch
from uuid import uuid4


class FileTest(TestCase, DatabaseTransactions):

    connection = "testing"

    def test_av_tags_set(self):
        with patch("app.models.File.boto3") as mock_boto:
            file = File.create(
                id=str(uuid4()),
                name="test.jpg",
                size=123,
                type="image/jpeg",
                user_email="test@email.com",
            )
            file.av_timestamp = "12345"
            file.save()
            file.load_av_tags()
            mock_boto.client.refute_called()

    def test_av_tags_not_set(self):
        with patch("app.models.File.boto3") as mock_boto:
            file = File.create(
                id=str(uuid4()),
                name="test.jpg",
                size=123,
                type="image/jpeg",
                user_email="test@email.com",
            )
            file.av_timestamp = None
            file.load_av_tags()
            client = Mock()
            mock_boto.client.return_value = client
            client.get_object_tagging.return_value = {
                "TagSet": [
                    {
                        "Key": "av-timestamp",
                        "Value": "12345",
                    },
                    {
                        "Key": "av-status",
                        "Value": "clean",
                    },
                    {
                        "Key": "av-scanner",
                        "Value": "av-scanner",
                    },
                    {
                        "Key": "av-checksum",
                        "Value": "av-checksum",
                    },
                ],
            }
            file.load_av_tags()
            client.get_object_tagging.assert_called_once()
            file.fresh()
            self.assertEqual(file.av_timestamp, "12345")
            self.assertEqual(file.av_status, "clean")
            self.assertEqual(file.av_scanner, "av-scanner")
            self.assertEqual(file.av_checksum, "av-checksum")

    def test_av_tags_not_set_with_error(self):
        with patch("app.models.File.boto3") as mock_boto:
            file = File.create(
                id=str(uuid4()),
                name="test.jpg",
                size=123,
                type="image/jpeg",
                user_email="test@email.com",
            )
            file.av_timestamp = None
            file.load_av_tags()
            client = Mock()
            mock_boto.client.return_value = client
            client.get_object_tagging.side_effect = Exception("error")
            file.load_av_tags()
            client.get_object_tagging.assert_called_once()
            file.fresh()
            self.assertEqual(file.av_timestamp, None)
