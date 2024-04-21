# Import all the pages.
from lahacks2024.pages import *
from lahacks2024.templates import template
from ..backend.user import User
from reflex_magic_link_auth import MagicLinkAuthState
from sqlmodel import select
import sqlalchemy

import reflex as rx

class MatchingState(rx.State):
    username: str
    name: str
    age: int
    illness: str
    language: str
    persistent_id: str
    current_user_username: str
    current_user_illness: str
    current_user_age: int
    connected_users: list[list]
    matching_users: list[User] = []

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
                self.persistent_id = user.persistent_id
            else:
                self.name = ""
                self.username = ""
                self.age = 0
                self.illness = ""
                self.language = ""
                self.persistent_id = ""
        self.on_load()

    def get_connected_users(self):
        with rx.session() as session:
            self.connected_users = [list(row) for row in session.execute(
                sqlalchemy.text(
                    "SELECT * FROM user WHERE NOT user.username = :u AND user.username IN (SELECT message.sender FROM message WHERE message.sender = :u OR message.recipient = :u UNION SELECT message.recipient FROM message WHERE message.sender = :u OR message.recipient = :u)"
                ),
                {"u": self.username}
            ).all()]

    def find_new_matches(self) -> list[User]:
        with rx.session() as session:
            self.matching_users = session.exec(
                User.select().where(
                    User.illness == self.illness
                ).where(
                    User.username != self.username
                )
            ).all()

            # sort based on closeness score
            self.matching_users = sorted(
                self.matching_users,
                key = lambda user: abs(user.age - self.age) if self.age and isinstance(self.age, int) else user.age
            )

    def on_load(self):
        self.get_connected_users()
        self.find_new_matches()

def match_box_connected_user(userList):
    bio = f'Name: {userList[1]}, Age: {userList[2]}, Illness: {userList[3]}, Language: {userList[4]}'
    redirect_url = f'/chatroom/{MagicLinkAuthState.auth_session.persistent_id}+{userList[5]}'
    return rx.vstack(
        rx.button(
            bio,
            border_radius="lg",
            on_click=rx.redirect(redirect_url)
        ),
        rx.spacer(),
        align_items="start"
    )

def match_box(user: User):
    bio = f'Name: {user.name}, Age: {user.age}, Illness: {user.illness}, Language: {user.language}'
    redirect_url = f'/chatroom/{MagicLinkAuthState.auth_session.persistent_id}+{user.persistent_id}'
    return rx.vstack(
        rx.button(
            bio,
            border_radius="lg",
            on_click=rx.redirect(redirect_url)
        ),
        rx.spacer(),
        align_items="start"
    )

def connected_list():
    return rx.vstack(
        rx.heading("Connected"),
        rx.vstack(
            rx.foreach(
                MatchingState.connected_users, match_box_connected_user
            )
        )
    )

def new_matches_list():
    return rx.vstack(
        rx.heading("Matches"),
        rx.vstack(
            rx.foreach(
                MatchingState.matching_users, match_box
            )
        )
    )

@template(route="/matching", title="Matching", on_load=MatchingState.load_user)
def matching() -> rx.Component:
    return rx.box(
        rx.box(
            connected_list(),
            new_matches_list(),
            padding="4em",
        ),
        font_family="Inter",
    )