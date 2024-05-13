import reflex as rx
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import os, time, json

CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")

class GoogleOAuthProvider(rx.Component):
    library = "@react-oauth/google"
    tag = "GoogleOAuthProvider"

    client_id: rx.Var[str]

class GoogleLogin(rx.Component):
    library = "@react-oauth/google"
    tag = "GoogleLogin"

    on_success: rx.EventHandler[lambda data: [data]]

class OauthState(rx.State):
    def on_success(self, id_token: dict):
        print(
            verify_oauth2_token(
                id_token["credential"],
                requests.Request(),
                CLIENT_ID,
            )
        )

    @rx.cached_var
    def tokeninfo(self) -> dict[str, str]:
        try:
            return verify_oauth2_token(
                json.loads(self.id_token_json)["credential"],
                requests.Request(),
                CLIENT_ID,
            )
        except Exception as exc:
            if self.id_token_json:
                print(f"Error verifying token: {exc}")
        return {}

    def logout(self):
        self.id_token_json = ""

    @rx.var
    def token_is_valid(self) -> bool:
        try:
            return bool(
                self.tokeninfo
                and int(self.tokeninfo.get("exp", 0))
                > time.time()
            )
        except Exception:
            return False
