import base64
import boto3
import hmac
import hashlib
import json
from uuid import uuid4

from masonite.controllers import Controller
from masonite.environment import env
from masonite.request import Request
from masonite.response import Response
from masonite.views import View

from datetime import datetime, timedelta

from app.models.File import File


class FileController(Controller):
    def delete(self, request: Request, response: Response):
        user = request.session.get("user")
        id = request.param("id")
        file = File.where("id", id).where("user_email", user["email"]).first()
        if file:
            client = boto3.client("s3")
            client.delete_object(Bucket=env("AWS_S3_BUCKET"), Key=f"{user['email']}/{file.name}")
            file.delete()
            return response.redirect("/").with_success("File deleted!")
        return response.redirect("/").with_error("File not found!")

    def generate(self, request: Request, response: Response, view: View):
        user = request.session.get("user")
        file_id = request.input("id")
        link_duration = request.input("link_duration")
        try:
            file = File.where("id", file_id).where("user_email", user["email"]).first()
            if file:
                client = boto3.client(
                    "s3",
                    config=boto3.session.Config(signature_version="s3v4"),
                    region_name="ca-central-1",
                )
                response = client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": env("AWS_S3_BUCKET"), "Key": f"{user['email']}/{file.name}"},
                    ExpiresIn=int(link_duration) * 60 * 60,
                )
                return view.render(
                    "generate", {"file": file, "link": response, "link_duration": link_duration}
                )
        except Exception as e:
            print(e)
        return response.json({"error": "File not found!"})

    def save(self, request: Request, response: Response):
        user = request.session.get("user")
        name = request.input("name")
        size = request.input("size")
        type = request.input("type")

        # Check if we already have an entry for the file and need to overwrite it
        file = File.where("name", name).where("user_email", user["email"]).first()
        if file:
            file.name = name
            file.size = size
            file.type = type
            file.av_timestamp = None
            file.av_status = None
            file.av_scanner = None
            file.av_checksum = None
            file.save()
            result = "updated"
        else:
            file = File.create(
                id=str(uuid4()), name=name, size=size, type=type, user_email=user["email"]
            ).fresh()
            result = "created"

        return response.json({"status": result, "id": file.id})

    def share(self, request: Request, view: View):
        user = request.session.get("user")
        id = request.param("id")
        try:
            file = File.where("id", id).where("user_email", user["email"]).first()
            if file:
                file.load_av_tags()
                return view.render("share", {"file": file})
        except Exception as e:
            print(e)
        return view.render("errors/404")

    def sign(self, request: Request, response: Response):

        user = request.session.get("user")
        name = request.input("name")
        key = f"{user['email']}/{name}"
        s3_client = boto3.client(
            "s3",
            config=boto3.session.Config(signature_version="s3v4"),
            region_name="ca-central-1",
        )
        resp = s3_client.generate_presigned_post(env("AWS_S3_BUCKET"), key, ExpiresIn=300)

        return response.json(resp["fields"])
