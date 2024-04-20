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
    with rx.session() as session:
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