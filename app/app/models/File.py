"""File Model."""
import boto3

from masonite.environment import env
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin


class File(Model, SoftDeletesMixin):
    __fillable__ = ["id", "name", "size", "type", "user_email"]

    def load_av_tags(self):
        if self.av_timestamp is None:
            key = f"{self.user_email}/{self.name}"
            s3_client = boto3.client("s3", region_name="ca-central-1")
            try:
                response = s3_client.get_object_tagging(Bucket=env("AWS_S3_BUCKET"), Key=key)
                tag_dict = {t["Key"]: t["Value"] for t in response["TagSet"]}
                if len(tag_dict) > 0:
                    self.av_timestamp = tag_dict["av-timestamp"]
                    self.av_status = tag_dict["av-status"]
                    self.av_scanner = tag_dict["av-scanner"]
                    self.av_checksum = tag_dict["av-checksum"]
                    self.save()
            except Exception as e:
                print(e)
