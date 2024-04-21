import reflex as rx
from lahacks2024.templates import template

@template(route="/check-email", title="Check Email")
def check_email() -> rx.Component:
    return rx.box(
        rx.heading("Check your email", size="1"),
        rx.text("We've sent you a magic link to log in. Please check your email and click the link."),
        align="center",
        padding="25px",
    )