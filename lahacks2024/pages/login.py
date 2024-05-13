"""The login page"""

import reflex as rx
from lahacks2024.templates import template
from .index import LoginState
from reflex_magic_link_auth import MagicLinkAuthState, send_magic_link_mailgun

class LoginPageState(rx.State):
    login_error: str = ""

    @rx.cached_var
    def is_prod_mode(self):
        return rx.utils.exec.is_prod_mode()

    async def handle_submit_login(self, form_data):
        magic_link = await self.get_state(MagicLinkAuthState)
        self.login_error = ""
        record, otp = magic_link._generate_otp(form_data["email"])
        if otp is None:
            if record is not None:
                self.login_error = "Too many attempts. Please try again later."
            else:
                self.login_error = (
                    "Invalid email, or too many attempts. Please try again later."
                )
            return
        yield rx.redirect("/check-email")

        if self.is_prod_mode:
            try:
                send_magic_link_mailgun(
                    record.email,
                    magic_link._get_magic_link(record, otp),
                )
            except Exception as e:
                print(e)
        else:
            print(magic_link._get_magic_link(record, otp))


def login_controls() -> rx.Component:
    return rx.vstack(
        rx.input.root(
            rx.input(name="email", placeholder="Email", type="email"),
            width="100%",
        ),
        rx.button("Send Magic Link", width="100%"),
    )


def login_form() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Enter your email to log in", size="8", margin_bottom="10px"),
            rx.cond(
                LoginPageState.login_error,
                rx.callout.root(
                    rx.callout.text(LoginPageState.login_error, color="red"),
                    width="100%",
                ),
            ),
            rx.form(
                login_controls(),
                on_submit=LoginPageState.handle_submit_login,
                on_mount=MagicLinkAuthState.get_base_url,
            ),
            align="center",
        ),
    )


@template(route="/login", title="Login", on_load=LoginState.check_and_redirect("/login"))
def login() -> rx.Component:
    return rx.vstack(
        rx.heading("Login"),
        login_form()
    )