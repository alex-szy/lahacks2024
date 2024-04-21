import gemini
import reflex as rx
import datetime
class message(rx.Model, table=True):
    sender: int
    recipient: int
    convo_id: tuple[int, int]
    content: str
    timestamp: datetime

def send_message(user, recipient, content):
    with rx.session() as session: #add message to table, want to update state of the table
        #when state of table is updated, 
        session.add(
            message(
                sender = user,
                recipient = recipient,
                convo_id = sorted(user,recipient),
                content = content,
                timestamp = datetime.datetime.now()
            )
        )
        session.commit()

def retrieve_messages(user,recipient):
    convo_id = sorted(user,recipient)
    with rx.session() as session:
        messages = session.exec(
            message.select().where(
                message.convo_id == convo_id
            )
        ).all()
    return messages