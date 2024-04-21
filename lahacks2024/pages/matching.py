# Import all the pages.
from lahacks2024.pages import *
from lahacks2024.templates import template
from ..backend.user import User, MatchingState

import reflex as rx

class User(rx.Model, table=True):
    username: str = Field(primary_key=True)
    name: str
    age: int
    illness: str
    language: str

class MatchingState(rx.State):
    username: str
    name: str
    age: int
    illness: str
    language: str
    current_user_illness: str
    current_user_age: int
    connected_users: list[User] = []
    matching_users: list[User] = []

    def get_connected_users(self) -> list[User]:
        # with rx.session() as session:
        #     self.connected_users = session.exec(

        #     )
        return

    def find_new_matches(self) -> list[User]:
        with rx.session() as session:
            # test variables
            self.current_user_illness = ""
            self.current_user_age = 14

            self.matching_users = session.exec(
                User.select().where(
                    User.illness.contains(self.current_user_illness)
                )
            ).all()

            # sort based on closeness score
            self.matching_users = sorted(
                self.matching_users, key = lambda user: abs(user.age - self.current_user_age)
            )

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
        self.find_new_matches()
        return rx.window_alert(f"User {self.username} has been added.")
    
    def on_load(self):
        self.find_new_matches()

def show_user(user: User):
    """Show a user in a table row."""
    return rx.table.row(
        rx.table.cell(user.username),
        rx.table.cell(user.name),
        rx.table.cell(user.age),
        rx.table.cell(user.illness),
        rx.table.cell(user.language)
    )

def find_match_button():
    return rx.button(
        "Find new match", on_click=MatchingState.find_new_matches()
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
        find_match_button(),
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

def match_box(user: User):
    bio = f'Name: {user.name}, Age: {user.age}, Illness: {user.illness}, Language: {user.language}'
    return rx.vstack(
        rx.button(
            bio,
            # on_click=lambda statement=statement, index=index: RoundState.reveal_statement_class(statement[0], index),
            # bg=RoundState.half_truths_bg[statement[0]],
            border_radius="lg",
            # variant=rx.cond(
            #     (RoundState.half_truths_bg[index] == "red") | (RoundState.half_truths_bg[index] == "green"), 
            #     "unstyled", 
            #     "solid"
            # ),
            # is_disabled=RoundState.half_truths_clicked[index],
            # style={"_hover": {"bg": rx.cond(RoundState.half_truths_clicked[index], RoundState.half_truths_bg[index], "#ebedf0")}},
        ),
        rx.spacer(),
        align_items="start"
    )
    # bio = f'Age: {user.age}, Illness: {user.illness}, Language: {user.language}'
    # return rx.vstack(
    #     rx.button(
    #         rx.vstack(
    #             rx.text(
    #                 user.name,
    #                 size="3",
    #                 style=button_title_style
    #             ),
    #             rx.text(
    #                 bio,
    #                 size="1",
    #                 style=button_body_style
    #             ),
    #             align_items="start",
    #             spacing="1",
    #             padding_y="3",
    #             padding_right="3"
    #         ),
    #     # border=f"{'2px' if highlight_color != None else '0px'} solid {highlight_color}",
    #     # class_name=styles.BOUNCEIN_ANIMATION if animated else None,
    #     # on_click=rx.redirect(path=url, external=is_external)
    #     ),
    #     rx.spacer(),
    #     align_items="start"
    # )
    # return rx.hstack(
    #     rx.box(
    #         user.name
    #     ),
    #     rx.box(
    #         user.age
    #     ),
    #     rx.box(
    #         user.illness
    #     ),
    #     rx.box(
    #         user.language
    #     )
    # )


def connected_list():
    return rx.vstack(
        rx.heading("Connected"),
        rx.vstack(
            rx.foreach(
                MatchingState.connected_users, match_box
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
    # return rx.fragment(
    #     rx.vstack(
    #         rx.divider(),
    #         rx.hstack(
    #             rx.heading(
    #                 f"Total: {MatchingState.num_users} Users",
    #                 size="5",
    #                 font_family="Inter",
    #             ),
    #             rx.spacer(),
    #             # rx.select(
    #             #     ["username", "illness"],
    #             #     placeholder="Sort By: Username",
    #             #     size="3",
    #             #     on_change=lambda sort_value: MatchingState.sort_values(sort_value),
    #             #     font_family="Inter",
    #             # ),
    #             width="100%",
    #             padding_x="2em",
    #             padding_top="2em",
    #             padding_bottom="1em",
    #         ),
    #         rx.table.root(
    #             rx.table.header(
    #                 rx.table.row(
    #                     rx.table.column_header_cell("Username"),
    #                     rx.table.column_header_cell("Name"),
    #                     rx.table.column_header_cell("Age"),
    #                     rx.table.column_header_cell("Illness"),
    #                     rx.table.column_header_cell("Language"),
    #                 ),
    #             ),
    #             rx.table.body(rx.foreach(MatchingState.users, show_user)),
    #             # variant="surface",
    #             size="3",
    #             width="100%",
    #         ),
    #     ),
    # )

@template(route="/matching", title="Matching", on_load=MatchingState.on_load)
def matching() -> rx.Component:
    return rx.box(
        # navbar(),
        rx.box(
            new_matches_list(),
            # margin_top="calc(50px + 2em)",
            padding="4em",
        ),
        font_family="Inter",
    )