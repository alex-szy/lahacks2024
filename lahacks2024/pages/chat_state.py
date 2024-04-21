import reflex as rx
import asyncio
from . import messages
from ..backend.user import User


class ChatState(rx.State):
    # sender: User
    # recipient: User
    sender = User(
                username='dummy1',
                name='Alice',
                age=12,
                illness='Cancer',
                language='Chinese'
            )
    recipient = User(
                    username='dummy2',
                    name='Bob',
                    age=32,
                    illness='Cancer',
                    language='French'
                )
    input: str
    def update_text(self, new_text):
        self.input = new_text
    def clear_text(self):
        self.input =""
    def send_clear(self):
        messages.QueryMessage.send_message('dummy1', 'dummy2', self.input)
        self.clear_text()


