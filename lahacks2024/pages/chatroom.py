import gemini
import reflex as rx
from chat_state import ChatState
import messages
from lahacks2024 import styles



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