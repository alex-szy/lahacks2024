import gemini
import reflex as rx
from chat_state import ChatState
from . import messages
from lahacks2024 import styles
from lahacks2024.templates import template

sender = "Dummy1"
recipient = "Dummy2"
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

def message_display(self, sender, recipient) -> rx.Component:
    conv_id = sorted(sender,recipient)
    # def get_users(self):
    display = messages.retrieve_messages(sender,recipient)
    return rx.box(
        rx.foreach(
          display, render
        )
    )

def render(display) -> rx.Component:
    # language = display.sender.language
    message_box = rx.cond(
            sender == display.sender,
            rx.box(rx.text(display.content, style=styles.question_style),
                    text_align="right",),
            rx.box(rx.text(display.content, style=styles.answer_style),
                    text_align="left",)
            )
    return rx.box(message_box, margin_y="1em")

@template(route="/chatroom",title="Chatroom")
def chatroom() -> rx.Component:
    return rx.center(
        rx.vstack(
        message_display(sender, recipient),
        message_bar()
        )
    )