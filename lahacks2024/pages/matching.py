# Import all the pages.
from lahacks2024.pages import *
from lahacks2024.templates import template
from ..backend.user import User
from sqlmodel import select

import reflex as rx

class MatchingState(rx.State):
    username: str
    name: str
    age: int
    illness: str
    language: str
    users: list[User] = []
    sort_value: str = ""
    num_users: int

    def load_entries(self) -> list[User]:
        """Get all users from the database."""
        with rx.session() as session:
            self.users = session.exec(
                User.select().where(
                    User.illness.contains('ill')
                )
            ).all()

            self.num_users = len(self.users)

            if self.sort_value:
                self.users = sorted(
                    self.users, key=lambda user: getattr(user, self.sort_value)
                )

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def add_user(self):
        """Add a user to the database."""
        with rx.session() as session:
            if session.exec(
                select(User).where(User.username == self.username)
            ).first():
                return rx.window_alert("User already exists")
            session.add(
                User(
                    username=self.username,
                    name=self.name,
                    age=self.age,
                    illness=self.illness,
                    language=self.language
                )
            )
            session.commit()
        self.load_entries()
        return rx.window_alert(f"User {self.username} has been added.")
    
    def on_load(self):
        self.load_entries()

def show_user(user: User):
    """Show a user in a table row."""
    return rx.table.row(
        rx.table.cell(user.username),
        rx.table.cell(user.name),
        rx.table.cell(user.age),
        rx.table.cell(user.illness),
        rx.table.cell(user.language)
    )

def add_user():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.flex(
                    "Add New User",
                    rx.icon(tag="plus", width=24, height=24),
                    spacing="3",
                ),
                size="4",
                radius="full",
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "User Details",
                font_family="Inter",
            ),
            rx.dialog.description(
                "Add your user profile details.",
                size="2",
                mb="4",
                padding_bottom="1em",
            ),
            rx.flex(
                rx.text(
                    "Username",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Username", on_blur=MatchingState.set_username),
                rx.text(
                    "Name",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Name", on_blur=MatchingState.set_name),
                rx.text(
                    "Age",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Age", on_blur=MatchingState.set_age),
                rx.text(
                    "Illness",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Illness", on_blur=MatchingState.set_illness),
                rx.text(
                    "Language",
                    as_="div",
                    size="2",
                    mb="1",
                    weight="bold",
                ),
                rx.input(placeholder="Language", on_blur=MatchingState.set_language),
                direction="column",
                spacing="3",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Submit user",
                        on_click=MatchingState.add_user,
                        variant="solid",
                    ),
                ),
                padding_top="1em",
                spacing="3",
                mt="4",
                justify="end",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1em",
            border_radius="25px",
            font_family="Inter",
        ),
    )

def navbar():
    return rx.hstack(
        rx.vstack(
            rx.heading("User Data App", size="7", font_family="Inter"),
        ),
        rx.spacer(),
        add_user(),
        rx.avatar(fallback="TG", size="4"),
        rx.color_mode.button(rx.color_mode.icon(), size="3", float="right"),
        position="fixed",
        width="100%",
        top="0px",
        z_index="1000",
        padding_x="4em",
        padding_top="2em",
        padding_bottom="1em",
        backdrop_filter="blur(10px)",
    )

def content():
    return rx.fragment(
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.heading(
                    f"Total: {MatchingState.num_users} Users",
                    size="5",
                    font_family="Inter",
                ),
                rx.spacer(),
                rx.select(
                    ["username", "illness"],
                    placeholder="Sort By: Username",
                    size="3",
                    on_change=lambda sort_value: MatchingState.sort_values(sort_value),
                    font_family="Inter",
                ),
                width="100%",
                padding_x="2em",
                padding_top="2em",
                padding_bottom="1em",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Username"),
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Age"),
                        rx.table.column_header_cell("Language"),
                        rx.table.column_header_cell("Illness"),
                    ),
                ),
                rx.table.body(rx.foreach(MatchingState.users, show_user)),
                # variant="surface",
                size="3",
                width="100%",
            ),
        ),
    )

@template(route="/matching", title="Matching")
def matching() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            content(),
            margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        font_family="Inter",
    )