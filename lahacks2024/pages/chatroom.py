from . import gemini
import reflex as rx
from .chat_state import ChatState
from . import messages
from lahacks2024 import styles
from lahacks2024.templates import template
from ..backend.user import User

sender = ChatState.sender
recipient = ChatState.recipient
def message_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=ChatState.input,
            placeholder="Send a message...",
            on_change=ChatState.update_text,
            style=styles.input_style,
        ),
        rx.button(
            "Send",
            on_click=ChatState.send_clear, #find out who user and recipient are!!!
            style=styles.button_style,
        ),
    )

def message_display() -> rx.Component:
    # conv_id = sorted(sender,recipient)
    # def get_users(self):
    display = messages.QueryMessage.messages
    return rx.box(
        rx.foreach(
          messages.QueryMessage.messages, render
        )
    )

def render(display: messages.message) -> rx.Component:
    # language = display.sender.language
    message_box = rx.cond(
            sender == display.sender,
            rx.box(rx.text(display.content, style=styles.question_style),
                    align="right", margin_y="1em"),
            rx.box(rx.text(display.content, style=styles.answer_style),
                    align="left", margin_y="1em")
            )
    return message_box#, margin_y="1em")



@template(route="/chatroom",title="Chatroom", on_load=messages.QueryMessage.retrieve_messages('dummy1','dummy2'))
def chatroom() -> rx.Component:
    return rx.center(
        rx.vstack(
        message_display(),
        message_bar()
        )
    )