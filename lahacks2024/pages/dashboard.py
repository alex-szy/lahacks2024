"""The dashboard page."""
from lahacks2024 import styles
from lahacks2024.templates import template
from sqlmodel import select
from reflex_magic_link_auth import MagicLinkAuthState, MagicLinkAuthSession
from ..backend.user import User

import reflex as rx

class ProfileFormState(rx.State):
    name: str
    username: str
    age: int | None
    illness: str
    language: str
    email: str

    # Populate the form data
    async def load_user(self):
        authstate = await self.get_state(MagicLinkAuthState)
        if not authstate.session_is_valid:
            return rx.redirect("/login")
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.persistent_id == authstate.auth_session.persistent_id)
            ).first()
            if user:
                self.name = user.name
                self.username = user.username
                self.age = user.age
                self.illness = user.illness
                self.language = user.language
                self.email = user.email
            else:
                self.name = ""
                self.username = ""
                self.age = None
                self.illness = ""
                self.language = ""
                self.email = ""

    async def post_user(self, form_data):
        authstate = await self.get_state(MagicLinkAuthState)
        if not authstate.session_is_valid:
            return rx.redirect("/login")
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.persistent_id == authstate.auth_session.persistent_id)
            ).first()
            sesh = session.exec(select(MagicLinkAuthSession).where(MagicLinkAuthSession.persistent_id == authstate.auth_session.persistent_id).first())
            if user:
                user.name = form_data.get("name")
                user.username = form_data.get("username")
                user.age = form_data.get("age")
                user.illness = form_data.get("illness")
                user.language = form_data.get("language")
                session.add(user)
                session.commit()
            else:
                session.add(
                    User(
                        name=form_data.get("name"),
                        username=form_data.get("username"),
                        age=form_data.get("age"),
                        illness=form_data.get("illness"),
                        language=form_data.get("language"),
                        persistent_id=authstate.auth_session.persistent_id,
                        email=sesh.email
                    )
                )
                session.commit()
        return rx.redirect("/dashboard")
            
    


def profileform() -> rx.Component:
    return rx.form.root( 
        rx.flex(
            rx.form.field(
                rx.form.label(f"Username: {ProfileFormState.username}"),
                rx.form.control(
                    rx.input.input(
                        placeholder="Username",
                    ),
                    as_child=True,
                ),
                name="username",
            ),
            rx.form.field(
                rx.form.label(f"Name: {ProfileFormState.name}"),
                rx.form.control(
                    rx.input.input(
                        placeholder="Name",
                    ),
                    as_child=True,
                ),
                name="name",
            ),
            rx.form.field(
                rx.form.label(f"Age: {ProfileFormState.age}"),
                rx.form.control(
                    rx.input.input(
                        placeholder="Age",
                    ),
                    as_child=True,
                ),
                name="age",
            ),
            rx.form.field(
                rx.form.label(f"Illness: {ProfileFormState.illness}"),
                rx.form.control(
                    rx.input.input(
                        placeholder="Illness",
                    ),
                    as_child=True,
                ),
                name="illness",
            ),
            rx.form.field(
                rx.form.label(f"Language: {ProfileFormState.language}"),
                rx.form.control(
                    rx.input.input(
                        placeholder="Language",
                    ),
                    as_child=True,
                ),
                name="language",
            ),
            rx.text(f"Email: {ProfileFormState.email}"),
            rx.form.submit(
                rx.button("Submit"),
                as_child=True,
            ),
            direction="column",
        ),
        on_submit=ProfileFormState.post_user,
        reset_on_submit=True,
    )


@template(route="/dashboard", title="Dashboard", on_load=ProfileFormState.load_user)
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return profileform()
