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
