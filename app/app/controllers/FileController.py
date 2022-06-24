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
            client = boto3.client("s3", aws_access_key_id=env("AWS_ACCESS_KEY_ID"), aws_secret_access_key=env("AWS_SECRET_ACCESS_KEY"))
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
                    aws_access_key_id=env("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=env("AWS_SECRET_ACCESS_KEY"),
                    config=boto3.session.Config(signature_version='s3v4'),
                    region_name="ca-central-1"
                )
                response = client.generate_presigned_url('get_object',
                                                    Params={'Bucket': env('AWS_S3_BUCKET'),
                                                            'Key': f"{user['email']}/{file.name}"},
                                                    ExpiresIn=int(link_duration) * 60 * 60)
                return view.render("generate", {
                    "file": file,
                    "link": response,
                    "link_duration": link_duration
                })
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
            file.save()
            result = "updated"
        else:
            file = File.create(id=str(uuid4()), name=name, size=size, type=type, user_email=user["email"]).fresh()
            result = "created"

        return response.json({"status": result, "id": file.id})

    def share(self, request: Request, view: View):
        user = request.session.get("user")
        id = request.param("id")
        try:
            file = File.where("id", id).where("user_email", user["email"]).first()
            if file:
                return view.render("share", {
                    "file": file
                })
        except Exception as e:
            print(e)
        return view.render("errors/404")

    def sign(self, request: Request, response: Response):

        user = request.session.get("user")

        name = request.input("name")
        size = request.input("size")
        type = request.input("type")

        key = f"{user['email']}/{name}"

        t = datetime.utcnow()
        amz_date = t.strftime('%Y%m%dT000000Z')
        datestamp = t.strftime('%Y%m%d')

        signing_key = getSignatureKey(env("AWS_SECRET_ACCESS_KEY"), datestamp, "ca-central-1", "s3")

        policy = {
            "expiration": (t + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "conditions": [
                {"bucket": env("AWS_S3_BUCKET")},
                ["starts-with", "$key", user['email']],
                {"success_action_status": "201"},
                ["starts-with", "$Content-Type", type],
                ["content-length-range", 0, size],
                {"x-amz-meta-email": user['email']},
                {"x-amz-credential": f"{env('AWS_ACCESS_KEY_ID')}/{datestamp}/ca-central-1/s3/aws4_request"},
                {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
                {"x-amz-server-side-encryption": "AES256"},
                {"x-amz-date": amz_date},
            ]
        }

        policy_b64 = base64.b64encode(json.dumps(policy).encode()).decode()
        signing_key = getSignatureKey(env("AWS_SECRET_ACCESS_KEY"), datestamp, "ca-central-1", "s3")
        signature = hmac.new(signing_key, policy_b64.encode(), hashlib.sha256).hexdigest()

        payload = {
            "x-amz-signature": signature,
            "x-amz-meta-email": user['email'],
            "x-amz-server-side-encryption": "AES256",
            "x-amz-credential": f"{env('AWS_ACCESS_KEY_ID')}/{datestamp}/ca-central-1/s3/aws4_request",
            "x-amz-algorithm": "AWS4-HMAC-SHA256",
            "x-amz-date": amz_date,
            "success_action_status": "201",
            "Content-Type": type,
            "key": key,
            "policy": policy_b64,
        }
        return response.json(payload)


def signed(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = signed(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = signed(kDate, regionName)
    kService = signed(kRegion, serviceName)
    kSigning = signed(kService, 'aws4_request')
    return kSigning
