import reflex as rx
from lahacks2024.templates import template
from reflex_magic_link_auth import MagicLinkAuthState

@template(route="/logout", title="Logout", on_load=MagicLinkAuthState.logout)
def logout() -> rx.Component:
    return rx.vstack(
        rx.text("You have been logged out successfully."),
        rx.link("Go back to the home page", href="/")
    )
