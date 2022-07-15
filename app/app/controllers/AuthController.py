from masonite.controllers import Controller
from masonite.response import Response
from masonite.request import Request
from masonite.views import View

from masonite.environment import env
from masonite.sessions import Session


from requests_oauthlib import OAuth2Session

client_id = env("GOOGLE_CLIENT_ID")
client_secret = env("GOOGLE_CLIENT_SECRET")
redirect_uri = f"{env('APP_URL', 'http://localhost:8000')}/auth/callback"

authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
scope = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)


class AuthController(Controller):
    def auth(self, response: Response):
        authorization_url, _state = google.authorization_url(
            authorization_base_url, access_type="offline", prompt="select_account"
        )
        return response.redirect(location=f"https://accounts.google.com{authorization_url}")

    def callback(self, request: Request, session: Session, view: View):
        google.fetch_token(token_url, client_secret=client_secret, code=request.input("code"))
        resp = google.get("https://www.googleapis.com/oauth2/v2/userinfo")
        session.set("user", resp.json())
        return view.render("complete_auth")

    def logout(self, response: Response, session: Session):
        session.delete("user")
        session.flush()
        return response.redirect(name="home")
