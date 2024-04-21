import reflex as rx
from sqlmodel import select, Field
from reflex_magic_link_auth import MagicLinkAuthRecord

class User(rx.Model, table=True):
    username: str = Field(primary_key=True)
    name: str
    age: int
    illness: str
    language: str
    authrecord: int


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