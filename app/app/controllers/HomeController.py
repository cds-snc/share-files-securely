from masonite.views import View
from masonite.controllers import Controller
from masonite.environment import env
from masonite.request import Request

from app.models.File import File


class HomeController(Controller):

    def show(self, request: Request, view: View):
        user = request.session.get("user")
        return view.render("home", {
            "s3_url": f"https://{env('AWS_S3_BUCKET')}.s3.amazonaws.com/",
            "files": File.where("user_email", user["email"]).get()
        })
