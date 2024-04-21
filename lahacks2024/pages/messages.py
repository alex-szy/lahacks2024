from . import gemini
import reflex as rx
from datetime import datetime
from ..backend.user import User
from ..backend.message import message
from sqlmodel import Field



class QueryMessage(rx.State):
    messages: list[message] = []

    def send_message(self, user: str, recipient: str, content: str):
        ordered = sorted([user,recipient])
        convoid = ''.join(ordered)
        with rx.session() as session: #add message to table, want to update state of the table
            #when state of table is updated, 
            session.add(
                message(
                    sender = user,
                    recipient = recipient,
                    convo_id = convoid,
                    content = content,
                    timestamp = datetime.now()
                )
            )
            session.commit()
        return rx.redirect('/chatroom')

    def retrieve_messages(self, user: str, recipient: str):
        ordered = sorted([user,recipient])
        convoid = ''.join(ordered)
        with rx.session() as session:
            messages = session.exec(
                message.select().where(
                    message.convo_id == convoid
                )
            ).all()
        with rx.session() as session:
            usr = session.exec(
                User.select().where(
                    User.username == user
                )
            ).first()
        for msg in messages:
            msg.content = gemini.translate(msg.content,usr.language)
        self.messages = messages
        print(self.messages)

    