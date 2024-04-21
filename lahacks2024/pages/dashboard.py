"""The dashboard page."""
from lahacks2024 import styles
from lahacks2024.templates import template

import reflex as rx


@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.text("Time Spent on Chatting"),
        rx.text("14H 29M"),
        )
