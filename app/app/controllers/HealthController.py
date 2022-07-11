from masonite.views import View
from masonite.controllers import Controller
from masonite.environment import env
from masonite.response import Response

from app.models.File import File


class HealthController(Controller):
    def show(self, response: Response):
        return response.json({"status": "ok", "sha": env("GIT_SHA")})
