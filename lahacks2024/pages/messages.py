from . import gemini
import reflex as rx
from datetime import datetime
from ..backend.user import User
from sqlmodel import Field
class message(rx.Model, table=True):
    # sender: str = Field(foreign_key= 'User.username')
    # recipient: str = Field(foreign_key= 'User.username')
    sender: str
    recipient: str 
    convo_id: str
    content: str
    timestamp: datetime

class QueryMessage(rx.State):
    messages: list[message] = []

    def send_message(self, user: User, recipient: User, content: str):
        ordered = sorted([user.username,recipient.username])
        convoid = ''.join(ordered)
        with rx.session() as session: #add message to table, want to update state of the table
            #when state of table is updated, 
            session.add(
                message(
                    sender = user.username,
                    recipient = recipient.username,
                    convo_id = convoid,
                    content = content,
                    timestamp = datetime.datetime.now()
                )
            )
            session.commit()

    def retrieve_messages(self, user: User, recipient: User):
        ordered = sorted([user.username,recipient.username])
        convoid = ''.join(ordered)
        with rx.session() as session:
            messages = session.exec(
                message.select().where(
                    message.convo_id == convoid
                )
            ).all()
        self.messages = messages