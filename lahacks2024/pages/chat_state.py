import reflex as rx
import asyncio
from . import messages


class ChatState(rx.State):
    input: str
    def update_text(self, new_text):
        self.input = new_text
    def clear_text(self):
        self.input =""
    def send_clear(self, user, recipient):
        messages.send_message(user,recipient, self.input)
        self.clear_text()


