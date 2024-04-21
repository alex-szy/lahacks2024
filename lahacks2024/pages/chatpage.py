from lahacks2024.templates import template

from lahacks2024 import styles
import reflex as rx

####################################################
###Chat Page UI#####################################
####################################################

def qa(question: str, answer: str) -> rx.Component:
    question_box = rx.cond(
        question=="",
        rx.fragment(),
        rx.box(rx.text(question, style=styles.question_style),
                text_align="right",)
        )
    answer_box = rx.cond(
        answer=="",
        rx.fragment(),
        rx.box(rx.text(answer, style=styles.answer_style),
                text_align="left",)
        )
    return rx.box(
        question_box,
        answer_box,
        margin_y="1em",
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Send a message...",
            on_change=State.set_question,
            style=styles.input_style,
        ),
        rx.button(
            "Send",
            on_click=State.answer,
            style=styles.button_style,
        ),
    )

####################################################
###Binding State to Components######################
####################################################
from lahacks2024.pages.chatstate import State
import asyncio


@template(route="/chatpage", title="Chat")
def chatpage() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat(),
            action_bar(),
            align="center",
        )
    )