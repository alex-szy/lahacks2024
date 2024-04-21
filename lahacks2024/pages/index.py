"""The home page of the app."""

from lahacks2024 import styles
from lahacks2024.templates import template
from reflex_magic_link_auth import MagicLinkAuthState

import reflex as rx

class LoginState(rx.State):
    """
    Global state for login status.
    """

    is_logged_in: bool = False

    async def check_and_redirect(self, current_route: str):
        """
        Check if the user is logged in.
        """
        authstate = await self.get_state(MagicLinkAuthState)
        if authstate.session_is_valid and current_route != "/":
            return rx.redirect("/")
        elif current_route != "/login":
            return rx.redirect("/login")


@template(route="/", title="Home")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
