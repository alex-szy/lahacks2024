"""Welcome to Reflex!."""

# Import all the pages.
from lahacks2024.pages import *
import reflex as rx
import os

# class State(rx.State):
    # """Define empty state to allow access to rx.State.router."""

from .components.react_oauth_google import (
    GoogleOAuthProvider,
    GoogleLogin,
    OauthState,
)


def index():
    return rx.vstack(
        GoogleOAuthProvider.create(
            GoogleLogin.create(on_success=OauthState.on_success),
            client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
        )
    )


# Create the app.
app = rx.App()
app.add_page(index)