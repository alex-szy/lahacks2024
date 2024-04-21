import reflex as rx
from datetime import datetime


class Message(rx.Model, table=True):
    # sender: str = Field(foreign_key= 'User.username')
    # recipient: str = Field(foreign_key= 'User.username')
    sender: str
    recipient: str
    convo_id: str
    content: str
    timestamp: datetime