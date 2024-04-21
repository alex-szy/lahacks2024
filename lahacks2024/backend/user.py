import reflex as rx
from sqlmodel import Field, Relationship
from reflex_magic_link_auth import MagicLinkAuthRecord
from typing import Optional

class User(rx.Model, table=True):
    username: str = Field(unique=True)
    name: str
    age: int
    illness: str
    language: str
    persistent_id: str = Field(primary_key=True)